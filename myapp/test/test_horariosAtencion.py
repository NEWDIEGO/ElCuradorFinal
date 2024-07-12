import pytest
from django.contrib.auth.models import User
from myapp.models import Especialidad, Especialista, HorariosAtencion
from datetime import date, time
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_horarios_atencion_creation():
    # Prueba para verificar la creación de un horario de atención con todos los campos necesarios
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

    assert horario.dia_semana == 'Lunes'
    assert horario.fecha == date(2024, 7, 10)
    assert horario.hora_inicio == time(9, 0)
    assert horario.hora_fin == time(10, 0)
    assert horario.duracion_cita == 30
    assert horario.especialista == especialista
    assert horario.activo is True

@pytest.mark.django_db
def test_horarios_atencion_update():
    # Prueba para actualizar el día de la semana de un horario de atención
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

    horario.dia_semana = 'Martes'
    horario.save()

    updated_horario = HorariosAtencion.objects.get(id=horario.id)
    assert updated_horario.dia_semana == 'Martes'

@pytest.mark.django_db
def test_horarios_atencion_cancel():
    # Prueba para cancelar un horario de atención
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

    horario.cancelar()

    canceled_horario = HorariosAtencion.objects.get(id=horario.id)
    assert canceled_horario.activo is False

@pytest.mark.django_db
def test_horarios_atencion_reagendar():
    # Prueba para reagendar un horario de atención a una nueva fecha y hora
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

    nueva_fecha = date(2024, 7, 11)
    nueva_hora_inicio = time(10, 0)
    nueva_hora_fin = time(11, 0)
    horario.proponer_reagendar(nueva_fecha, nueva_hora_inicio, nueva_hora_fin)

    reagendado_horario = HorariosAtencion.objects.get(id=horario.id)
    assert reagendado_horario.fecha == nueva_fecha
    assert reagendado_horario.hora_inicio == nueva_hora_inicio
    assert reagendado_horario.hora_fin == nueva_hora_fin

@pytest.mark.django_db
def test_horarios_atencion_deletion():
    # Prueba para eliminar un horario de atención
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

    horario_id = horario.id
    horario.delete()

    with pytest.raises(HorariosAtencion.DoesNotExist):
        HorariosAtencion.objects.get(id=horario_id)

@pytest.mark.django_db
def test_horarios_atencion_min_max_values():
    # Prueba para crear horarios de atención con valores mínimos y máximos permitidos
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
    
    # Probar con valores mínimos permitidos
    horario_min = HorariosAtencion.objects.create(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(9, 0),
        hora_fin=time(9, 30),
        duracion_cita=10,
        especialista=especialista
    )

    assert horario_min.dia_semana == 'Lunes'
    assert horario_min.fecha == date(2024, 7, 10)
    assert horario_min.hora_inicio == time(9, 0)
    assert horario_min.hora_fin == time(9, 30)
    assert horario_min.duracion_cita == 10
    assert horario_min.especialista == especialista

    # Probar con valores máximos permitidos
    horario_max = HorariosAtencion.objects.create(
        dia_semana='Viernes',
        fecha=date(2024, 12, 31),
        hora_inicio=time(8, 0),
        hora_fin=time(17, 0),
        duracion_cita=120,
        especialista=especialista
    )

    assert horario_max.dia_semana == 'Viernes'
    assert horario_max.fecha == date(2024, 12, 31)
    assert horario_max.hora_inicio == time(8, 0)
    assert horario_max.hora_fin == time(17, 0)
    assert horario_max.duracion_cita == 120
    assert horario_max.especialista == especialista

@pytest.mark.django_db
def test_horarios_atencion_invalid_data():
    # Prueba para asegurar que no se pueda crear un horario de atención con datos inválidos
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
    
    horario = HorariosAtencion(
        dia_semana='Lunes',
        fecha=date(2024, 7, 10),
        hora_inicio=time(10, 0),
        hora_fin=time(9, 0),  # Hora fin antes de hora inicio
        duracion_cita=30,
        especialista=especialista
    )
    
    with pytest.raises(ValidationError) as excinfo:
        horario.full_clean()  # Ejecuta la validación manualmente
    
    assert 'La hora de fin debe ser posterior a la hora de inicio.' in str(excinfo.value)

@pytest.mark.django_db
def test_horarios_atencion_desactivar():
    # Prueba para desactivar un horario de atención
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

    horario.desactivar()

    desactivado_horario = HorariosAtencion.objects.get(id=horario.id)
    assert desactivado_horario.activo is False

@pytest.mark.django_db
def test_horarios_atencion_activar():
    # Prueba para activar un horario de atención previamente desactivado
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
        especialista=especialista,
        activo=False
    )

    horario.activar()

    activado_horario = HorariosAtencion.objects.get(id=horario.id)
    assert activado_horario.activo is True
