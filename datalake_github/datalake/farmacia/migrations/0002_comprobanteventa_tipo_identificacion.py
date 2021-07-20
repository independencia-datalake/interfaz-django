# Generated by Django 3.2.1 on 2021-07-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmacia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprobanteventa',
            name='tipo_identificacion',
            field=models.CharField(choices=[('Rut', 'Rut'), ('Pasaporte', 'Pasaporte'), ('Otro', 'Otro')], default='', max_length=30),
        ),
    ]
