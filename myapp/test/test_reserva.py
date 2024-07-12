import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from myapp.models import Cliente, Especialidad, Especialista, HorariosAtencion, Reserva
from datetime import date, datetime, time

@pytest.mark.django_db
def test_reserva_creation():
    # Prueba para verificar la creación de una reserva
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

    assert reserva.cliente == cliente
    assert reserva.horario_atencion == horario
    assert reserva.nro_reserva is not None

@pytest.mark.django_db
def test_reserva_update():
    # Prueba para actualizar el estado de una reserva
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

    reserva.estado = 'confirmado'
    reserva.save()

    updated_reserva = Reserva.objects.get(id=reserva.id)
    assert updated_reserva.estado == 'confirmado'

@pytest.mark.django_db
def test_reserva_cancel():
    # Prueba para cancelar una reserva
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

    reserva.cancelar()

    canceled_reserva = Reserva.objects.get(id=reserva.id)
    assert canceled_reserva.estado == 'cerrado'

@pytest.mark.django_db
def test_reserva_deletion():
    # Prueba para eliminar una reserva
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

    reserva_id = reserva.id
    reserva.delete()

    with pytest.raises(Reserva.DoesNotExist):
        Reserva.objects.get(id=reserva_id)