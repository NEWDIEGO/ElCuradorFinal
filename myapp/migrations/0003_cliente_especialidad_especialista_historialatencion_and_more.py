# Generated by Django 5.0.4 on 2024-06-04 03:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_authgroup_authgrouppermissions_authpermission_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('genero', models.CharField(max_length=1)),
                ('prevision', models.CharField(choices=[('Fonasa', 'Fonasa'), ('Isapre', 'Isapre'), ('Colmena', 'Colmena')], max_length=20)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('genero', models.CharField(max_length=1)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.especialidad')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialAtencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('comentario', models.CharField(max_length=255)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.cliente')),
                ('especialista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.especialista')),
            ],
        ),
        migrations.CreateModel(
            name='HorariosAtencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(max_length=20)),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('duracion_cita', models.IntegerField()),
                ('especialista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.especialista')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_reserva', models.IntegerField()),
                ('fecha', models.DateField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('especialista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.especialista')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_reserva', models.IntegerField()),
                ('agendar_hora', models.DateTimeField()),
                ('estado', models.BooleanField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.cliente')),
                ('horario_atencion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.horariosatencion')),
            ],
        ),
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.DeleteModel(
            name='MyappCliente',
        ),
        migrations.DeleteModel(
            name='MyappEspecialidad',
        ),
        migrations.DeleteModel(
            name='MyappEspecialista',
        ),
        migrations.DeleteModel(
            name='MyappHistorialatencion',
        ),
        migrations.DeleteModel(
            name='MyappHorariosatencion',
        ),
        migrations.DeleteModel(
            name='MyappPago',
        ),
        migrations.DeleteModel(
            name='MyappReserva',
        ),
        migrations.AddField(
            model_name='historialatencion',
            name='reserva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.reserva'),
        ),
    ]
