import pytest
from django.contrib.auth.models import User
from myapp.models import Cliente, Especialidad, Especialista, Reserva, HorariosAtencion, HistorialAtencion
from datetime import date, datetime, time
from django.utils import timezone
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_historial_atencion_creation_without_comentario():
    # Prueba para asegurar que no se pueda crear un historial de atención sin comentario
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
    historial = HistorialAtencion(
        fecha=date(2024, 7, 11),
        comentario='',  # Campo vacío
        cliente=cliente,
        especialista=especialista,
        reserva=reserva
    )
    with pytest.raises(ValidationError):
        historial.full_clean()
        historial.save()

@pytest.mark.django_db
def test_historial_atencion_update_fecha():
    # Prueba para actualizar la fecha de un historial de atención
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
    historial = HistorialAtencion.objects.create(
        fecha=date(2024, 7, 11),
        comentario='Consulta inicial',
        cliente=cliente,
        especialista=especialista,
        reserva=reserva
    )

    nueva_fecha = date(2024, 7, 12)
    historial.fecha = nueva_fecha
    historial.save()

    updated_historial = HistorialAtencion.objects.get(id=historial.id)
    assert updated_historial.fecha == nueva_fecha

@pytest.mark.django_db
def test_historial_atencion_long_comment():
    # Prueba para asegurar que no se pueda crear un historial de atención con un comentario demasiado largo
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
    long_comment = 'a' * 256  # Un comentario más largo que 255 caracteres
    historial = HistorialAtencion(
        fecha=date(2024, 7, 11),
        comentario=long_comment,  # Comentario largo
        cliente=cliente,
        especialista=especialista,
        reserva=reserva
    )
    with pytest.raises(ValidationError):
        historial.full_clean()
        historial.save()

@pytest.mark.django_db
def test_historial_atencion_creation_past_date():
    # Prueba para crear un historial de atención con una fecha pasada
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
    past_date = date(2023, 7, 10)
    historial = HistorialAtencion.objects.create(
        fecha=past_date,
        comentario='Consulta inicial en el pasado',
        cliente=cliente,
        especialista=especialista,
        reserva=reserva
    )

    assert historial.fecha == past_date

@pytest.mark.django_db
def test_historial_atencion_creation_future_date():
    # Prueba para crear un historial de atención con una fecha futura
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
    future_date = date(2025, 7, 10)
    historial = HistorialAtencion.objects.create(
        fecha=future_date,
        comentario='Consulta inicial en el futuro',
        cliente=cliente,
        especialista=especialista,
        reserva=reserva
    )

    assert historial.fecha == future_date