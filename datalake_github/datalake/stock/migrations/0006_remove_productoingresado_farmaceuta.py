# Generated by Django 3.2.8 on 2022-11-02 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_alter_productomermado_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoingresado',
            name='farmaceuta',
        ),
    ]
