# Generated by Django 5.0.6 on 2024-07-04 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_relatedmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='costo',
            field=models.DecimalField(blank=True, decimal_places=2, default=5000.0, max_digits=10, null=True),
        ),
    ]
