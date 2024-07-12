import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from myapp.models import Admin, RelatedModel

@pytest.mark.django_db
def test_admin_creation():
    # Prueba para verificar la creación de un administrador con nombre y email
    admin = Admin.objects.create(
        nombre='Administrador',
        email='admin@example.com'
    )
    assert admin.nombre == 'Administrador'
    assert admin.email == 'admin@example.com'

@pytest.mark.django_db
def test_admin_email_unique():
    # Prueba para asegurar que el email del administrador es único
    Admin.objects.create(nombre='Admin1', email='admin@example.com')
    with pytest.raises(ValidationError) as excinfo:
        admin2 = Admin(nombre='Admin2', email='admin@example.com')
        admin2.full_clean()  # Esto debería lanzar ValidationError
        admin2.save()
    assert 'Admin with this Email already exists.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_update():
    # Prueba para actualizar el nombre del administrador
    admin = Admin.objects.create(
        nombre='Admin',
        email='admin@example.com'
    )
    admin.nombre = 'Updated Admin'
    admin.save()
    updated_admin = Admin.objects.get(id=admin.id)
    assert updated_admin.nombre == 'Updated Admin'

@pytest.mark.django_db
def test_admin_deletion():
    # Prueba para eliminar un administrador
    admin = Admin.objects.create(
        nombre='Admin',
        email='admin@example.com'
    )
    admin_id = admin.id
    admin.delete()
    with pytest.raises(Admin.DoesNotExist):
        Admin.objects.get(id=admin_id)

@pytest.mark.django_db
def test_admin_creation_without_name():
    # Prueba para verificar que no se pueda crear un administrador sin nombre
    admin = Admin(nombre='', email='admin@example.com')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El nombre es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_creation_without_email():
    # Prueba para verificar que no se pueda crear un administrador sin email
    admin = Admin(nombre='Administrador', email='')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El email es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_email_max_length():
    # Prueba para asegurar que el email no exceda la longitud máxima permitida
    max_length_email = 'a' * 243 + '@example.com'  # Esto suma 254 caracteres en total
    admin = Admin(nombre='Administrador', email=max_length_email)
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'Ensure this value has at most 254 characters' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_str_method():
    # Prueba para verificar el método __str__ del modelo Admin
    admin = Admin.objects.create(
        nombre='Administrador',
        email='admin@example.com'
    )
    assert str(admin) == 'Administrador'

@pytest.mark.django_db
def test_admin_email_invalid():
    # Prueba para validar un formato de email incorrecto
    invalid_email = 'invalid-email'
    admin = Admin(nombre='Administrador', email=invalid_email)
    with pytest.raises(ValidationError):
        admin.full_clean()
        admin.save()

@pytest.mark.django_db
def test_admin_email_valid():
    # Prueba para validar un formato de email correcto
    valid_email = 'valid_email@example.com'
    admin = Admin.objects.create(
        nombre='Administrador',
        email=valid_email
    )
    assert admin.email == valid_email

@pytest.mark.django_db
def test_admin_nombre_max_length():
    # Prueba para asegurar que el nombre no exceda la longitud máxima permitida
    long_name = 'A' * 101  # assuming max_length is 100
    admin = Admin(nombre=long_name, email='admin@example.com')
    with pytest.raises(ValidationError):
        admin.full_clean()
        admin.save()

@pytest.mark.django_db
def test_admin_nombre_valid_length():
    # Prueba para asegurar que el nombre tenga una longitud válida
    valid_name = 'A' * 100  # assuming max_length is 100
    admin = Admin.objects.create(
        nombre=valid_name,
        email='admin@example.com'
    )
    assert admin.nombre == valid_name

@pytest.mark.django_db
def test_admin_partial_update():
    # Prueba para actualizar parcialmente los datos del administrador
    admin = Admin.objects.create(
        nombre='Admin',
        email='admin@example.com'
    )
    admin.email = 'new_email@example.com'
    admin.save()
    updated_admin = Admin.objects.get(id=admin.id)
    assert updated_admin.email == 'new_email@example.com'

@pytest.mark.django_db
def test_admin_creation_with_special_characters():
    # Prueba para crear un administrador con caracteres especiales en el nombre y el email
    special_name = 'Adm!n@#$'
    special_email = 'admin_special@example.com'
    admin = Admin.objects.create(
        nombre=special_name,
        email=special_email
    )
    assert admin.nombre == special_name
    assert admin.email == special_email

@pytest.mark.django_db
def test_admin_creation_and_deletion_cascade():
    # Prueba para asegurar la eliminación en cascada de un administrador y sus relaciones
    admin = Admin.objects.create(
        nombre='Admin',
        email='admin@example.com'
    )
    related_instance = RelatedModel.objects.create(
        admin=admin,
        related_field='test'
    )
    admin_id = admin.id
    admin.delete()
    with pytest.raises(RelatedModel.DoesNotExist):
        RelatedModel.objects.get(admin=admin_id)

@pytest.mark.django_db
def test_admin_blank_email_validation():
    # Prueba para asegurar que no se permita un email en blanco
    admin = Admin(nombre='Administrador', email=' ')
    with pytest.raises(ValidationError):
        admin.full_clean()
        admin.save()

@pytest.mark.django_db
def test_admin_empty_string_name():
    # Prueba para asegurar que no se permita un nombre vacío
    admin = Admin(nombre='', email='admin@example.com')
    with pytest.raises(ValidationError):
        admin.full_clean()
        admin.save()

@pytest.mark.django_db
def test_admin_blank_name():
    # Prueba para asegurar que no se permita un nombre en blanco
    admin = Admin(nombre='', email='admin@example.com')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El nombre es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_duplicate_email():
    # Prueba para asegurar que el email sea único en la base de datos
    Admin.objects.create(nombre='Admin1', email='admin@example.com')
    with pytest.raises(ValidationError) as excinfo:
        admin2 = Admin(nombre='Admin2', email='admin@example.com')
        admin2.full_clean()  # Esto debería lanzar ValidationError
        admin2.save()
    assert 'Admin with this Email already exists.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_invalid_email_format():
    # Prueba para asegurar que el email tenga un formato válido
    invalid_email = 'invalid-email-format'
    admin = Admin(nombre='Administrador', email=invalid_email)
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'Enter a valid email address.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_partial_name_update():
    # Prueba para actualizar parcialmente el nombre del administrador
    admin = Admin.objects.create(nombre='Admin', email='admin@example.com')
    admin.nombre = 'Updated Admin'
    admin.save()
    updated_admin = Admin.objects.get(id=admin.id)
    assert updated_admin.nombre == 'Updated Admin'

@pytest.mark.django_db
def test_admin_creation_with_special_name():
    # Prueba para crear un administrador con un nombre especial
    special_name = 'Admin@#$%'
    admin = Admin.objects.create(nombre=special_name, email='admin_special@example.com')
    assert admin.nombre == special_name

@pytest.mark.django_db
def test_admin_deletion_without_related():
    # Prueba para eliminar un administrador sin eliminar su relación
    admin = Admin.objects.create(nombre='Admin', email='admin@example.com')
    related_instance = RelatedModel.objects.create(admin=admin, related_field='test')
    admin_id = admin.id
    related_instance.delete()  # Eliminar solo la instancia relacionada
    admin.delete()  # Ahora eliminar el administrador
    with pytest.raises(Admin.DoesNotExist):
        Admin.objects.get(id=admin_id)

@pytest.mark.django_db
def test_admin_name_only_spaces():
    # Prueba para asegurar que no se permita un nombre con solo espacios
    admin = Admin(nombre='   ', email='admin@example.com')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El nombre es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_email_only_spaces():
    # Prueba para asegurar que no se permita un email con solo espacios
    admin = Admin(nombre='Administrador', email='   ')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El email es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_email_without_domain():
    # Prueba para asegurar que el email tenga un dominio válido
    admin = Admin(nombre='Administrador', email='admin@')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'Enter a valid email address.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_email_without_at():
    # Prueba para asegurar que el email tenga el símbolo @
    admin = Admin(nombre='Administrador', email='adminexample.com')
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'Enter a valid email address.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_email_with_special_characters():
    # Prueba para asegurar que el email permita caracteres especiales
    special_email = 'admin!#$%&\'*+-/=?^_`{|}~@example.com'
    admin = Admin(nombre='Administrador', email=special_email)
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.email == special_email

@pytest.mark.django_db
def test_admin_nombre_max_length_exact():
    # Prueba para asegurar que el nombre tenga exactamente la longitud máxima permitida
    max_length_name = 'A' * 100  # Assuming max_length is 100
    admin = Admin(nombre=max_length_name, email='admin@example.com')
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.nombre == max_length_name

@pytest.mark.django_db
def test_admin_email_none():
    # Prueba para asegurar que el email no sea nulo
    admin = Admin(nombre='Administrador', email=None)
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El email es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_update_email_none():
    # Prueba para asegurar que el email no sea nulo al actualizar
    admin = Admin.objects.create(nombre='Administrador', email='admin@example.com')
    admin.email = None
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El email es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_update_name_none():
    # Prueba para asegurar que el nombre no sea nulo al actualizar
    admin = Admin.objects.create(nombre='Administrador', email='admin@example.com')
    admin.nombre = None
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El nombre es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_nombre_min_length():
    # Prueba para asegurar que el nombre mínimo se valide correctamente
    admin = Admin(nombre='A', email='admin@example.com')
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.nombre == 'A'

@pytest.mark.django_db
def test_admin_update_nombre_min_length():
    # Prueba para asegurar que la longitud mínima del nombre se actualice correctamente
    admin = Admin.objects.create(nombre='Administrador', email='admin@example.com')
    admin.nombre = 'A'
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.nombre == 'A'

@pytest.mark.django_db
def test_admin_email_min_length():
    # Prueba para asegurar que la longitud mínima del email se valide correctamente
    admin = Admin(nombre='Administrador', email='a@bc.de')
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.email == 'a@bc.de'

@pytest.mark.django_db
def test_admin_update_email_min_length():
    # Prueba para asegurar que la longitud mínima del email se actualice correctamente
    admin = Admin.objects.create(nombre='Administrador', email='admin@example.com')
    admin.email = 'a@bc.de'
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.email == 'a@bc.de'

@pytest.mark.django_db
def test_admin_nombre_no_whitespace():
    # Prueba para asegurar que el nombre no contenga espacios en blanco
    admin = Admin(nombre='AdminWithoutSpaces', email='admin@example.com')
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.nombre == 'AdminWithoutSpaces'

@pytest.mark.django_db
def test_admin_nombre_strip_whitespace():
    # Prueba para asegurar que los espacios en blanco en el nombre se eliminen
    admin = Admin(nombre='   Admin   ', email='admin@example.com')
    admin.full_clean()
    admin.save()
    assert admin.nombre == 'Admin'

@pytest.mark.django_db
def test_admin_nombre_with_numbers():
    # Prueba para asegurar que el nombre permita números
    admin = Admin(nombre='Admin123', email='admin123@example.com')
    try:
        admin.full_clean()
        admin.save()
    except ValidationError as e:
        assert False, f"Test failed with ValidationError: {e}"
    assert admin.nombre == 'Admin123'

@pytest.mark.django_db
def test_admin_creation_invalid_email():
    # Prueba para asegurar que un email inválido no sea permitido al crear un administrador
    admin = Admin(nombre='Administrador', email='invalid-email')
    with pytest.raises(ValidationError):
        admin.full_clean()
        admin.save()

@pytest.mark.django_db
def test_admin_update_invalid_email():
    # Prueba para asegurar que un email inválido no sea permitido al actualizar un administrador
    admin = Admin.objects.create(nombre='Admin', email='admin@example.com')
    admin.email = 'invalid-email'
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'Enter a valid email address.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_update_empty_email():
    # Prueba para asegurar que el email no esté vacío al actualizar un administrador
    admin = Admin.objects.create(nombre='Admin', email='admin@example.com')
    admin.email = ''
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El email es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_update_empty_name():
    # Prueba para asegurar que el nombre no esté vacío al actualizar un administrador
    admin = Admin.objects.create(nombre='Admin', email='admin@example.com')
    admin.nombre = ''
    with pytest.raises(ValidationError) as excinfo:
        admin.full_clean()
        admin.save()
    assert 'El nombre es obligatorio.' in str(excinfo.value)

@pytest.mark.django_db
def test_admin_update_name_strip_whitespace():
    # Prueba para asegurar que los espacios en blanco en el nombre se eliminen al actualizar un administrador
    admin = Admin.objects.create(nombre='Admin', email='admin@example.com')
    admin.nombre = '   Admin   '
    admin.full_clean()
    admin.save()
    assert admin.nombre == 'Admin'