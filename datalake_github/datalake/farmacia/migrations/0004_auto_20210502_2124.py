# Generated by Django 3.1.7 on 2021-05-03 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmacia', '0003_auto_20210427_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productovendido',
            options={'ordering': ['-n_venta'], 'verbose_name': 'Producto Vendido', 'verbose_name_plural': 'Productos Vendidos'},
        ),
    ]
