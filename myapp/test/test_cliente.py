from django.forms import ValidationError
import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from myapp.models import Cliente
from datetime import date

@pytest.mark.django_db
def test_cliente_creation():
    # Prueba para verificar la creación de un cliente con todos los campos necesarios
    user = User.objects.create_user(username='abcd', email='abcd@gmail.com', password='12345')
    cliente = Cliente.objects.create(
        nombre='abcde',
        apellido_paterno='abcde',
        apellido_materno='abcde',
        correo='abcde@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='12345678-9',
        telefono='912345678',
        usuario=user,
        activo=True
    )

    assert cliente.usuario == user
    assert cliente.nombre == 'abcde'
    assert cliente.apellido_paterno == 'abcde'
    assert cliente.correo == 'abcde@example.com'
    assert cliente.run == '12345678-9'
    assert cliente.telefono == '912345678'
    assert cliente.activo is True

@pytest.mark.django_db
def test_cliente_email_unique():
    # Prueba para asegurar que el correo del cliente sea único
    user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='12345')
    cliente1 = Cliente.objects.create(
        nombre='cliente1',
        apellido_paterno='apellido1',
        apellido_materno='apellido1',
        correo='cliente@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='11111111-1',
        telefono='911111111',
        usuario=user1,
        activo=True
    )
    user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='12345')
    
    with pytest.raises(IntegrityError):
        Cliente.objects.create(
            nombre='cliente2',
            apellido_paterno='apellido2',
            apellido_materno='apellido2',
            correo='cliente@example.com',  # Mismo correo que cliente1
            fecha_nacimiento=date(1992, 2, 2),
            run='22222222-2',
            telefono='922222222',
            usuario=user2,
            activo=True
        )

@pytest.mark.django_db
def test_cliente_run_unique():
    # Prueba para asegurar que el RUN del cliente sea único
    user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='12345')
    cliente1 = Cliente.objects.create(
        nombre='cliente1',
        apellido_paterno='apellido1',
        apellido_materno='apellido1',
        correo='cliente1@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='11111111-1',
        telefono='911111111',
        usuario=user1,
        activo=True
    )
    user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='12345')
    
    with pytest.raises(IntegrityError):
        Cliente.objects.create(
            nombre='cliente2',
            apellido_paterno='apellido2',
            apellido_materno='apellido2',
            correo='cliente2@example.com',
            fecha_nacimiento=date(1992, 2, 2),
            run='11111111-1',  # Mismo RUN que cliente1
            telefono='922222222',
            usuario=user2,
            activo=True
        )

@pytest.mark.django_db
def test_cliente_inactive():
    # Prueba para crear un cliente inactivo
    user = User.objects.create_user(username='inactiveuser', email='inactiveuser@gmail.com', password='12345')
    cliente = Cliente.objects.create(
        nombre='Inactive',
        apellido_paterno='User',
        apellido_materno='Test',
        correo='inactiveuser@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='33333333-3',
        telefono='933333333',
        usuario=user,
        activo=False
    )

    assert cliente.activo is False

@pytest.mark.django_db
def test_cliente_update():
    # Prueba para actualizar los datos de un cliente
    user = User.objects.create_user(username='updateuser', email='updateuser@gmail.com', password='12345')
    cliente = Cliente.objects.create(
        nombre='Update',
        apellido_paterno='Test',
        apellido_materno='User',
        correo='updateuser@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='44444444-4',
        telefono='944444444',
        usuario=user,
        activo=True
    )

    cliente.nombre = 'Updated'
    cliente.save()

    updated_cliente = Cliente.objects.get(id=cliente.id)
    assert updated_cliente.nombre == 'Updated'

@pytest.mark.django_db
def test_cliente_nombre_max_length():
    # Prueba para asegurar que el nombre del cliente no exceda la longitud máxima permitida
    user = User.objects.create_user(username='longnameuser', email='longnameuser@gmail.com', password='12345')
    long_name = 'a' * 101  # Asumiendo que max_length es 100
    cliente = Cliente(
        nombre=long_name,
        apellido_paterno='Apellido',
        apellido_materno='Apellido',
        correo='longname@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='55555555-5',
        telefono='955555555',
        usuario=user,
        activo=True
    )
    with pytest.raises(ValidationError):
        cliente.full_clean()
        cliente.save()

@pytest.mark.django_db
def test_cliente_invalid_email():
    # Prueba para asegurar que no se permita un correo electrónico inválido
    user = User.objects.create_user(username='invalidemailuser', email='invalidemailuser@gmail.com', password='12345')
    cliente = Cliente(
        nombre='Invalid',
        apellido_paterno='Email',
        apellido_materno='Test',
        correo='invalid-email',  # Formato de correo inválido
        fecha_nacimiento=date(1990, 1, 1),
        run='66666666-6',
        telefono='966666666',
        usuario=user,
        activo=True
    )
    with pytest.raises(ValidationError):
        cliente.full_clean()
        cliente.save()

@pytest.mark.django_db
def test_cliente_empty_fields():
    # Prueba para asegurar que no se permitan campos vacíos
    user = User.objects.create_user(username='emptyfieldsuser', email='emptyfieldsuser@gmail.com', password='12345')
    cliente = Cliente(
        nombre='',
        apellido_paterno='',
        apellido_materno='',
        correo='emptyfields@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='77777777-7',
        telefono='977777777',
        usuario=user,
        activo=True
    )
    with pytest.raises(ValidationError):
        cliente.full_clean()
        cliente.save()

@pytest.mark.django_db
def test_cliente_duplicate_telefono():
    # Prueba para asegurar que el teléfono del cliente sea único
    user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='12345')
    Cliente.objects.create(
        nombre='Cliente1',
        apellido_paterno='Apellido1',
        apellido_materno='Apellido1',
        correo='cliente1@example.com',
        fecha_nacimiento=date(1990, 1, 1),
        run='88888888-8',
        telefono='988888888',
        usuario=user1,
        activo=True
    )
    user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='12345')
    with pytest.raises(IntegrityError):
        Cliente.objects.create(
            nombre='Cliente2',
            apellido_paterno='Apellido2',
            apellido_materno='Apellido2',
            correo='cliente2@example.com',
            fecha_nacimiento=date(1992, 2, 2),
            run='99999999-9',
            telefono='988888888',  # Mismo teléfono que cliente1
            usuario=user2,
            activo=True
        )