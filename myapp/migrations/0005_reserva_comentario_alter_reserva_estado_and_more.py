# Generated by Django 5.0.4 on 2024-06-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_cliente_correo_alter_cliente_run_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='comentario',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(choices=[('asignado', 'Asignado'), ('solucionado', 'Solucionado'), ('cerrado', 'Cerrado')], default='asignado', max_length=20),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='nro_reserva',
            field=models.IntegerField(editable=False, unique=True),
        ),
    ]