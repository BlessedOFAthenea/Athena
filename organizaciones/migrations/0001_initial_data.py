from django.db import migrations
from django.core.management import call_command

def create_default_superuser(apps, schema_editor):
    # Llamar al comando personalizado
    call_command('create_default_superuser')

class Migration(migrations.Migration):
    dependencies = [
        ('organizaciones', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_superuser),
    ]