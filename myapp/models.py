from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.core.validators import validate_email

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    run = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, unique=True)
    prevision = models.CharField(max_length=50)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.prevision = self.prevision.strip().lower()  # Limpieza del campo prevision
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class Especialidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.strip()
        if not self.nombre:
            raise ValidationError('El nombre no puede estar vacío.')
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean is called
        super(Especialidad, self).save(*args, **kwargs)

class Especialista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    run = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class Pago(models.Model):
    numero_reserva = models.IntegerField(unique=True)
    fecha = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00, null=True, blank=True)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)

    COSTOS = [
        (5000.00, 'Consulta General'),
        (6000.00, 'Consulta Especializada'),
        (7500.00, 'Control Médico'),
        (8500.00, 'Emergencia Médica')
    ]

    def clean(self):
        if not isinstance(self.fecha, date):
            raise ValidationError('Fecha inválida.')
        if self.fecha < date.today():
            raise ValidationError('La fecha no puede ser en el pasado.')
        if self.costo is not None and self.costo not in dict(self.COSTOS):
            raise ValidationError('El costo debe ser uno de los valores permitidos.')

    def __str__(self):
        return f"Pago {self.numero_reserva} - {self.especialista}"

class HorariosAtencion(models.Model):
    dia_semana = models.CharField(max_length=20)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_cita = models.IntegerField()
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('fecha', 'hora_inicio', 'especialista')

    def __str__(self):
        return f"{self.dia_semana} - {self.especialista}"

    def clean(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError('La hora de fin debe ser posterior a la hora de inicio.')

    def cancelar(self):
        self.activo = False
        self.save()
        # Notificar al cliente sobre la cancelación
        for reserva in self.reserva_set.all():
            Notificacion.objects.create(
                mensaje=f"Su cita para el {self.fecha} a las {self.hora_inicio} ha sido cancelada.",
                especialista=self.especialista,
                leido=False
            )

    def proponer_reagendar(self, nueva_fecha, nueva_hora_inicio, nueva_hora_fin):
        self.fecha = nueva_fecha
        self.hora_inicio = nueva_hora_inicio
        self.hora_fin = nueva_hora_fin
        self.save()
        # Notificar al cliente sobre la propuesta de nueva fecha
        for reserva in self.reserva_set.all():
            Notificacion.objects.create(
                mensaje=f"Su cita ha sido propuesta para reagendar al {self.fecha} a las {self.hora_inicio}. Por favor confirme.",
                especialista=self.especialista,
                leido=False
            )

    def desactivar(self):
        self.activo = False
        self.save()

    def activar(self):
        self.activo = True
        self.save()

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('asignado', 'Asignado'),
        ('solucionado', 'Solucionado'),
        ('cerrado', 'Cerrado'),
        ('confirmado', 'Confirmado'),  # Nuevo estado agregado
    ]

    nro_reserva = models.IntegerField(unique=True, editable=False)
    agendar_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='asignado')
    comentario = models.TextField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    horario_atencion = models.ForeignKey(HorariosAtencion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cliente', 'horario_atencion')

    def __str__(self):
        return f"Reserva {self.nro_reserva} - {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.nro_reserva:
            last_reserva = Reserva.objects.all().order_by('nro_reserva').last()
            if last_reserva:
                self.nro_reserva = last_reserva.nro_reserva + 1
            else:
                self.nro_reserva = 1000
        super(Reserva, self).save(*args, **kwargs)

    def cancelar(self):
        self.estado = 'cerrado'
        self.save()
        # Notificar al cliente sobre la cancelación
        Notificacion.objects.create(
            mensaje=f"Su reserva número {self.nro_reserva} ha sido cancelada.",
            especialista=self.horario_atencion.especialista,
            leido=False
        )

    def proponer_reagendar(self, nueva_fecha, nueva_hora_inicio, nueva_hora_fin):
        self.horario_atencion.proponer_reagendar(nueva_fecha, nueva_hora_inicio, nueva_hora_fin)
        self.estado = 'solucionado'
        self.save()

    def desactivar(self):
        self.horario_atencion.desactivar()
        self.estado = 'cerrado'
        self.save()

    def activar(self):
        self.horario_atencion.activar()
        self.estado = 'asignado'
        self.save()

class HistorialAtencion(models.Model):
    fecha = models.DateField()
    comentario = models.CharField(max_length=255, null=False, blank=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)

    def __str__(self):
        return f"Historial {self.cliente} - {self.especialista} - {self.fecha}"

    def clean(self):
        if not self.comentario:
            raise ValidationError('El comentario no puede estar vacío.')
        if len(self.comentario) > 255:
            raise ValidationError('El comentario no puede exceder los 255 caracteres.')

class Admin(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.nombre:
            print(f"Before strip: '{self.nombre}'")
            self.nombre = self.nombre.strip()
            print(f"After strip: '{self.nombre}'")
        if self.email:
            print(f"Before strip: '{self.email}'")
            self.email = self.email.strip()
            print(f"After strip: '{self.email}'")

        if not self.nombre:
            raise ValidationError('El nombre es obligatorio.')
        if not self.email:
            raise ValidationError('El email es obligatorio.')

        # Validar el formato del correo electrónico después de eliminar espacios
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError('Enter a valid email address.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Asegurar que se ejecute clean() antes de guardar
        super(Admin, self).save(*args, **kwargs)

class RelatedModel(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    related_field = models.CharField(max_length=100)
    # Otros campos necesarios

    def __str__(self):
        return self.related_field

class Notificacion(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notificación para {self.especialista.nombre} - {self.mensaje}"

    def enviar_notificacion(self, cliente):
        # Lógica para enviar notificación al cliente
        send_mail(
            'Notificación de la Clínica El Curador',
            self.mensaje,
            'from@example.com',
            [cliente.correo],
            fail_silently=False,
        )

class Calificacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField()  # calificación del 1 al 5

    def clean(self):
        if not 1 <= self.calificacion <= 5:
            raise ValidationError('La calificación debe estar entre 1 y 5.')
        if not self.comentario:
            raise ValidationError('El comentario no puede estar vacío.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Validar antes de guardar
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Calificación de {self.cliente} para {self.especialista}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')), null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
