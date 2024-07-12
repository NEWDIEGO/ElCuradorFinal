import pytest
from django.contrib.auth.models import User
from myapp.models import Especialidad, Especialista, Pago
from datetime import date
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_pago_creation():
    # Prueba para verificar la creación de un pago con todos los campos completos
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    assert pago.numero_reserva == 1234
    assert pago.fecha == date(2024, 7, 10)
    assert pago.costo == 5000.00
    assert pago.especialista == especialista

@pytest.mark.django_db
def test_pago_update():
    # Prueba para actualizar el costo de un pago
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    pago.costo = 2000.00
    pago.save()

    updated_pago = Pago.objects.get(id=pago.id)
    assert updated_pago.costo == 2000.00

@pytest.mark.django_db
def test_pago_deletion():
    # Prueba para eliminar un pago
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    pago_id = pago.id
    pago.delete()

    with pytest.raises(Pago.DoesNotExist):
        Pago.objects.get(id=pago_id)

@pytest.mark.django_db
def test_pago_default_cost():
    # Prueba para verificar la creación de un pago con el costo por defecto
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        especialista=especialista
    )

    assert pago.costo == 5000.00  # Default cost

@pytest.mark.django_db
def test_pago_invalid_data():
    # Prueba para verificar la validación de datos inválidos en un pago
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
    
    # Invalid date
    pago = Pago(
        numero_reserva=1234,
        fecha='invalid-date',  # Invalid date
        costo=5000.00,
        especialista=especialista
    )
    with pytest.raises(ValidationError) as excinfo:
        pago.full_clean()  # Ejecuta la validación manualmente
    assert 'Fecha inválida.' in str(excinfo.value)
    
    # Invalid cost
    pago = Pago(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo='invalid-cost',  # Invalid cost
        especialista=especialista
    )
    with pytest.raises(ValidationError) as excinfo:
        pago.full_clean()  # Ejecuta la validación manualmente
    assert 'El costo debe ser uno de los valores permitidos.' in str(excinfo.value)

@pytest.mark.django_db
def test_pago_especialista_relation():
    # Prueba para verificar la relación entre el pago y el especialista
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    assert pago.especialista == especialista

@pytest.mark.django_db
def test_pago_find_by_date():
    # Prueba para encontrar pagos por fecha
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
    pago1 = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )
    pago2 = Pago.objects.create(
        numero_reserva=1235,
        fecha=date(2024, 7, 11),
        costo=2000.00,
        especialista=especialista
    )

    pagos = Pago.objects.filter(fecha=date(2024, 7, 10))
    assert len(pagos) == 1
    assert pagos[0] == pago1

@pytest.mark.django_db
def test_pago_creation_without_especialista():
    # Prueba para asegurar que no se pueda crear un pago sin especialista
    with pytest.raises(IntegrityError):
        Pago.objects.create(
            numero_reserva=1234,
            fecha=date(2024, 7, 10),
            costo=5000.00,
            especialista=None  # No especialista
        )

@pytest.mark.django_db
def test_list_all_pagos():
    # Prueba para listar todos los pagos
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
    Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )
    Pago.objects.create(
        numero_reserva=1235,
        fecha=date(2024, 7, 11),
        costo=2000.00,
        especialista=especialista
    )

    pagos = Pago.objects.all()
    assert len(pagos) == 2

@pytest.mark.django_db
def test_optional_fields():
    # Prueba para verificar la creación de un pago con campos opcionales y por defecto
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        especialista=especialista
    )

    assert pago.costo == 5000.00  # Default cost

@pytest.mark.django_db
def test_filter_and_order_pagos():
    # Prueba para filtrar y ordenar pagos
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
    Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )
    Pago.objects.create(
        numero_reserva=1235,
        fecha=date(2024, 7, 11),
        costo=2000.00,
        especialista=especialista
    )

    pagos = Pago.objects.filter(costo__gt=1000.00).order_by('fecha')
    assert len(pagos) == 2
    assert pagos[0].numero_reserva == 1234
    assert pagos[1].numero_reserva == 1235

@pytest.mark.django_db
def test_update_pago_fecha():
    # Prueba para actualizar la fecha de un pago
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    pago.fecha = date(2024, 8, 10)
    pago.save()

    updated_pago = Pago.objects.get(id=pago.id)
    assert updated_pago.fecha == date(2024, 8, 10)

@pytest.mark.django_db
def test_filter_pagos_by_especialista():
    # Prueba para filtrar pagos por especialista
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    user_especialista1 = User.objects.create_user(username='especialista1', email='especialista1@gmail.com', password='password123')
    especialista1 = Especialista.objects.create(
        usuario=user_especialista1,
        run='98765432-1',
        nombre='Especialista1',
        apellido_paterno='ApellidoP1',
        apellido_materno='ApellidoM1',
        correo='especialista1@example.com',
        telefono='9876543211',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    user_especialista2 = User.objects.create_user(username='especialista2', email='especialista2@gmail.com', password='password123')
    especialista2 = Especialista.objects.create(
        usuario=user_especialista2,
        run='98765432-2',
        nombre='Especialista2',
        apellido_paterno='ApellidoP2',
        apellido_materno='ApellidoM2',
        correo='especialista2@example.com',
        telefono='9876543212',
        fecha_nacimiento=date(1980, 5, 15),
        genero='M',
        especialidad=especialidad
    )
    Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista1
    )
    Pago.objects.create(
        numero_reserva=1235,
        fecha=date(2024, 7, 11),
        costo=2000.00,
        especialista=especialista2
    )

    pagos_especialista1 = Pago.objects.filter(especialista=especialista1)
    assert len(pagos_especialista1) == 1
    assert pagos_especialista1[0].especialista == especialista1

@pytest.mark.django_db
def test_update_numero_reserva():
    # Prueba para actualizar el número de reserva de un pago
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    pago.numero_reserva = 4321
    pago.save()

    updated_pago = Pago.objects.get(id=pago.id)
    assert updated_pago.numero_reserva == 4321

@pytest.mark.django_db
def test_find_pago_by_numero_reserva():
    # Prueba para encontrar un pago por número de reserva
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
    Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    pago = Pago.objects.get(numero_reserva=1234)
    assert pago.numero_reserva == 1234
    assert pago.costo == 5000.00

@pytest.mark.django_db
def test_pago_negative_cost():
    # Prueba para asegurar que no se pueda crear un pago con costo negativo
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
        pago = Pago(
            numero_reserva=1234,
            fecha=date(2024, 7, 10),
            costo=-5000.00,  # Negative cost
            especialista=especialista
        )
        pago.full_clean()  # Ejecuta la validación manualmente
        pago.save()

@pytest.mark.django_db
def test_update_multiple_fields():
    # Prueba para actualizar múltiples campos de un pago
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    pago.numero_reserva = 4321
    pago.fecha = date(2024, 8, 10)
    pago.costo = 2500.00
    pago.save()

    updated_pago = Pago.objects.get(id=pago.id)
    assert updated_pago.numero_reserva == 4321
    assert updated_pago.fecha == date(2024, 8, 10)
    assert updated_pago.costo == 2500.00

@pytest.mark.django_db
def test_create_pago_with_minimum_fields():
    # Prueba para crear un pago con el número mínimo de campos
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        especialista=especialista
    )

    assert pago.numero_reserva == 1234
    assert pago.fecha == date(2024, 7, 10)
    assert pago.costo == 5000.00  # Default cost
    assert pago.especialista == especialista

@pytest.mark.django_db
def test_delete_nonexistent_pago():
    # Prueba para intentar eliminar un pago inexistente
    with pytest.raises(Pago.DoesNotExist):
        Pago.objects.get(id=9999).delete()

@pytest.mark.django_db
def test_create_pago_with_same_reserva_number():
    # Prueba para asegurar que no se puedan crear pagos con el mismo número de reserva
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
    Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    with pytest.raises(IntegrityError):
        Pago.objects.create(
            numero_reserva=1234,  # Same reserva number
            fecha=date(2024, 7, 11),
            costo=2000.00,
            especialista=especialista
        )

@pytest.mark.django_db
def test_create_pago_with_future_date():
    # Prueba para crear un pago con una fecha futura
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2030, 7, 10),  # Future date
        costo=5000.00,
        especialista=especialista
    )

    assert pago.fecha == date(2030, 7, 10)

@pytest.mark.django_db
def test_create_pago_without_cost():
    # Prueba para crear un pago sin especificar el costo, usando el costo por defecto
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        especialista=especialista
    )

    assert pago.costo == 5000.00  # Default cost

@pytest.mark.django_db
def test_pago_str_method():
    # Prueba para verificar el método __str__ de la clase Pago
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,
        especialista=especialista
    )

    assert str(pago) == f'Pago {pago.numero_reserva} - {pago.especialista}'

@pytest.mark.django_db
def test_pago_full_clean():
    # Prueba para verificar la validación completa de un pago
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

    pago = Pago(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=5000.00,  # Use valid cost from COSTOS
        especialista=especialista
    )
    pago.full_clean()
    pago.save()

    fetched_pago = Pago.objects.get(numero_reserva=1234)
    assert fetched_pago == pago

@pytest.mark.django_db
def test_pago_validation():
    # Prueba para verificar la validación de un pago con costo negativo
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
    
    pago = Pago(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        costo=-5000.00,  # Negative cost to trigger validation
        especialista=especialista
    )
    with pytest.raises(ValidationError):
        pago.full_clean()

@pytest.mark.django_db
def test_pago_creation_with_minimum_data():
    # Prueba para crear un pago con el número mínimo de datos requeridos
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
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        especialista=especialista
    )
    
    assert pago.costo == 5000.00  # Default cost
    assert pago.numero_reserva == 1234
    assert pago.fecha == date(2024, 7, 10)
    assert pago.especialista == especialista

@pytest.mark.django_db
def test_optional_fields_and_defaults():
    # Prueba para verificar la creación de un pago con campos opcionales y valores por defecto
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
    
    pago = Pago.objects.create(
        numero_reserva=1234,
        fecha=date(2024, 7, 10),
        especialista=especialista
    )
    
    assert pago.costo == 5000.00  # Default cost
    assert pago.fecha == date(2024, 7, 10)
    assert pago.numero_reserva == 1234
    assert pago.especialista == especialista
