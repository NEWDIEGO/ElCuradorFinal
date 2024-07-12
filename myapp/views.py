#FROM E IMPORT UNICOS (REVISAR)
from django.utils.timezone import make_aware, localtime
from django.db.models import Count
from myapp.models import Cliente, Especialista, HistorialAtencion
from datetime import datetime, date, timedelta
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm, RegisterForm, EspecialistaForm
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponse
from django.db.models import Q
from reportlab.pdfgen import canvas
#FROM E IMPORT UNICOS (LISTOS)
from audioop import reverse
from profile import Profile
from django.db.models import Count
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator
from sqlite3 import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Especialista, Especialidad, Cliente, HorariosAtencion, Notificacion, Reserva, HistorialAtencion, Profile, Calificacion
from django.contrib.auth import get_user_model
from django import template
from .forms import ProfilePictureForm
import calendar
import random
import pytz
from django.db import transaction
from io import BytesIO
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Reserva
from django.core.mail import EmailMessage
import qrcode
from django.conf import settings
import logging

reagendamientos_propuestos = {}

register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

def is_admin(user):
    return user.is_superuser

def is_especialista(user):
    return user.is_authenticated and hasattr(user, 'especialista')

def is_cliente(user):
    return hasattr(user, 'cliente')

@login_required
def home(request):
    context = {
        'is_cliente': is_cliente(request.user),
        'is_admin': is_admin(request.user),
        'is_especialista': is_especialista(request.user),
    }
    return render(request, 'home.html', context)

def index(request):
    return render(request, 'home/index.html')

def home(request):
    return render(request, 'home/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso. ¡Bienvenido!')

            # Envío de correo electrónico al usuario
            mail_subject = 'Bienvenido a "El Curador"'
            message = f'Usted ingresó al sistema de El Curador, {user.username}. Le damos la bienvenida.'
            send_mail(
                mail_subject,
                message,
                'curador778@gmail.com',
                [user.email],  # Envía al correo registrado del usuario
                fail_silently=False,
            )

            # Asegurarse de que el perfil existe
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)

            if hasattr(user, 'especialista'):
                return redirect('esp_dashboard')  # Redirige a la página de especialista
            elif user.is_staff:
                return redirect('admin_dashboard')  # Redirige a la página de administrador
            else:
                return redirect('home')  # Redirige a la página de cliente
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return redirect('login')  # Redirigir de nuevo al login si hay error
    else:
        return render(request, 'home/login.html')

@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'nombre_completo': f'{user.first_name} {user.last_name}',
        'fecha_nacimiento': profile.fecha_nacimiento,
        'correo': user.email,
        'genero': profile.genero,
        'comentarios': profile.comentarios,
        'redirect_url': 'home',
    }

    try:
        cliente = Cliente.objects.get(usuario=user)
        context.update({
            'nombre_completo': f"{cliente.nombre} {cliente.apellido_paterno} {cliente.apellido_materno}",
            'fecha_nacimiento': cliente.fecha_nacimiento.strftime('%d/%m/%Y'),
            'correo': cliente.correo,
            'genero': cliente.genero,
            'redirect_url': 'home'
        })
    except Cliente.DoesNotExist:
        try:
            especialista = Especialista.objects.get(usuario=user)
            context.update({
                'nombre_completo': f"{especialista.nombre} {especialista.apellido_paterno} {especialista.apellido_materno}",
                'fecha_nacimiento': especialista.fecha_nacimiento.strftime('%d/%m/%Y'),
                'correo': especialista.correo,
                'genero': especialista.genero,
                'redirect_url': 'esp_dashboard'
            })
        except Especialista.DoesNotExist:
            if user.is_staff:
                context.update({
                    'redirect_url': 'admin_dashboard'
                })

    return render(request, 'home/profile.html', context)

@login_required
@user_passes_test(is_especialista)
def especialista_datos_paciente(request):
    return render(request, 'especialista/datos_paciente.html')

@login_required
@user_passes_test(is_especialista)
def especialista_historial(request):
    especialista = request.user.especialista
    historiales = HistorialAtencion.objects.filter(especialista=especialista)
    return render(request, 'especialista/historial.html', {'historiales': historiales})

@login_required
@user_passes_test(is_especialista)
def especialista_lista_espera(request):
    reservas = Reserva.objects.filter(estado='asignado')
    return render(request, 'especialista/lista_espera.html', {'reservas': reservas})

@login_required
@user_passes_test(is_especialista)
def especialista_notificar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Reserva.ESTADO_CHOICES):
            reserva.estado = nuevo_estado
            reserva.save()

            # Crear un registro en HistorialAtencion
            historial = HistorialAtencion(
                fecha=datetime.now().date(),
                comentario=comentario,
                cliente=reserva.cliente,
                especialista=reserva.horario_atencion.especialista,
                reserva=reserva
            )
            historial.save()
            
            messages.success(request, 'Reserva notificada exitosamente.')
        else:
            messages.error(request, 'Estado no válido.')
        return redirect('especialista_lista_espera')

    context = {
        'reserva': reserva,
    }
    return render(request, 'especialista/notificar_reserva.html', context)

@login_required
@user_passes_test(is_especialista)
def actualizar_estado_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        nuevo_comentario = request.POST.get('comentario')
        if nuevo_estado in dict(Reserva.ESTADO_CHOICES):
            reserva.estado = nuevo_estado
            reserva.comentario = nuevo_comentario
            reserva.save()

            # Crear una entrada en HistorialAtencion
            HistorialAtencion.objects.create(
                fecha=reserva.agendar_hora.date(),
                comentario=nuevo_comentario,
                cliente=reserva.cliente,
                especialista=reserva.horario_atencion.especialista,
                reserva=reserva
            )

            # Enviar correo de notificación al cliente
            send_mail(
                subject='Actualización de Reserva',
                message=f"""
                Estimado/a {reserva.cliente.nombre} {reserva.cliente.apellido_paterno},

                La reserva con el número {reserva.nro_reserva} ha sido actualizada.

                Detalles de la reserva:
                - Nombre: {reserva.cliente.nombre} {reserva.cliente.apellido_paterno}
                - Fecha: {reserva.agendar_hora.date()}
                - Hora: {reserva.agendar_hora.time()}
                - Estado: {reserva.get_estado_display()}
                - Comentario: {nuevo_comentario}

                Gracias,
                El Curador
                """,
                from_email='curador778@gmail.com',
                recipient_list=[reserva.cliente.correo],
                fail_silently=False,
            )

            messages.success(request, 'Reserva actualizada exitosamente.')
        else:
            messages.error(request, 'Estado no válido.')
    return redirect('especialista_lista_espera')

@login_required
@user_passes_test(is_especialista)
def horarios_semana(request):
    today = datetime.today()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)

    mes = int(request.GET.get('mes', today.month))
    semana = int(request.GET.get('semana', 1))
    
    start_week = datetime(2024, mes, 1) + timedelta(weeks=semana-1)
    end_week = start_week + timedelta(days=6)

    horarios = HorariosAtencion.objects.filter(fecha__range=[start_week, end_week]).order_by('hora_inicio')

    calendario = {hora: {dia: [] for dia in range(7)} for hora in range(8, 18)}

    for horario in horarios:
        dia_semana = horario.fecha.weekday()
        hora_inicio = horario
        hora_inicio = horario.hora_inicio.hour
        dia_info = {
            'id': horario.id,  # Para poder usar en la URL de anular/activar
            'especialista': f"{horario.especialista.nombre} {horario.especialista.apellido_paterno}",
            'fecha': horario.fecha.strftime('%d/%m/%Y'),
            'dia_semana': horario.fecha.strftime('%A'),
            'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
            'hora_fin': horario.hora_fin.strftime('%H:%M'),
            'duracion': horario.duracion_cita,
            'activo': horario.activo
        }
        calendario[hora_inicio][dia_semana].append(dia_info)

    meses = [(i, calendar.month_name[i]) for i in range(1, 13)]
    semanas = range(1, 5)

    context = {
        'calendario': calendario,
        'meses': meses,
        'semanas': semanas,
        'mes': mes,
        'semana': semana
    }

    return render(request, 'especialista/ver_horarios.html', context)

@login_required
@user_passes_test(is_especialista)
def activar_horario(request, horario_id):
    mes = request.GET.get('mes', datetime.today().month)
    semana = request.GET.get('semana', 1)
    try:
        horario = HorariosAtencion.objects.get(id=horario_id)
        horario.activo = True
        horario.save()
        messages.success(request, 'Horario activado exitosamente.')
    except HorariosAtencion.DoesNotExist:
        messages.error(request, 'El horario no existe.')
    return redirect(f'/especialista/ver_horarios/?mes={mes}&semana={semana}')

@login_required
@user_passes_test(is_especialista)
def anular_horario(request, horario_id):
    mes = request.GET.get('mes', datetime.today().month)
    semana = request.GET.get('semana', 1)
    try:
        horario = HorariosAtencion.objects.get(id=horario_id)
        horario.activo = False
        horario.save()
        messages.success(request, 'Horario anulado exitosamente.')
    except HorariosAtencion.DoesNotExist:
        messages.error(request, 'El horario no existe.')
    return redirect(f'/especialista/ver_horarios/?mes={mes}&semana={semana}')

@login_required
@user_passes_test(is_cliente)
def cargar_especialistas(request):
    especialidad_id = request.GET.get('especialidad_id')
    especialistas = Especialista.objects.filter(especialidad_id=especialidad_id).all()
    return JsonResponse(list(especialistas.values('id', 'nombre', 'apellido_paterno')), safe=False)

@login_required
def profile(request):
    usuario = request.user
    redirect_url = reverse_lazy('home')  # Valor por defecto

    # Contexto inicial
    context = {
        'nombre_completo': f"{usuario.first_name} {usuario.last_name}",
        'fecha_nacimiento': '',
        'correo': usuario.email,
        'genero': '',
        'comentarios': 'Aquí van los comentarios del usuario.',  # Ajusta esto según tus necesidades
        'redirect_url': redirect_url
    }

    try:
        cliente = Cliente.objects.get(usuario=usuario)
        context.update({
            'nombre_completo': f"{cliente.nombre} {cliente.apellido_paterno} {cliente.apellido_materno}",
            'fecha_nacimiento': cliente.fecha_nacimiento.strftime('%d/%m/%Y'),
            'correo': cliente.correo,
            'genero': cliente.genero,
            'redirect_url': reverse_lazy('home')
        })
    except Cliente.DoesNotExist:
        try:
            especialista = Especialista.objects.get(usuario=usuario)
            context.update({
                'nombre_completo': f"{especialista.nombre} {especialista.apellido_paterno} {especialista.apellido_materno}",
                'fecha_nacimiento': especialista.fecha_nacimiento.strftime('%d/%m/%Y'),
                'correo': especialista.correo,
                'genero': especialista.genero,
                'redirect_url': reverse_lazy('esp_dashboard')
            })
        except Especialista.DoesNotExist:
            if usuario.is_staff:
                context.update({
                    'redirect_url': reverse_lazy('admin_dashboard')
                })

    return render(request, 'home/profile.html', context)

User = get_user_model()

def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generar un PIN aleatorio de 4 dígitos
            pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])

            # Guardar el PIN en la sesión del usuario
            request.session['reset_pin'] = pin
            request.session['reset_email'] = email

            # Enviar correo con el PIN
            mail_subject = 'Código de verificación para restablecer contraseña'
            message = f'Su código de verificación es: {pin}'
            send_mail(
                mail_subject,
                message,
                'curador778@gmail.com',
                [email],
                fail_silently=False,
            )

            return redirect('pin_verification')
        except User.DoesNotExist:
            return render(request, 'home/password_reset.html', {'error': 'Correo electrónico no registrado'})

    return render(request, 'home/password_reset.html')

def pin_verification_view(request):
    if request.method == "POST":
        pin = request.POST.get('pin')
        if pin == request.session.get('reset_pin'):
            email = request.session.get('reset_email')
            user = get_object_or_404(User, email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        else:
            return render(request, 'home/pin_verification.html', {'error': 'PIN incorrecto'})

    return render(request, 'home/pin_verification.html')

def password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'home/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha caducado.')
        return redirect('password_reset')

def password_reset_complete(request):
    return render(request, 'home/password_reset_complete.html')

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            rut = form.cleaned_data['rut']
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento']

            # Check if the username or rut already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro nombre de usuario.')
                return render(request, 'home/register.html', {'form': form})

            if Cliente.objects.filter(run=rut).exists():
                messages.error(request, 'El RUT ya existe. Por favor, verifica tu RUT.')
                return render(request, 'home/register.html', {'form': form})

            # Check if the user is at least 18 years old
            age = calculate_age(fecha_nacimiento)
            if age < 18:
                messages.error(request, 'Debe ser mayor de 18 años para registrarse. Ejemplo: 01/01/2006 o antes.')
                return render(request, 'home/register.html', {'form': form})

            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.email = form.cleaned_data['correo']  # Ensure email is saved
                user.save()

                Cliente.objects.create(
                    usuario=user,
                    run=form.cleaned_data['rut'],
                    nombre=form.cleaned_data['nombre'],
                    apellido_paterno=form.cleaned_data['apellido_paterno'],
                    apellido_materno=form.cleaned_data['apellido_materno'],
                    correo=form.cleaned_data['correo'],
                    telefono=form.cleaned_data['numero_telefonico'],
                    fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                    genero=form.cleaned_data['genero'],
                    prevision=form.cleaned_data['prevision']
                )

                messages.success(request, 'Cliente registrado exitosamente.')
                return redirect('login')
            except Exception as e:
                print(f"Error al crear el cliente: {e}")
                messages.error(request, 'Ocurrió un error al crear el cliente. Por favor, inténtalo de nuevo.')
        else:
            print("Errores del formulario:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    return render(request, 'home/register.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def crear_especialista(request):
    if request.method == 'POST':
        form = EspecialistaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialista creado exitosamente.')
            return redirect('lista_especialistas')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = EspecialistaForm()
    return render(request, 'especialista/crear_especialista.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def lista_especialistas(request):
    especialistas = Especialista.objects.all()
    return render(request, 'especialista/lista_especialistas.html', {'especialistas': especialistas})

@login_required
@user_passes_test(is_admin)
def detalle_especialista(request, pk):
    especialista = get_object_or_404(Especialista, pk=pk)
    return render(request, 'especialista/detalle_especialista.html', {'especialista': especialista})

@login_required
@user_passes_test(is_admin)
def editar_especialista(request, pk):
    especialista = get_object_or_404(Especialista, pk=pk)
    if request.method == 'POST':
        form = EspecialistaForm(request.POST, instance=especialista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialista actualizado exitosamente.')
            return redirect('detalle_especialista', pk=especialista.pk)
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = EspecialistaForm(instance=especialista)
    return render(request, 'especialista/editar_especialista.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def eliminar_especialista(request, pk):
    especialista = get_object_or_404(Especialista, pk=pk)
    if request.method == 'POST':
        especialista.delete()
        messages.success(request, 'Especialista eliminado exitosamente.')
        return redirect('lista_especialistas')
    return render(request, 'especialista/eliminar_especialista.html', {'especialista': especialista})

def pago_qr_view(request):
    # Obteniendo datos de la reserva (esto es solo un ejemplo, debes obtener los datos reales de la reserva)
    reserva = {
        'especialista': 'Nombre del Especialista',
        'fecha': 'Fecha de la Reserva',
        'hora_inicio': 'Hora de Inicio',
        'hora_fin': 'Hora de Fin',
        'duracion': 'Duración',
        'especialidad': 'Especialidad',
        'costo': '$15.000',
    }
    return render(request, 'cliente/pago_qr.html', {'reserva': reserva})

def nosotros(request):
    return render(request, 'nuevos/nosotros.html')

def psicologia(request):
    return render(request, 'nuevos/psicologia.html')

def medicina_general(request):
    return render(request, 'nuevos/medicina_general.html')

def salud_mental(request):
    return render(request, 'nuevos/salud_mental.html')

def dental(request):
    return render(request, 'nuevos/dental.html')

@login_required
def obtener_dias_disponibles(request, area):
    especialidad = Especialidad.objects.get(nombre__iexact=area.replace('_', ' '))
    horarios = HorariosAtencion.objects.filter(especialista__especialidad=especialidad, activo=True)

    # Excluir los horarios que ya tienen reservas
    horarios_reservados = Reserva.objects.filter(horario_atencion__in=horarios).values_list('horario_atencion_id', flat=True)
    horarios_disponibles = horarios.exclude(id__in=horarios_reservados).values('fecha').distinct()

    available_dates = [{'date': horario['fecha'].strftime('%Y-%m-%d'), 'title': 'Disponible'} for horario in horarios_disponibles]
    return JsonResponse(available_dates, safe=False)

@login_required
def detalles_horarios(request):
    fecha = request.GET.get('fecha')
    area = request.GET.get('area')
    especialidad = get_object_or_404(Especialidad, nombre__iexact=area.replace('_', ' '))

    # Excluir horarios ya reservados
    horarios_reservados = Reserva.objects.filter(horario_atencion__fecha=fecha).values_list('horario_atencion_id', flat=True)
    horarios = HorariosAtencion.objects.filter(fecha=fecha, especialista__especialidad=especialidad, activo=True).exclude(id__in=horarios_reservados)

    # Definir el costo basado en la especialidad
    costos_especialidad = {
        'psicología': 5500,
        'Medicina General': 5000,
        'Dental': 7000,
        'Salud Mental': 8500
    }

    # Añadir costo a cada horario basado en la especialidad
    for horario in horarios:
        horario.costo = costos_especialidad.get(especialidad.nombre, 0)

    # Obtener previsión del cliente
    cliente = get_object_or_404(Cliente, usuario=request.user)
    prevision = cliente.prevision.strip().lower()  # Asegurándonos de que la previsión esté en minúsculas para comparación

    # Definir descuentos basados en la previsión
    descuentos_prevision = {
        'fonasa': 3,
        'isapre': 5,
        'colmena': 10
    }

    descuento = descuentos_prevision.get(prevision, 0)

    # Calcular el total a pagar para cada horario
    for horario in horarios:
        horario.total_a_pagar = int(horario.costo - (horario.costo * descuento / 100))

    context = {
        'fecha': fecha,
        'horarios': horarios,
        'area': area.replace('_', ' ').capitalize(),
        'prevision': prevision.capitalize(),
        'descuento': descuento
    }
    return render(request, 'cli-reserva/horas.html', context)

def areas(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'cli-reserva/areas.html', {'especialidades': especialidades})

def areas(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'cli-reserva/areas.html', {'especialidades': especialidades})

def areas(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'cli-reserva/areas.html', {'especialidades': especialidades})

def areas(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'cli-reserva/areas.html', {'especialidades': especialidades})

def areas(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'cli-reserva/areas.html', {'especialidades': especialidades})

@login_required
def calendario(request):
    area = request.GET.get('area')
    especialidad = get_object_or_404(Especialidad, nombre__iexact=area.replace('_', ' '))

    today = timezone.now().date()
    horarios = HorariosAtencion.objects.filter(fecha__gte=today, activo=True, especialista__especialidad=especialidad)

    # Excluir las fechas completamente reservadas
    horarios_reservados = Reserva.objects.filter(horario_atencion__in=horarios).values_list('horario_atencion_id', flat=True)
    horarios_disponibles = horarios.exclude(id__in=horarios_reservados).values_list('fecha', flat=True).distinct()
    available_dates = [date.strftime('%Y-%m-%d') for date in horarios_disponibles]

    context = {
        'area': area,
        'available_dates': available_dates
    }
    return render(request, 'cli-reserva/calendario.html', context)

@login_required
def reserva2(request, horario_id):
    horario = get_object_or_404(HorariosAtencion, id=horario_id)
    
    if request.method == 'POST':
        comentario = request.POST.get('comentario', '')
        agendar_hora = timezone.now()

        # Verificar si ya existe una reserva para el mismo cliente y horario
        cliente = request.user.cliente
        reserva_existente = Reserva.objects.filter(cliente=cliente, horario_atencion=horario).first()
        
        if reserva_existente:
            # Manejar el caso de reserva duplicada (por ejemplo, redirigir a una página de error o mostrar un mensaje)
            return redirect('error_reserva_duplicada')
        
        # Crear la nueva reserva y capturar su ID
        nueva_reserva = Reserva.objects.create(
            horario_atencion=horario,
            cliente=cliente,
            comentario=comentario,
            agendar_hora=agendar_hora
        )

        # Redirigir a la confirmación de reserva con el `reserva_id`
        return redirect('confirmacion_reserva', reserva_id=nueva_reserva.id)

    return render(request, 'cli-reserva/reserva_form.html', {'horario': horario})

@login_required
def horas(request):
    fecha = request.GET.get('date')
    area = request.GET.get('area')
    
    # Obtener los horarios disponibles para la fecha seleccionada
    horarios = HorariosAtencion.objects.filter(fecha=fecha, activo=True, especialista__especialidad__nombre=area)
    
    context = {
        'fecha': fecha,
        'horarios': horarios,
    }
    return render(request, 'cli-reserva/horas.html', context)

@login_required
def confirmacion_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    context = {
        'reserva': reserva,
    }
    
    # Enviar el PDF por correo electrónico
    enviar_correo_con_pdf(reserva)
    
    return render(request, 'cli-reserva/confirmacion_reserva.html', context)

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user.cliente, estado__in=['asignado', 'confirmado'])
    return render(request, 'paciente/mis_reservas.html', {'reservas': reservas})

@login_required
def historial_medico(request):
    historial = HistorialAtencion.objects.filter(cliente=request.user.cliente)\
                                         .select_related('especialista', 'reserva', 'reserva__horario_atencion', 'reserva__horario_atencion__especialista', 'reserva__horario_atencion__especialista__especialidad')
    return render(request, 'paciente/historial_medico.html', {'historial': historial})

@login_required
def resultado_examenes(request):
    resultados = HistorialAtencion.objects.filter(cliente=request.user.cliente).exclude(comentario='')
    return render(request, 'paciente/resultado_examenes.html', {'resultados': resultados})

@login_required
def historial_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user.cliente).select_related('horario_atencion__especialista__especialidad')
    areas = Especialidad.objects.all()
    return render(request, 'paciente/historial_reservas.html', {'reservas': reservas, 'areas': areas})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user.cliente)
    if request.method == 'POST':
        reserva.estado = 'cancelado'
        reserva.save()
        return redirect('mis_reservas')
    return render(request, 'paciente/cancelar_reserva.html', {'reserva': reserva})

@login_required
def notificaciones(request):
    notificaciones = Notificacion.objects.filter(especialista__cliente=request.user.cliente)
    return render(request, 'paciente/notificaciones.html', {'notificaciones': notificaciones})

@login_required
@user_passes_test(lambda user: hasattr(user, 'cliente'))
def confirmar_reagendamiento(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user.cliente)
    if request.method == 'POST':
        # Obtenemos los datos de la nueva fecha y hora desde los datos guardados temporalmente
        nueva_fecha = request.session.get('nueva_fecha')
        nueva_hora_inicio = request.session.get('nueva_hora_inicio')
        nueva_hora_fin = request.session.get('nueva_hora_fin')

        if nueva_fecha and nueva_hora_inicio and nueva_hora_fin:
            nueva_fecha = datetime.strptime(nueva_fecha, '%Y-%m-%d').date()
            nueva_hora_inicio = datetime.strptime(nueva_hora_inicio, '%H:%M').time()
            nueva_hora_fin = datetime.strptime(nueva_hora_fin, '%H:%M').time()
            
            reserva.agendar_hora = datetime.combine(nueva_fecha, nueva_hora_inicio)
            reserva.hora_fin = nueva_hora_fin
            reserva.save()

            messages.success(request, 'La hora de la cita ha sido reagendada exitosamente.')
            return redirect('mis_reservas')

    return render(request, 'paciente/confirmar_reagendamiento.html', {'reserva': reserva})

@login_required
@user_passes_test(lambda user: hasattr(user, 'cliente'))
def rechazar_reagendamiento(request, reserva_id):
    if reserva_id in reagendamientos_propuestos:
        # Limpiar la propuesta después de rechazar
        del reagendamientos_propuestos[reserva_id]
        messages.success(request, 'La propuesta de reagendamiento ha sido rechazada.')
    else:
        messages.error(request, 'No se encontró la propuesta de reagendamiento.')
    
    return redirect('home')

@login_required
@user_passes_test(is_especialista)
def especialista_funciones(request):
    return render(request, 'especialista/funciones.html')

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def esp_dashboard(request):
    especialista = request.user.especialista
    
    tz = pytz.timezone('America/Santiago')
    today = datetime.now(tz).date()
    start_week = today - timedelta(days=today.weekday())  # Monday of the current week
    end_week = start_week + timedelta(days=6)  # Sunday of the current week
    start_month = today.replace(day=1)
    next_month = start_month + timedelta(days=32)
    end_month = next_month.replace(day=1) - timedelta(days=1)
    
    horarios_hoy = HorariosAtencion.objects.filter(especialista=especialista, fecha=today, reserva__isnull=False).count()
    horarios_semana = HorariosAtencion.objects.filter(especialista=especialista, fecha__range=[start_week, end_week], reserva__isnull=False).count()
    horarios_mes = HorariosAtencion.objects.filter(especialista=especialista, fecha__range=[start_month, end_month], reserva__isnull=False).count()
    total_horarios = HorariosAtencion.objects.filter(especialista=especialista, reserva__isnull=False).count()
    
    # Citas por especialidad
    citas_por_especialidad = Reserva.objects.filter(horario_atencion__especialista=especialista).values('horario_atencion__especialista__especialidad__nombre').annotate(count=Count('id'))
    
    # Atención por estado
    atencion_por_estado = Reserva.objects.filter(horario_atencion__especialista=especialista).values('estado').annotate(count=Count('id'))

    # Especialistas por área
    especialistas_por_area = Especialista.objects.values('especialidad__nombre').annotate(count=Count('id'))

    if not horarios_hoy and not horarios_semana and not horarios_mes and not total_horarios:
        messages.error(request, "No se encontraron horarios para el especialista.")
    if not citas_por_especialidad.exists():
        messages.error(request, "No se encontraron citas por especialidad para el especialista.")
    if not atencion_por_estado.exists():
        messages.error(request, "No se encontró atención por estado para el especialista.")
    if not especialistas_por_area.exists():
        messages.error(request, "No se encontraron especialistas por área.")

    context = {
        'horarios_hoy': horarios_hoy,
        'horarios_semana': horarios_semana,
        'horarios_mes': horarios_mes,
        'total_horarios': total_horarios,
        'citas_por_especialidad': citas_por_especialidad,
        'atencion_por_estado': atencion_por_estado,
        'especialistas_por_area': especialistas_por_area
    }

    return render(request, 'esp-nuevo/dashboard.html', context)

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def buscar_pacientes(request):
    return render(request, 'esp-nuevo/buscar_pacientes.html')

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def resultados_busqueda_pacientes(request):
    query = request.GET.get('buscar')
    pacientes = Cliente.objects.filter(
        Q(nombre__icontains=query) | Q(apellido_paterno__icontains=query) | Q(apellido_materno__icontains=query) | Q(run__icontains=query)
    )

    historiales = []
    if pacientes.exists():
        for paciente in pacientes:
            historial_paciente = HistorialAtencion.objects.filter(cliente=paciente)
            historiales.append({
                'paciente': paciente,
                'historial': historial_paciente if historial_paciente.exists() else None
            })
    
    return render(request, 'esp-nuevo/resultados_busqueda_pacientes.html', {'historiales': historiales})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def detalles_horarios2(request, periodo):
    especialista = request.user.especialista
    tz = pytz.timezone('America/Santiago')
    today = datetime.now(tz).date()
    start_week = today - timedelta(days=today.weekday())  # Monday of the current week
    end_week = start_week + timedelta(days=6)  # Sunday of the current week
    start_month = today.replace(day=1)
    next_month = start_month + timedelta(days=32)
    end_month = next_month.replace(day=1) - timedelta(days=1)

    start_date = parse_date(request.GET.get('start_date', ''))
    end_date = parse_date(request.GET.get('end_date', ''))

    if periodo == 'hoy':
        horarios = HorariosAtencion.objects.filter(especialista=especialista, fecha=today)
    elif periodo == 'semana':
        horarios = HorariosAtencion.objects.filter(especialista=especialista, fecha__range=[start_week, end_week])
    elif periodo == 'mes':
        horarios = HorariosAtencion.objects.filter(especialista=especialista, fecha__range=[start_month, end_month])
    else:
        horarios = HorariosAtencion.objects.filter(especialista=especialista)

    if start_date and end_date:
        horarios = horarios.filter(fecha__range=[start_date, end_date])

    # Definir el costo basado en la especialidad
    costos_especialidad = {
        'Consulta General': 5000.00,
        'Consulta Especializada': 6000.00,
        'Control Médico': 7500.00,
        'Emergencia Médica': 8500.00
    }

    # Añadir costo a cada horario basado en la especialidad
    for horario in horarios:
        if horario.especialista.especialidad.nombre == 'Consulta General':
            horario.costo = costos_especialidad['Consulta General']
        elif horario.especialista.especialidad.nombre == 'Consulta Especializada':
            horario.costo = costos_especialidad['Consulta Especializada']
        elif horario.especialista.especialidad.nombre == 'Control Médico':
            horario.costo = costos_especialidad['Control Médico']
        elif horario.especialista.especialidad.nombre == 'Emergencia Médica':
            horario.costo = costos_especialidad['Emergencia Médica']
        else:
            horario.costo = 0  # O un valor por defecto si la especialidad no coincide

    return render(request, 'esp-nuevo/detalles_horarios.html', {'horarios': horarios, 'periodo': periodo})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def confirmar_cita(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, horario_atencion__especialista__usuario=request.user)
    if request.method == 'POST':
        # Actualizar el estado de la reserva a 'confirmado'
        reserva.estado = 'confirmado'
        reserva.save()

        # Enviar una notificación al cliente
        mensaje = f"Su cita número {reserva.nro_reserva} ha sido confirmada."
        notificacion = Notificacion.objects.create(
            mensaje=mensaje,
            especialista=reserva.horario_atencion.especialista,
            leido=False
        )
        notificacion.enviar_notificacion(reserva.cliente)

        messages.success(request, 'La cita ha sido confirmada.')
        return redirect('citas_totales')  # Ajuste para redirigir a citas_totales
    
    return render(request, 'esp-nuevo/confirmar_cita.html', {'reserva': reserva})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def solucionar_cita(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, horario_atencion__especialista__usuario=request.user)
    
    if request.method == 'POST':
        comentario = request.POST.get('comentario', '')
        
        # Marcar la cita como solucionada
        reserva.estado = 'solucionado'
        reserva.save()
        
        # Registrar en HistorialAtencion
        HistorialAtencion.objects.create(
            fecha=reserva.agendar_hora.date(),
            comentario=comentario,
            cliente=reserva.cliente,
            especialista=reserva.horario_atencion.especialista,
            reserva=reserva
        )
        
        messages.success(request, 'La cita ha sido marcada como solucionada.')
        return redirect('esp_dashboard')
    
    return render(request, 'esp-nuevo/solucionar_cita.html', {'reserva': reserva})



@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def citas_totales(request):
    especialista = request.user.especialista
    current_date = datetime.now()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        citas = Reserva.objects.filter(
            horario_atencion__especialista=especialista,
            horario_atencion__fecha__gte=start_date,
            horario_atencion__fecha__lte=end_date
        ).order_by('horario_atencion__fecha', 'horario_atencion__hora_inicio')
    else:
        citas = Reserva.objects.filter(
            horario_atencion__especialista=especialista,
            horario_atencion__fecha__gte=current_date
        ).order_by('horario_atencion__fecha', 'horario_atencion__hora_inicio')

    return render(request, 'esp-nuevo/citas_totales.html', {'citas': citas, 'start_date': start_date, 'end_date': end_date})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def calendario_especialista(request):
    return render(request, 'esp-nuevo/calendario_especialista.html')

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def obtener_dias_disponibles_especialista(request):
    especialista = get_object_or_404(Especialista, usuario=request.user)
    horarios = HorariosAtencion.objects.filter(especialista=especialista, activo=True).values('fecha').distinct()
    available_dates = [{'date': horario['fecha'].strftime('%Y-%m-%d'), 'title': 'Horario Laboral'} for horario in horarios]
    return JsonResponse(available_dates, safe=False)

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def detalle_jornada_laboral(request, fecha):
    especialista = request.user.especialista
    horarios = HorariosAtencion.objects.filter(especialista=especialista, fecha=fecha).order_by('hora_inicio')
    detalles = []

    for horario in horarios:
        # Combina la fecha y la hora en objetos datetime
        hora_inicio_dt = datetime.combine(horario.fecha, horario.hora_inicio)
        hora_fin_dt = datetime.combine(horario.fecha, horario.hora_fin)

        # Asegúrate de que los datetime son "aware"
        hora_inicio_aware = make_aware(hora_inicio_dt)
        hora_fin_aware = make_aware(hora_fin_dt)

        reserva = Reserva.objects.filter(horario_atencion=horario).first()
        if reserva:
            detalles.append({
                'hora_inicio': localtime(hora_inicio_aware).strftime('%I:%M %p'),
                'hora_fin': localtime(hora_fin_aware).strftime('%I:%M %p'),
                'duracion_cita': horario.duracion_cita,
                'cliente': f"{reserva.cliente.nombre} {reserva.cliente.apellido_paterno}",
                'reserva_id': reserva.id,
                'horario_id': horario.id,
                'activo': horario.activo
            })
        else:
            detalles.append({
                'hora_inicio': localtime(hora_inicio_aware).strftime('%I:%M %p'),
                'hora_fin': localtime(hora_fin_aware).strftime('%I:%M %p'),
                'duracion_cita': horario.duracion_cita,
                'cliente': 'Ninguno',
                'horario_id': horario.id,
                'activo': horario.activo
            })

    context = {
        'fecha': fecha,
        'detalles': detalles
    }
    return render(request, 'esp-nuevo/detalles_jornada_laboral.html', context)

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def desactivar_horario(request, horario_id):
    horario = get_object_or_404(HorariosAtencion, id=horario_id, especialista__usuario=request.user)
    if request.method == 'POST':
        horario.activo = False
        horario.save()
        return redirect('detalle_jornada_laboral', fecha=horario.fecha)
    return render(request, 'esp-nuevo/desactivar_horario.html', {'horario': horario})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def cancelar_cita(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, horario_atencion__especialista__usuario=request.user)
    if request.method == 'POST':
        reserva.cancelar()
        messages.success(request, 'La reserva ha sido cancelada.')
        return redirect('citas_mes')  # Ajuste para redirigir a citas_mes
    return render(request, 'esp-nuevo/cancelar_cita.html', {'reserva': reserva})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def reagendar_cita(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, horario_atencion__especialista__usuario=request.user)
    if request.method == 'POST':
        nueva_fecha = request.POST.get('nueva_fecha')
        nueva_hora_inicio = request.POST.get('nueva_hora_inicio')
        nueva_hora_fin = request.POST.get('nueva_hora_fin')

        # Guardamos temporalmente los datos en la sesión
        request.session['nueva_fecha'] = nueva_fecha
        request.session['nueva_hora_inicio'] = nueva_hora_inicio
        request.session['nueva_hora_fin'] = nueva_hora_fin

        # Enviamos el correo con el enlace para confirmar
        confirmar_url = request.build_absolute_uri(reverse('confirmar_reagendamiento', args=[reserva.id]))
        mensaje = f"Por favor confirme su nueva cita médica en el siguiente enlace: {confirmar_url}\n\nDebe iniciar sesión en su correo para confirmar o rechazar."
        send_mail(
            'Confirmación de Reagendamiento de Cita',
            mensaje,
            'tu_correo@ejemplo.com',
            [reserva.cliente.correo],
            fail_silently=False,
        )
        
        messages.success(request, 'La propuesta de reagendamiento ha sido enviada. Esperando confirmación del cliente. Por favor, pida al cliente que inicie sesión en su correo para confirmar o rechazar.')
        return redirect('detalle_jornada_laboral', fecha=reserva.horario_atencion.fecha)

    return render(request, 'esp-nuevo/reagendar_cita.html', {'reserva': reserva})

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def activar_horario(request, horario_id):
    horario = get_object_or_404(HorariosAtencion, id=horario_id, especialista__usuario=request.user)
    if request.method == 'POST':
        horario.activo = True
        horario.save()
        return redirect('detalle_jornada_laboral', fecha=horario.fecha)
    return render(request, 'esp-nuevo/activar_horario.html', {'horario': horario})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Contar administradores, especialistas y pacientes
    admin_count = User.objects.filter(is_superuser=True).count()
    specialist_count = User.objects.filter(especialista__isnull=False).count()
    patient_count = User.objects.filter(is_staff=False, especialista__isnull=True).count()

    # Contar citas por especialidad
    especialidades = Especialidad.objects.all()
    citas_por_especialidad = Reserva.objects.values('horario_atencion__especialista__especialidad__nombre').annotate(count=Count('id'))

    # Contar reservas por estado
    reservas_asignadas = Reserva.objects.filter(estado='asignado').count()
    reservas_confirmadas = Reserva.objects.filter(estado='confirmado').count()
    reservas_canceladas = Reserva.objects.filter(estado='cancelado').count()
    reservas_solucionadas = Reserva.objects.filter(estado='solucionado').count()

    # Contar especialistas por especialidad
    especialistas_por_especialidad = Especialista.objects.values('especialidad__nombre').annotate(count=Count('id'))

    context = {
        'admin_count': admin_count,
        'specialist_count': specialist_count,
        'patient_count': patient_count,
        'especialidades': especialidades,
        'citas_por_especialidad': citas_por_especialidad,
        'reservas_asignadas': reservas_asignadas,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_canceladas': reservas_canceladas,
        'reservas_solucionadas': reservas_solucionadas,
        'especialistas_por_especialidad': especialistas_por_especialidad,
    }
    return render(request, 'administrador/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_modify_user(request):
    user = None
    cliente = None
    especialista = None
    especialidades = Especialidad.objects.all()

    if request.method == 'POST':
        if 'search' in request.POST:
            search_query = request.POST.get('search_query', '').strip()
            if search_query:
                try:
                    user = User.objects.get(username=search_query)
                    cliente = Cliente.objects.filter(usuario=user).first()
                    especialista = Especialista.objects.filter(usuario=user).first()
                    if cliente:
                        context = {'user': user, 'cliente': cliente, 'especialidades': especialidades, 'found': True}
                    elif especialista:
                        context = {'user': user, 'especialista': especialista, 'especialidades': especialidades, 'found': True}
                    else:
                        context = {'user': user, 'especialidades': especialidades, 'found': True}
                    return render(request, 'administrador/modify_user.html', context)
                except User.DoesNotExist:
                    messages.error(request, 'El usuario no existe.')
                    return redirect('admin_modify_user')
        elif 'modify' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            new_username = request.POST.get('username', '').strip()
            new_email = request.POST.get('email', '').strip()

            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'El nombre de usuario ya existe')
                return render(request, 'administrador/modify_user.html', {'user': user, 'especialidades': especialidades, 'found': True})

            if new_email != user.email:
                if User.objects.filter(email=new_email).exists():
                    messages.error(request, 'El correo electrónico ya existe')
                    return render(request, 'administrador/modify_user.html', {'user': user, 'especialidades': especialidades, 'found': True})
                else:
                    user.email = new_email

            user.username = new_username

            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            if password and password == confirm_password:
                user.set_password(password)
            user.save()

            if hasattr(user, 'cliente'):
                cliente = user.cliente
                cliente.nombre = request.POST.get('nombre', '').strip()
                cliente.apellido_paterno = request.POST.get('apellido_paterno', '').strip()
                cliente.apellido_materno = request.POST.get('apellido_materno', '').strip()
                cliente.telefono = request.POST.get('telefono', '').strip()
                cliente.save()
            elif hasattr(user, 'especialista'):
                especialista = user.especialista
                especialista.nombre = request.POST.get('nombre', '').strip()
                especialista.apellido_paterno = request.POST.get('apellido_paterno', '').strip()
                especialista.apellido_materno = request.POST.get('apellido_materno', '').strip()
                especialista.telefono = request.POST.get('telefono', '').strip()
                especialista.genero = request.POST.get('genero', '').strip()
                especialista.especialidad = Especialidad.objects.get(id=request.POST.get('especialidad'))
                especialista.save()

            messages.success(request, 'Usuario modificado exitosamente')
            return redirect('admin_modify_user')

    return render(request, 'administrador/modify_user.html', {'especialidades': especialidades, 'found': False})


@login_required
@user_passes_test(is_admin)
def admin_assign_schedules(request):
    if request.method == 'POST':
        especialista_id = request.POST.get('especialista')
        fecha_str = request.POST.get('fecha')
        hora_inicio_str = request.POST.get('hora_inicio')
        hora_termino_str = request.POST.get('hora_termino')

        try:
            especialista = Especialista.objects.get(id=especialista_id)
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fin = datetime.strptime(hora_termino_str, '%H:%M').time()

            ahora = datetime.now().date()
            if fecha < ahora:
                messages.error(request, 'No puedes asignar horarios en fechas pasadas.')
                raise ValueError('Fecha inválida')
            
            if not (6 <= hora_inicio.hour <= 22):
                messages.error(request, 'La hora de inicio debe estar entre las 06:00 y las 22:00.')
                raise ValueError('Hora de inicio inválida')
            
            if not (6 <= hora_fin.hour <= 22):
                messages.error(request, 'La hora de término debe estar entre las 06:00 y las 22:00.')
                raise ValueError('Hora de término inválida')

            if hora_inicio >= hora_fin:
                messages.error(request, 'La hora de inicio debe ser anterior a la hora de término.')
                raise ValueError('Rango de horas inválido')

            # Verificar si el horario se solapa con otro horario del mismo especialista
            overlapping_schedule = HorariosAtencion.objects.filter(
                especialista=especialista,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exists()

            if overlapping_schedule:
                messages.error(request, 'El especialista ya tiene un horario asignado en este intervalo.')
                raise ValueError('Horario solapado')

            duracion_cita = (datetime.combine(fecha, hora_fin) - datetime.combine(fecha, hora_inicio)).seconds // 60
            dia_semana = fecha.strftime('%A')

            HorariosAtencion.objects.create(
                dia_semana=dia_semana,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                duracion_cita=duracion_cita,
                especialista=especialista
            )

            messages.success(request, 'Horario asignado correctamente.')
            return redirect('admin_assign_schedules')
        except Especialista.DoesNotExist:
            messages.error(request, 'Especialista no encontrado.')
        except ValueError:
            # Mensajes de error ya han sido agregados.
            pass
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    especialistas = Especialista.objects.all()
    return render(request, 'administrador/assign_schedules.html', {'especialistas': especialistas})

@login_required
@user_passes_test(is_admin)
def admin_create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        tipo_usuario = request.POST.get('tipo_usuario', '')

        # Validaciones de datos
        if password != confirm_password:
            return render(request, 'administrador/create_user.html', {'error': 'Las contraseñas no coinciden'})

        if len(username) < 3:
            return render(request, 'administrador/create_user.html', {'error': 'El nombre de usuario debe tener al menos 3 caracteres'})

        if User.objects.filter(username=username).exists():
            return render(request, 'administrador/create_user.html', {'error': 'El nombre de usuario ya existe'})

        try:
            with transaction.atomic():
                # Crear el usuario
                user = User.objects.create_user(username=username, email=request.POST.get('correo'), password=password)

                if tipo_usuario == 'administrador':
                    user.is_staff = True  # Permiso para acceder a la consola de administración
                    user.is_superuser = True  # Permiso de superusuario
                elif tipo_usuario == 'especialista':
                    run = request.POST.get('rut')
                    nombre = request.POST.get('nombre')
                    apellido_paterno = request.POST.get('apellido_paterno')
                    apellido_materno = request.POST.get('apellido_materno')
                    correo = request.POST.get('correo')
                    telefono = request.POST.get('numero_telefonico')
                    fecha_nacimiento = request.POST.get('fecha_nacimiento')
                    genero = request.POST.get('genero')
                    especialidad_id = request.POST.get('especialidad')

                    try:
                        especialidad = Especialidad.objects.get(id=especialidad_id)
                    except Especialidad.DoesNotExist:
                        return render(request, 'administrador/create_user.html', {'error': 'La especialidad seleccionada no existe'})

                    Especialista.objects.create(
                        usuario=user,
                        run=run,
                        nombre=nombre,
                        apellido_paterno=apellido_paterno,
                        apellido_materno=apellido_materno,
                        correo=correo,
                        telefono=telefono,
                        fecha_nacimiento=fecha_nacimiento,
                        genero=genero,
                        especialidad=especialidad
                    )
                    user.is_staff = False  # No debe ser staff

                user.save()
                messages.success(request, 'Usuario creado correctamente.')
                return redirect('admin_dashboard')

        except IntegrityError:
            return render(request, 'administrador/create_user.html', {'error': 'El nombre de usuario ya existe'})
        except Exception as e:
            return render(request, 'administrador/create_user.html', {'error': f'Error: {str(e)}'})

    else:
        especialidades = Especialidad.objects.all()
        return render(request, 'administrador/create_user.html', {'especialidades': especialidades})

@login_required
@user_passes_test(is_admin)
def admin_view_reports(request):
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    area = request.GET.get('area', 'Todos')
    tecnico_id = request.GET.get('tecnico', 'Todos')

    # Convertir las fechas de los filtros
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d') if fecha_inicio_str else None
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') if fecha_fin_str else None

    # Filtros
    horarios = HorariosAtencion.objects.all()
    if fecha_inicio and fecha_fin:
        horarios = horarios.filter(fecha__range=[fecha_inicio, fecha_fin])

    if area and area != 'Todos':
        horarios = horarios.filter(especialista__especialidad__nombre=area)

    if tecnico_id and tecnico_id != 'Todos':
        horarios = horarios.filter(especialista__id=tecnico_id)

    # Cantidad total de registros
    total_registros = horarios.count()

    # Cantidad de registros por especialista
    registros_por_especialistas = horarios.values(
        'especialista__usuario__username',
        'especialista__nombre',
        'especialista__apellido_paterno',
        'especialista__apellido_materno',
        'especialista__correo',
        'especialista__especialidad__nombre'
    ).annotate(total_registros=Count('id'))

    # Cantidad de usuarios registrados
    usuarios = User.objects.all()
    if area and area != 'Todos':
        usuarios = usuarios.filter(especialista__especialidad__nombre=area)
    total_usuarios = usuarios.count()

    especialidades = Especialidad.objects.all()
    tecnicos = Especialista.objects.all()
    if area and area != 'Todos':
        tecnicos = tecnicos.filter(especialidad__nombre=area)

    context = {
        'total_registros': total_registros,
        'registros_por_especialistas': registros_por_especialistas,
        'total_usuarios': total_usuarios,
        'especialidades': especialidades,
        'tecnicos': tecnicos,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'area_seleccionada': area,
        'tecnico_seleccionado': tecnico_id,
    }

    return render(request, 'administrador/view_reports.html', context)

def generate_pdf(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    horario = reserva.horario_atencion
    especialista = horario.especialista
    cliente = reserva.cliente

    costos_especialidad = {
        'psicología': 5500,
        'Medicina General': 5000,
        'Dental': 7000,
        'Salud Mental': 8500
    }
    costo = costos_especialidad.get(especialista.especialidad.nombre, 0)

    prevision = cliente.prevision.strip().lower()
    descuentos_prevision = {
        'fonasa': 3,
        'isapre': 5,
        'colmena': 10
    }
    descuento = descuentos_prevision.get(prevision, 0)
    total_a_pagar = int(costo - (costo * descuento / 100))

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Añadir logo
    logo_path = "C:/Users/Diego/OneDrive/Desktop/CURADOR 26 JUNIO/El_Curador/myapp/static/images/LogoFinal.png"
    p.drawImage(ImageReader(logo_path), 50, 750, width=100, height=100)

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Reserva de “El Curador”")

    # Cambiar a Arial 11 para el resto del texto
    p.setFont("Helvetica", 11)

    # Información de la reserva
    p.drawString(50, 720, f"N° De Reserva: {reserva.nro_reserva}")
    p.drawString(50, 700, f"Paciente: {cliente.nombre} {cliente.apellido_paterno} {cliente.apellido_materno}")
    p.drawString(50, 680, f"Fecha de la reserva: {horario.fecha.strftime('%d-%m-%Y')}")
    p.drawString(50, 660, f"Especialista: {especialista.nombre} {especialista.apellido_paterno}")
    p.drawString(50, 640, f"Área: {especialista.especialidad.nombre}")
    p.drawString(50, 620, f"Hora Inicio: {horario.hora_inicio.strftime('%I:%M %p')}")
    p.drawString(50, 600, f"Hora Fin: {horario.hora_fin.strftime('%I:%M %p')}")
    p.drawString(50, 580, f"Duración de la Cita: {horario.duracion_cita} minutos")
    p.drawString(50, 560, f"Consultorio: El Curador")
    p.drawString(50, 540, f"Valor: ${costo}")
    p.drawString(50, 520, f"Previsión: {prevision.capitalize()}")
    p.drawString(50, 500, f"Descuento: {descuento}%")
    p.drawString(50, 480, f"Total a Pagar: ${total_a_pagar}")

    # Añadir código QR
    qr_data = f"Reserva: {reserva.nro_reserva}, Paciente: {cliente.nombre} {cliente.apellido_paterno}, Total: ${total_a_pagar}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_buffer = BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)
    p.drawImage(ImageReader(img_buffer), 400, 500, width=100, height=100)

    # Dirección y contacto
    p.drawString(50, 300, "Dirección")
    p.drawString(50, 280, "Av. Concha y Toro 26, Puente Alto, Santiago, Región Metropolitana")
    p.drawString(50, 260, "Teléfono")
    p.drawString(50, 240, "+56 2 1234 5678")
    p.drawString(50, 220, "Correo electrónico")
    p.drawString(50, 200, "curador778@gmail.com")

    # Cerrar el objeto PDF limpiamente
    p.showPage()
    p.save()

    # Obtener el valor del buffer de BytesIO y escribirlo en la respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Comprobante_{reserva.nro_reserva}.pdf"'
    return response

#citas_especialista
def citas_hoy(request):
    hoy = date.today()
    citas = Reserva.objects.filter(agendar_hora__date=hoy)

    context = {
        'citas': citas,
    }
    return render(request, 'esp-nuevo/citas_hoy.html', context)

def citas_semana(request):
    hoy = date.today()
    fin_semana = hoy + timedelta(days=7)
    citas = Reserva.objects.filter(agendar_hora__date__range=[hoy, fin_semana])

    context = {
        'citas': citas,
    }
    return render(request, 'esp-nuevo/citas_semana.html', context)

def citas_mes(request):
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)
    proximo_mes = primer_dia_mes + timedelta(days=32)
    primer_dia_proximo_mes = proximo_mes.replace(day=1)
    
    citas = Reserva.objects.filter(agendar_hora__date__gte=primer_dia_mes, agendar_hora__date__lt=primer_dia_proximo_mes, horario_atencion__especialista=request.user.especialista)

    context = {
        'citas': citas,
    }
    return render(request, 'esp-nuevo/citas_mes.html', context)

@login_required
@user_passes_test(lambda user: hasattr(user, 'especialista'))
def citas_confirmadas(request):
    # Obtener todas las citas confirmadas sin filtrar por especialista
    citas_confirmadas = Reserva.objects.filter(estado='confirmado')
    
    # Depuración
    for reserva in citas_confirmadas:
        print(f"Reserva ID: {reserva.id}, Fecha: {reserva.horario_atencion.fecha}, Estado: {reserva.estado}")

    return render(request, 'esp-nuevo/citas_confirmadas.html', {'citas_confirmadas': citas_confirmadas})

def enviar_correo_con_pdf(reserva):
    try:
        horario = reserva.horario_atencion
        especialista = horario.especialista
        cliente = reserva.cliente

        costos_especialidad = {
            'psicología': 5500,
            'Medicina General': 5000,
            'Dental': 7000,
            'Salud Mental': 8500
        }
        costo = costos_especialidad.get(especialista.especialidad.nombre, 0)

        prevision = cliente.prevision.strip().lower()
        descuentos_prevision = {
            'fonasa': 3,
            'isapre': 5,
            'colmena': 10
        }
        descuento = descuentos_prevision.get(prevision, 0)
        total_a_pagar = int(costo - (costo * descuento / 100))

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        # Añadir logo
        logo_path = "C:/Users/Diego/OneDrive/Desktop/CURADOR 26 JUNIO/El_Curador/myapp/static/images/LogoFinal.png"
        p.drawImage(ImageReader(logo_path), 50, 750, width=100, height=100)

        # Título
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, 800, "Reserva de “El Curador”")

        # Cambiar a Arial 11 para el resto del texto
        p.setFont("Helvetica", 11)

        # Información de la reserva
        p.drawString(50, 720, f"N° De Reserva: {reserva.nro_reserva}")
        p.drawString(50, 700, f"Paciente: {cliente.nombre} {cliente.apellido_paterno} {cliente.apellido_materno}")
        p.drawString(50, 680, f"Fecha de la reserva: {horario.fecha.strftime('%d-%m-%Y')}")
        p.drawString(50, 660, f"Especialista: {especialista.nombre} {especialista.apellido_paterno}")
        p.drawString(50, 640, f"Área: {especialista.especialidad.nombre}")
        p.drawString(50, 620, f"Hora Inicio: {horario.hora_inicio.strftime('%I:%M %p')}")
        p.drawString(50, 600, f"Hora Fin: {horario.hora_fin.strftime('%I:%M %p')}")
        p.drawString(50, 580, f"Duración de la Cita: {horario.duracion_cita} minutos")
        p.drawString(50, 560, f"Consultorio: El Curador")
        p.drawString(50, 540, f"Valor: ${costo}")
        p.drawString(50, 520, f"Previsión: {prevision.capitalize()}")
        p.drawString(50, 500, f"Descuento: {descuento}%")
        p.drawString(50, 480, f"Total a Pagar: ${total_a_pagar}")

        # Añadir código QR
        qr_data = f"Reserva: {reserva.nro_reserva}, Paciente: {cliente.nombre} {cliente.apellido_paterno}, Total: ${total_a_pagar}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img_buffer = BytesIO()
        img.save(img_buffer)
        img_buffer.seek(0)
        p.drawImage(ImageReader(img_buffer), 400, 500, width=100, height=100)

        # Dirección y contacto
        p.drawString(50, 300, "Dirección")
        p.drawString(50, 280, "Av. Concha y Toro 26, Puente Alto, Santiago, Región Metropolitana")
        p.drawString(50, 260, "Teléfono")
        p.drawString(50, 240, "+56 2 1234 5678")
        p.drawString(50, 220, "Correo electrónico")
        p.drawString(50, 200, "curador778@gmail.com")

        p.showPage()
        p.save()

        buffer.seek(0)

        # Crear el correo electrónico
        mail_subject = 'Confirmación de Reserva - El Curador'
        message = 'Adjunto encontrará su comprobante de reserva.'
        email = EmailMessage(
            mail_subject,
            message,
            settings.EMAIL_HOST_USER,
            [cliente.correo],
        )

        # Adjuntar el PDF al correo electrónico
        email.attach(f"Comprobante_{reserva.nro_reserva}.pdf", buffer.getvalue(), 'application/pdf')

        # Enviar el correo electrónico
        email.send()
        
        # Log de éxito
        logging.info(f"Correo enviado exitosamente a {cliente.correo}")
    except Exception as e:
        # Log de error
        logging.error(f"Error al enviar correo a {cliente.correo}: {e}")

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def lista_calificaciones(request):
    calificaciones = Calificacion.objects.all()
    return render(request, 'calificaciones/lista_calificaciones.html', {'calificaciones': calificaciones})

from django.views.generic import ListView
from .models import Calificacion

class ListaCalificacionesView(ListView):
    model = Calificacion
    template_name = 'calificaciones/lista_calificaciones.html'
    context_object_name = 'calificaciones'