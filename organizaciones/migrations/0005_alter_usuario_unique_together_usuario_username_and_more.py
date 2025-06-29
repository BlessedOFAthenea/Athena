# Generated by Django 5.1 on 2025-06-24 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0004_organizacion_db_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usuario',
            unique_together={('organizacion', 'email')},
        ),
        migrations.AddField(
            model_name='usuario',
            name='username',
            field=models.CharField(default='', max_length=50, verbose_name='Nombre de Usuario'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='usuario',
            unique_together={('organizacion', 'email'), ('organizacion', 'username')},
        ),
    ]
