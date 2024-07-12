# Generated by Django 5.0.4 on 2024-06-25 02:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_cliente_activo_alter_cliente_apellido_materno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('calificacion', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.cliente')),
                ('especialista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.especialista')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.reserva')),
            ],
        ),
    ]
