import pytest
from django.contrib.auth.models import User
from myapp.models import Cliente, Especialidad, Especialista, Reserva, Calificacion, HorariosAtencion
from datetime import date, datetime, time
from django.utils import timezone
from django.core.exceptions import ValidationError

# Inhabilitar temporalmente una prueba específica
@pytest.mark.skip(reason="Inhabilitado temporalmente para ajustes")
def test_calificacion():
    # Tu código de prueba aquí
    assert False  # Esta línea es solo un ejemplo, reemplázala con tu lógica de prueba


@pytest.mark.django_db
def test_calificacion_creation():
    # Prueba para verificar la creación de una calificación con todos los campos necesarios
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    calificacion = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario='Excelente atención',
        calificacion=5
    )

    assert calificacion.cliente == cliente
    assert calificacion.especialista == especialista
    assert calificacion.reserva == reserva
    assert calificacion.comentario == 'Excelente atención'
    assert calificacion.calificacion == 5

@pytest.mark.django_db
def test_calificacion_update():
    # Prueba para actualizar los campos de una calificación existente
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    calificacion = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario='Buena atención',
        calificacion=4
    )

    calificacion.comentario = 'Excelente atención'
    calificacion.calificacion = 5
    calificacion.save()

    updated_calificacion = Calificacion.objects.get(id=calificacion.id)
    assert updated_calificacion.comentario == 'Excelente atención'
    assert updated_calificacion.calificacion == 5

@pytest.mark.django_db
def test_calificacion_deletion():
    # Prueba para eliminar una calificación existente
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    calificacion = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario='Buena atención',
        calificacion=4
    )

    calificacion_id = calificacion.id
    calificacion.delete()

    with pytest.raises(Calificacion.DoesNotExist):
        Calificacion.objects.get(id=calificacion_id)

@pytest.mark.django_db
def test_calificacion_invalid_rating():
    # Prueba para verificar que no se pueda crear una calificación con una puntuación inválida
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    
    with pytest.raises(ValidationError):
        calificacion = Calificacion(
            cliente=cliente,
            especialista=especialista,
            reserva=reserva,
            comentario='Atención regular',
            calificacion=6  # Puntuación inválida
        )
        calificacion.full_clean()  # Ejecuta la validación manualmente
        calificacion.save()

@pytest.mark.django_db
def test_calificacion_update_invalid_rating():
    # Prueba para verificar que no se pueda actualizar una calificación con una puntuación inválida
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    calificacion = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario='Buena atención',
        calificacion=4
    )

    with pytest.raises(ValidationError):
        calificacion.calificacion = 6  # Puntuación inválida
        calificacion.full_clean()  # Ejecuta la validación manualmente
        calificacion.save()

@pytest.mark.django_db
def test_calificacion_empty_comment():
    # Prueba para verificar que no se pueda crear una calificación con un comentario vacío
    from django.core.exceptions import ValidationError

    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )

    with pytest.raises(ValidationError) as excinfo:
        calificacion = Calificacion(
            cliente=cliente,
            especialista=especialista,
            reserva=reserva,
            comentario='',  # Campo comentario vacío
            calificacion=4
        )
        calificacion.full_clean()  # Ejecuta la validación manualmente

    assert 'This field cannot be blank.' in str(excinfo.value)
    assert 'El comentario no puede estar vacío.' in str(excinfo.value)

@pytest.mark.django_db
def test_calificacion_min_max_values():
    # Prueba para verificar que las calificaciones pueden tener valores mínimos y máximos válidos
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    
    # Probar con el valor mínimo permitido
    calificacion_min = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario='Mala atención',
        calificacion=1
    )
    assert calificacion_min.calificacion == 1
    
    # Probar con el valor máximo permitido
    calificacion_max = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario='Excelente atención',
        calificacion=5
    )
    assert calificacion_max.calificacion == 5

@pytest.mark.django_db
def test_calificacion_without_comment():
    # Prueba para verificar que no se pueda crear una calificación sin comentario
    from django.core.exceptions import ValidationError

    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    
    with pytest.raises(ValidationError) as excinfo:
        calificacion = Calificacion.objects.create(
            cliente=cliente,
            especialista=especialista,
            reserva=reserva,
            comentario='',  # Campo comentario vacío
            calificacion=4
        )
        calificacion.full_clean()  # Ejecuta la validación manualmente

    assert 'El comentario no puede estar vacío.' in str(excinfo.value)

@pytest.mark.django_db
def test_calificacion_long_comment():
    # Prueba para verificar que una calificación con un comentario largo se guarda correctamente
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    horario = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(10, 0),
        duracion_cita=30,
        especialista=especialista
    )
    agendar_hora = timezone.make_aware(datetime(2024, 7, 10, 9, 0), timezone.get_current_timezone())
    reserva = Reserva.objects.create(
        agendar_hora=agendar_hora,
        cliente=cliente,
        horario_atencion=horario
    )
    
    long_comment = 'a' * 1000  # Comentario extremadamente largo
    calificacion = Calificacion.objects.create(
        cliente=cliente,
        especialista=especialista,
        reserva=reserva,
        comentario=long_comment,
        calificacion=4
    )

    assert calificacion.comentario == long_comment
    assert calificacion.calificacion == 4

@pytest.mark.django_db
def test_calificacion_without_reserva():
    # Prueba para verificar que no se pueda crear una calificación sin una reserva asociada
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Cliente.objects.create(
        nombre='Cliente',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user_cliente,
        activo=True
    )
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='98765432-1',
        nombre='Especialista',
        apellido_paterno='ApellidoP',
        apellido_materno='ApellidoM',
        correo='especialista@example.com',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )

    with pytest.raises(ValidationError):
        calificacion = Calificacion.objects.create(
            cliente=cliente,
            especialista=especialista,
            reserva=None,
            comentario='Buena atención',
            calificacion=4
        )
        calificacion.full_clean()  # Ejecuta la validación manualmente
        calificacion.save()

