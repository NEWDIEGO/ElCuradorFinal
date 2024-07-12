import pytest
from django.core.exceptions import ValidationError
from myapp.models import Especialidad

@pytest.mark.django_db
def test_especialidad_creation():
    # Prueba para verificar la creación de una especialidad
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    assert especialidad.nombre == 'Medicina General'

@pytest.mark.django_db
def test_especialidad_update():
    # Prueba para actualizar el nombre de una especialidad
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    especialidad.nombre = 'Dental'
    especialidad.save()
    updated_especialidad = Especialidad.objects.get(id=especialidad.id)
    assert updated_especialidad.nombre == 'Dental'

@pytest.mark.django_db
def test_especialidad_deletion():
    # Prueba para eliminar una especialidad
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    especialidad_id = especialidad.id
    especialidad.delete()
    with pytest.raises(Especialidad.DoesNotExist):
        Especialidad.objects.get(id=especialidad_id)

@pytest.mark.django_db
def test_especialidad_nombre_blank():
    # Prueba para asegurar que no se permita un nombre de especialidad en blanco
    especialidad = Especialidad(nombre='')
    with pytest.raises(ValidationError) as excinfo:
        especialidad.full_clean()
        especialidad.save()
    assert 'This field cannot be blank.' in str(excinfo.value)

@pytest.mark.django_db
def test_especialidad_nombre_max_length():
    # Prueba para asegurar que el nombre de la especialidad no exceda la longitud máxima permitida
    long_name = 'A' * 51  # Asumiendo que max_length es 50
    especialidad = Especialidad(nombre=long_name)
    with pytest.raises(ValidationError) as excinfo:
        especialidad.full_clean()
        especialidad.save()
    assert 'Ensure this value has at most 50 characters' in str(excinfo.value)

@pytest.mark.django_db
def test_especialidad_duplicate_nombre():
    # Prueba para asegurar que el nombre de la especialidad sea único
    Especialidad.objects.create(nombre='Medicina General')
    duplicate_especialidad = Especialidad(nombre='Medicina General')
    with pytest.raises(ValidationError):
        duplicate_especialidad.full_clean()
        duplicate_especialidad.save()

@pytest.mark.django_db
def test_especialidad_partial_update():
    # Prueba para actualizar parcialmente el nombre de una especialidad
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    especialidad.nombre = 'psicologia'
    especialidad.save()
    updated_especialidad = Especialidad.objects.get(id=especialidad.id)
    assert updated_especialidad.nombre == 'psicologia'

@pytest.mark.django_db
def test_especialidad_str_method():
    # Prueba para verificar el método __str__ de la especialidad
    especialidad = Especialidad.objects.create(nombre='Medicina General')
    assert str(especialidad) == 'Medicina General'

@pytest.mark.django_db
def test_especialidad_creation_with_special_characters():
    # Prueba para crear una especialidad con caracteres especiales en el nombre
    special_name = 'Medicina General!@#$%'
    especialidad = Especialidad.objects.create(nombre=special_name)
    assert especialidad.nombre == special_name

@pytest.mark.django_db
def test_especialidad_nombre_strip_whitespace():
    # Prueba para asegurar que se eliminen los espacios en blanco en el nombre de la especialidad
    especialidad = Especialidad(nombre='   Medicina General   ')
    especialidad.full_clean()
    especialidad.save()
    assert especialidad.nombre == 'Medicina General'