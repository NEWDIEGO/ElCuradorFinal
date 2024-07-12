from django.forms import ValidationError
import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from myapp.models import Especialista, Especialidad
from datetime import date

@pytest.mark.django_db
def test_especialista_creation():
    # Prueba para verificar la creación de un especialista con todos los campos necesarios
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='especialista', email='especialista@gmail.com', password='password123')
    especialista = Especialista.objects.create(
        usuario=user,
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

    assert especialista.usuario == user
    assert especialista.run == '98765432-1'
    assert especialista.nombre == 'Especialista'
    assert especialista.apellido_paterno == 'ApellidoP'
    assert especialista.correo == 'especialista@example.com'
    assert especialista.telefono == '987654321'
    assert especialista.especialidad == especialidad

@pytest.mark.django_db
def test_especialista_email_unique():
    # Prueba para asegurar que el correo del especialista sea único
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='12345')
    especialista1 = Especialista.objects.create(
        usuario=user1,
        run='11111111-1',
        nombre='Especialista1',
        apellido_paterno='Apellido1',
        apellido_materno='Apellido1',
        correo='especialista@example.com',
        telefono='911111111',
        fecha_nacimiento=date(1980, 1, 1),
        genero='M',
        especialidad=especialidad
    )
    user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='12345')
    
    with pytest.raises(IntegrityError):
        Especialista.objects.create(
            usuario=user2,
            run='22222222-2',
            nombre='Especialista2',
            apellido_paterno='Apellido2',
            apellido_materno='Apellido2',
            correo='especialista@example.com',  # Mismo correo que especialista1
            telefono='922222222',
            fecha_nacimiento=date(1982, 2, 2),
            genero='F',
            especialidad=especialidad
        )

@pytest.mark.django_db
def test_especialista_run_unique():
    # Prueba para asegurar que el RUN del especialista sea único
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='12345')
    especialista1 = Especialista.objects.create(
        usuario=user1,
        run='11111111-1',
        nombre='Especialista1',
        apellido_paterno='Apellido1',
        apellido_materno='Apellido1',
        correo='especialista1@example.com',
        telefono='911111111',
        fecha_nacimiento=date(1980, 1, 1),
        genero='M',
        especialidad=especialidad
    )
    user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='12345')
    
    with pytest.raises(IntegrityError):
        Especialista.objects.create(
            usuario=user2,
            run='11111111-1',  # Mismo RUN que especialista1
            nombre='Especialista2',
            apellido_paterno='Apellido2',
            apellido_materno='Apellido2',
            correo='especialista2@example.com',
            telefono='922222222',
            fecha_nacimiento=date(1982, 2, 2),
            genero='F',
            especialidad=especialidad
        )

@pytest.mark.django_db
def test_especialista_inactive():
    # Prueba para crear un especialista inactivo
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='inactiveespecialista', email='inactiveespecialista@gmail.com', password='12345')
    especialista = Especialista.objects.create(
        usuario=user,
        run='33333333-3',
        nombre='Inactive',
        apellido_paterno='Especialista',
        apellido_materno='Test',
        correo='inactiveespecialista@example.com',
        telefono='933333333',
        fecha_nacimiento=date(1990, 1, 1),
        genero='M',
        especialidad=especialidad
    )

    especialista.usuario.is_active = False
    especialista.usuario.save()

    updated_especialista = Especialista.objects.get(id=especialista.id)
    assert updated_especialista.usuario.is_active is False

@pytest.mark.django_db
def test_especialista_update():
    # Prueba para actualizar los datos de un especialista
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='updateespecialista', email='updateespecialista@gmail.com', password='12345')
    especialista = Especialista.objects.create(
        usuario=user,
        run='44444444-4',
        nombre='Update',
        apellido_paterno='Especialista',
        apellido_materno='User',
        correo='updateespecialista@example.com',
        telefono='944444444',
        fecha_nacimiento=date(1990, 1, 1),
        genero='M',
        especialidad=especialidad
    )

    especialista.nombre = 'Updated'
    especialista.save()

    updated_especialista = Especialista.objects.get(id=especialista.id)
    assert updated_especialista.nombre == 'Updated'

@pytest.mark.django_db
def test_especialista_invalid_email_format():
    # Prueba para asegurar que no se permita un correo electrónico inválido para el especialista
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='invalidemailuser', email='invalidemailuser@gmail.com', password='password123')
    especialista = Especialista(
        usuario=user,
        run='98765432-9',
        nombre='InvalidEmail',
        apellido_paterno='Especialista',
        apellido_materno='Test',
        correo='invalid-email',
        telefono='987654321',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    with pytest.raises(ValidationError):
        especialista.full_clean()

@pytest.mark.django_db
def test_especialista_creation_without_nombre():
    # Prueba para asegurar que no se pueda crear un especialista sin nombre
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='nonameuser', email='nonameuser@gmail.com', password='password123')
    especialista = Especialista(
        usuario=user,
        run='98765432-8',
        nombre='',
        apellido_paterno='Especialista',
        apellido_materno='Test',
        correo='nonameuser@example.com',
        telefono='987654322',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    with pytest.raises(ValidationError):
        especialista.full_clean()

@pytest.mark.django_db
def test_especialista_nombre_max_length():
    # Prueba para asegurar que el nombre del especialista no exceda la longitud máxima permitida
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='longnameuser', email='longnameuser@gmail.com', password='password123')
    especialista = Especialista(
        usuario=user,
        run='98765432-7',
        nombre='A' * 51,  # Suponiendo que la longitud máxima es 50
        apellido_paterno='Especialista',
        apellido_materno='Test',
        correo='longnameuser@example.com',
        telefono='987654323',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    with pytest.raises(ValidationError):
        especialista.full_clean()

@pytest.mark.django_db
def test_especialista_creation_without_apellido_paterno():
    # Prueba para asegurar que no se pueda crear un especialista sin apellido paterno
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user = User.objects.create_user(username='noapellidopaterno', email='noapellidopaterno@gmail.com', password='password123')
    especialista = Especialista(
        usuario=user,
        run='98765432-6',
        nombre='NoApellidoPaterno',
        apellido_paterno='',
        apellido_materno='Test',
        correo='noapellidopaterno@example.com',
        telefono='987654324',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    with pytest.raises(ValidationError):
        especialista.full_clean()

@pytest.mark.django_db
def test_especialista_duplicate_run():
    # Prueba para asegurar que el RUN del especialista sea único
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='12345')
    especialista1 = Especialista.objects.create(
        usuario=user1,
        run='11111111-1',
        nombre='Especialista1',
        apellido_paterno='Apellido1',
        apellido_materno='Apellido1',
        correo='especialista1@example.com',
        telefono='911111111',
        fecha_nacimiento=date(1980, 1, 1),
        genero='M',
        especialidad=especialidad
    )
    user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='12345')
    
    with pytest.raises(IntegrityError):
        Especialista.objects.create(
            usuario=user2,
            run='11111111-1',  # Mismo RUN que especialista1
            nombre='Especialista2',
            apellido_paterno='Apellido2',
            apellido_materno='Apellido2',
            correo='especialista2@example.com',
            telefono='922222222',
            fecha_nacimiento=date(1982, 2, 2),
            genero='F',
            especialidad=especialidad
        )