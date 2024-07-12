from django import forms
from django.contrib.auth.models import User
from .models import Especialista, Especialidad, Profile
from myapp.models import *

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    rut = forms.CharField(max_length=12, label='RUT')
    nombre = forms.CharField(max_length=30, label='Nombre')
    apellido_paterno = forms.CharField(max_length=30, label='Apellido Paterno')
    apellido_materno = forms.CharField(max_length=30, label='Apellido Materno')
    correo = forms.EmailField(label='Correo')
    numero_telefonico = forms.CharField(max_length=15, label='Número Telefónico')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Nacimiento')
    genero = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], label='Género')
    prevision = forms.ChoiceField(choices=[('Fonasa', 'Fonasa'), ('Isapre', 'Isapre'), ('Colmena', 'Colmena')], label='Previsión')

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'numero_telefonico', 'fecha_nacimiento', 'genero', 'prevision']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

class RegisterDoctorsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    rut = forms.CharField(max_length=12, label='RUT')
    nombre = forms.CharField(max_length=30, label='Nombre')
    apellido_paterno = forms.CharField(max_length=30, label='Apellido Paterno')
    apellido_materno = forms.CharField(max_length=30, label='Apellido Materno')
    correo = forms.EmailField(label='Correo')
    numero_telefonico = forms.CharField(max_length=15, label='Número Telefónico')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Nacimiento')
    genero = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], label='Género')
    especialidad = forms.ChoiceField(choices=[('Medicina General', 'Medicina General'), ('Dentista', 'Dentista'), ('Nutricionista', 'Nutricionista')], label='Especialidad')  

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'numero_telefonico', 'fecha_nacimiento', 'genero', 'especialidad']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

class RegisterSpecialistForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    run = forms.CharField(max_length=20, label='RUT')
    nombre = forms.CharField(max_length=50, label='Nombre')
    apellido_paterno = forms.CharField(max_length=50, label='Apellido Paterno')
    apellido_materno = forms.CharField(max_length=50, label='Apellido Materno')
    correo = forms.EmailField(label='Correo')
    telefono = forms.CharField(max_length=20, label='Teléfono')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Nacimiento')
    genero = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], label='Género')
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), label='Especialidad')

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'run', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'telefono', 'fecha_nacimiento', 'genero', 'especialidad']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), label='Especialidad')

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

class EspecialistaForm(forms.ModelForm):
    class Meta:
        model = Especialista
        fields = ['nombre', 'correo', 'especialidad', 'telefono']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'fecha_nacimiento', 'genero', 'comentarios']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
