# Generated by Django 3.2.8 on 2022-11-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_remove_productoingresado_farmaceuta'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordeningresoproducto',
            name='estado',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Estado Ingreso'),
        ),
    ]