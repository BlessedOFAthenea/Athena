# Generated by Django 5.1 on 2025-06-18 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0002_organizacion_comuna_organizacion_direccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizacion',
            name='activo',
            field=models.BooleanField(default=False, verbose_name='Activo'),
        ),
    ]
