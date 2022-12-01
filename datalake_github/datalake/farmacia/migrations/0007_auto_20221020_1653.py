# Generated by Django 3.2.8 on 2022-10-20 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farmacia', '0006_auto_20221020_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productoingresado',
            options={'ordering': ['-n_venta'], 'verbose_name': 'Producto Ingresado', 'verbose_name_plural': 'Productos Ingresados'},
        ),
        migrations.AddField(
            model_name='bodegavirtual',
            name='holgura',
            field=models.IntegerField(blank=True, null=True, verbose_name='Holgura del Stock'),
        ),
        migrations.CreateModel(
            name='OrdenIngresoProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farmacia.productofarmacia', verbose_name='Nombre Producto')),
            ],
            options={
                'verbose_name': 'Orden de Ingreso de Producto',
                'verbose_name_plural': 'Ordenes de Ingresos de Productos',
            },
        ),
        migrations.AlterField(
            model_name='productoingresado',
            name='n_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmacia.ordeningresoproducto'),
        ),
    ]