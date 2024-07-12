from django.contrib import admin
from .models import *

# Registramos los modelos en el admin
admin.site.register(Especialista)
admin.site.register(Especialidad)
admin.site.register(Cliente)
admin.site.register(Pago)
admin.site.register(HorariosAtencion)
admin.site.register(Reserva)
admin.site.register(HistorialAtencion)
admin.site.register(Admin)
admin.site.register(Calificacion)