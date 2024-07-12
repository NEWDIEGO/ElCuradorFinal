import pytest
from django.contrib.auth.models import User
from myapp.models import Especialidad, Especialista, Notificacion
from datetime import date
from django.db.utils import IntegrityError
from django.core import mail

@pytest.mark.django_db
def test_notificacion_creation():
    # Prueba para verificar la creación de una notificación con mensaje vacío y mensaje de longitud máxima
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
    mensaje_vacio = ''
    mensaje_max_longitud = 'a' * 255

    notificacion_vacia = Notificacion.objects.create(
        mensaje=mensaje_vacio,
        especialista=especialista
    )
    notificacion_max = Notificacion.objects.create(
        mensaje=mensaje_max_longitud,
        especialista=especialista
    )

    assert notificacion_vacia.mensaje == mensaje_vacio
    assert notificacion_max.mensaje == mensaje_max_longitud
    assert notificacion_vacia.leido is False
    assert notificacion_max.leido is False
    assert notificacion_vacia.especialista == especialista
    assert notificacion_max.especialista == especialista

@pytest.mark.django_db
def test_notificacion_creation_with_different_message_and_state():
    # Prueba para crear una notificación con un mensaje y estado de leído diferentes
    especialidad = Especialidad.objects.create(nombre='Dental')
    user_especialista = User.objects.create_user(username='neuro', email='neuro@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user_especialista,
        run='87654321-0',
        nombre='Neuro',
        apellido_paterno='ApellidoN',
        apellido_materno='ApellidoM',
        correo='neuro@example.com',
        telefono='876543210',
        fecha_nacimiento=date(1985, 7, 20),
        genero='F',
        especialidad=especialidad
    )
    notificacion = Notificacion.objects.create(
        mensaje='Su receta está lista.',
        especialista=especialista,
        leido=True
    )

    assert notificacion.mensaje == 'Su receta está lista.'
    assert notificacion.leido is True
    assert notificacion.especialista == especialista

@pytest.mark.django_db
def test_notificacion_update():
    # Prueba para actualizar el estado de una notificación a leído
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
    notificacion = Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )

    notificacion.leido = True
    notificacion.save()

    updated_notificacion = Notificacion.objects.get(id=notificacion.id)
    assert updated_notificacion.leido is True

@pytest.mark.django_db
def test_notificacion_update_message():
    # Prueba para actualizar el mensaje de una notificación
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
    notificacion = Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )

    notificacion.mensaje = 'Su cita ha sido cancelada.'
    notificacion.save()

    updated_notificacion = Notificacion.objects.get(id=notificacion.id)
    assert updated_notificacion.mensaje == 'Su cita ha sido cancelada.'

@pytest.mark.django_db
def test_notificacion_deletion():
    # Prueba para eliminar una notificación
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
    notificacion = Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )

    notificacion_id = notificacion.id
    notificacion.delete()

    with pytest.raises(Notificacion.DoesNotExist):
        Notificacion.objects.get(id=notificacion_id)

@pytest.mark.django_db
def test_notificacion_deletion_nonexistent():
    # Prueba para verificar la eliminación de una notificación inexistente
    with pytest.raises(Notificacion.DoesNotExist):
        Notificacion.objects.get(id=99999).delete()

@pytest.mark.django_db
def test_notificacion_creation_without_especialista():
    # Prueba para asegurar que no se pueda crear una notificación sin especialista
    with pytest.raises(IntegrityError):
        Notificacion.objects.create(
            mensaje='Su cita ha sido confirmada.',
            especialista=None  # No especialista
        )

@pytest.mark.django_db
def test_notificacion_creation_with_defaults():
    # Prueba para crear una notificación con valores por defecto
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
    notificacion = Notificacion.objects.create(
        mensaje='Recordatorio de cita.',
        especialista=especialista
    )

    assert notificacion.mensaje == 'Recordatorio de cita.'
    assert notificacion.leido is False

@pytest.mark.django_db
def test_list_all_notificaciones():
    # Prueba para listar todas las notificaciones
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
    Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )
    Notificacion.objects.create(
        mensaje='Su receta está lista.',
        especialista=especialista
    )

    notificaciones = Notificacion.objects.all()
    assert len(notificaciones) == 2

@pytest.mark.django_db
def test_list_notificaciones_for_especialista():
    # Prueba para listar todas las notificaciones de un especialista
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
    Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )
    Notificacion.objects.create(
        mensaje='Su receta está lista.',
        especialista=especialista
    )

    notificaciones = Notificacion.objects.filter(especialista=especialista)
    assert len(notificaciones) == 2

@pytest.mark.django_db
def test_notificacion_mensaje_largo():
    # Prueba para asegurar que se pueda crear una notificación con un mensaje largo
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
    mensaje_largo = 'Este es un mensaje muy largo para probar el límite de longitud del campo mensaje.' * 2  # Ajustar la longitud según el campo
    if len(mensaje_largo) > 255:
        mensaje_largo = mensaje_largo[:255]  # Ajustar al tamaño máximo permitido

    notificacion = Notificacion.objects.create(
        mensaje=mensaje_largo,
        especialista=especialista
    )

    assert notificacion.mensaje == mensaje_largo

@pytest.mark.django_db
def test_notificacion_mark_as_unread():
    # Prueba para marcar una notificación como no leída
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
    notificacion = Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista,
        leido=True
    )

    notificacion.leido = False
    notificacion.save()

    updated_notificacion = Notificacion.objects.get(id=notificacion.id)
    assert updated_notificacion.leido is False

@pytest.mark.django_db
def test_enviar_notificacion():
    # Prueba para enviar una notificación por correo electrónico
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
    user_cliente = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='password123')
    cliente = Especialista.objects.create(
        usuario=user_cliente,
        run='12345678-9',
        nombre='Cliente',
        apellido_paterno='ApellidoC',
        apellido_materno='ApellidoM',
        correo='cliente@example.com',
        telefono='123456789',
        fecha_nacimiento=date(1990, 1, 1),
        genero='F',
        especialidad=especialidad
    )
    notificacion = Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )

    notificacion.enviar_notificacion(cliente)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Notificación de la Clínica El Curador'
    assert mail.outbox[0].body == 'Su cita ha sido confirmada.'
    assert mail.outbox[0].to == [cliente.correo]

@pytest.mark.django_db
def test_notificacion_min_max_values():
    # Prueba para crear notificaciones con valores mínimos y máximos permitidos
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
    notificacion = Notificacion.objects.create(
        mensaje='',
        especialista=especialista
    )

    assert notificacion.mensaje == ''
    assert notificacion.leido is False
    assert notificacion.especialista == especialista

    long_message = 'a' * 255
    notificacion = Notificacion.objects.create(
        mensaje=long_message,
        especialista=especialista
    )

    assert notificacion.mensaje == long_message
    assert notificacion.leido is False
    assert notificacion.especialista == especialista

@pytest.mark.django_db
def test_notificacion_fields_validation():
    # Prueba para asegurar que los campos de la notificación sean válidos
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

    with pytest.raises(IntegrityError):
        Notificacion.objects.create(
            mensaje='Su cita ha sido confirmada.',
            especialista=None
        )

@pytest.mark.django_db
def test_notificacion_str():
    # Prueba para verificar la representación en cadena de una notificación
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
    notificacion = Notificacion.objects.create(
        mensaje='Su cita ha sido confirmada.',
        especialista=especialista
    )

    assert str(notificacion) == f"Notificación para {especialista.nombre} - Su cita ha sido confirmada."
