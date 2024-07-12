# Generated by Django 5.0.4 on 2024-06-07 02:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_cliente_especialidad_especialista_historialatencion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='run',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='correo',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='run',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='telefono',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='historialatencion',
            name='reserva',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.reserva'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='numero_reserva',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='nro_reserva',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='horariosatencion',
            unique_together={('fecha', 'especialista')},
        ),
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together={('cliente', 'horario_atencion')},
        ),
    ]
