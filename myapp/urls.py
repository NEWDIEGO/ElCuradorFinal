from django.urls import path, include
from . import views as main_views
from rest_framework.routers import DefaultRouter
from myapp.api_crud import views as api_views
from . import views
from django.urls import path
from . import views as main_views
from .views import generate_pdf
from .views import ListaCalificacionesView

router = DefaultRouter()
router.register(r'clientes', api_views.ClienteViewSet)
router.register(r'especialistas', api_views.EspecialistaViewSet)
router.register(r'admins', api_views.AdminViewSet)

urlpatterns = [
    path('', main_views.home, name='home'),
    path('register/', main_views.register_view, name='register'),
    path('login/', main_views.login_view, name='login'),
    path('profile/', main_views.profile, name='profile'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    #path('cerrar_sesion/', main_views.cerrar_sesion, name='cerrar_sesion'),
    #reset password
    path('password_reset/', main_views.password_reset_view, name='password_reset'),
    path('pin_verification/', main_views.pin_verification_view, name='pin_verification'),
    path('password_reset_confirm/<uidb64>/<token>/', main_views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', main_views.password_reset_complete, name='password_reset_complete'),
    # Cliente URLs}
    path('pago_qr/', views.pago_qr_view, name='pago_qr'),
    # Especialista URLs
    path('especialista/funciones/', main_views.especialista_funciones, name='especialista_funciones'),
    path('especialista/ver_horarios/', main_views.horarios_semana, name='horarios_semana'),
    path('especialista/datos_paciente/', main_views.especialista_datos_paciente, name='especialista_datos_paciente'),
    path('especialista/historial/', main_views.especialista_historial, name='especialista_historial'),
    path('especialista/lista_espera/', main_views.especialista_lista_espera, name='especialista_lista_espera'),
    path('especialista/notificar_reserva/<int:reserva_id>/', main_views.especialista_notificar_reserva, name='especialista_notificar_reserva'),
    path('especialista/actualizar_estado/<int:reserva_id>/', main_views.actualizar_estado_reserva, name='actualizar_estado_reserva'),
    path('anular_horario/<int:horario_id>/', main_views.anular_horario, name='anular_horario'),
    path('activar_horario/<int:horario_id>/', main_views.activar_horario, name='activar_horario'),
    # CRUD Especialista
    path('especialistas/', main_views.lista_especialistas, name='lista_especialistas'),
    path('especialista/<int:pk>/', main_views.detalle_especialista, name='detalle_especialista'),
    path('especialista/nuevo/', main_views.crear_especialista, name='crear_especialista'),
    path('especialista/<int:pk>/editar/', main_views.editar_especialista, name='editar_especialista'),
    path('especialista/<int:pk>/eliminar/', main_views.eliminar_especialista, name='eliminar_especialista'),
    # AJAX URLs
    path('cargar_especialistas/', main_views.cargar_especialistas, name='cargar_especialistas'),
    # API_CRUD
    path('api/', include(router.urls)),
    # Administrador URLs 
    path('admin-panel/dashboard/', main_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/manage_users/create/', main_views.admin_create_user, name='admin_create_user'),
    path('admin-panel/manage_users/modify/', main_views.admin_modify_user, name='admin_modify_user'),
    path('admin-panel/assign_schedules/', main_views.admin_assign_schedules, name='admin_assign_schedules'),
    path('admin-panel/view_reports/', main_views.admin_view_reports, name='admin_view_reports'),
    # Mejora de experiencia de usuario
    path('nosotros/', main_views.nosotros, name='nosotros'),
    path('psicologia/', main_views.psicologia, name='psicologia'),
    path('dental/', main_views.dental, name='dental'),
    path('medicina_general/', main_views.medicina_general, name='medicina_general'),
    path('salud_mental/', main_views.salud_mental, name='salud_mental'),
    # Mejorar Reserva de hora Cliente
    path('cli-areas/', views.areas, name='areas'),
    path('calendario/', views.calendario, name='calendario'),
    path('obtener_dias_disponibles/<str:area>/', views.obtener_dias_disponibles, name='obtener_dias_disponibles'),
    path('detalles_horarios/', views.detalles_horarios, name='detalles_horarios'),
    path('reserva/<int:horario_id>/', views.reserva2, name='reserva2'),
    path('confirmacion_reserva/<int:reserva_id>/', views.confirmacion_reserva, name='confirmacion_reserva'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('historial_medico/', views.historial_medico, name='historial_medico'),
    path('resultado_examenes/', views.resultado_examenes, name='resultado_examenes'),
    path('historial_reservas/', views.historial_reservas, name='historial_reservas'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    # Mejora Especialista
    path('esp-dashboard/', views.esp_dashboard, name='esp_dashboard'),
    path('calendario-especialista/', views.calendario_especialista, name='calendario_especialista'),
    path('obtener-dias-disponibles-especialista/', views.obtener_dias_disponibles_especialista, name='obtener_dias_disponibles_especialista'),
    path('desactivar-horario/<int:horario_id>/', views.desactivar_horario, name='desactivar_horario'),
    path('cancelar-cita/<int:reserva_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('reagendar-cita/<int:reserva_id>/', views.reagendar_cita, name='reagendar_cita'),
    path('activar-horario/<int:horario_id>/', views.activar_horario, name='activar_horario'),
    path('detalle-jornada-laboral/<str:fecha>/', views.detalle_jornada_laboral, name='detalle_jornada_laboral'),
    path('detalles_horarios2/<str:periodo>/', views.detalles_horarios2, name='detalles_horarios2'),
    path('buscar-pacientes/', views.buscar_pacientes, name='buscar_pacientes'),
    path('resultados-busqueda-pacientes/', views.resultados_busqueda_pacientes, name='resultados_busqueda_pacientes'),
    path('confirmar-cita/<int:reserva_id>/', views.confirmar_cita, name='confirmar_cita'),
    path('solucionar-cita/<int:reserva_id>/', views.solucionar_cita, name='solucionar_cita'),
    path('citas-confirmadas/', views.citas_confirmadas, name='citas_confirmadas'),
    path('confirmar-reagendamiento/<int:reserva_id>/', views.confirmar_reagendamiento, name='confirmar_reagendamiento'),
    path('rechazar-reagendamiento/<int:reserva_id>/', views.rechazar_reagendamiento, name='rechazar_reagendamiento'),
    path('citas_totales/', views.citas_totales, name='citas_totales'),
    # Descarga PDF
    path('generate_pdf/<int:reserva_id>/', views.generate_pdf, name='generate_pdf'),
    # Nuevas URLs para redirecciones
    path('citas_hoy/', views.citas_hoy, name='citas_hoy'),
    path('citas_semana/', views.citas_semana, name='citas_semana'),
    path('citas_mes/', views.citas_mes, name='citas_mes'),
    path('citas_confirmadas/', views.citas_confirmadas, name='citas_confirmadas'),
    #calificacion
    path('calificaciones/', ListaCalificacionesView.as_view(), name='lista_calificaciones'),
]
