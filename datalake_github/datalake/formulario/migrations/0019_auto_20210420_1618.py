# Generated by Django 3.1.7 on 2021-04-20 20:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formulario', '0018_farmacia'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FormularioOMIL',
            new_name='FormularioBase',
        ),
    ]
