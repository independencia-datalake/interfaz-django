# Generated by Django 3.2.8 on 2022-02-25 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(blank=True, null=True, upload_to='farmacia/carga_producto/')),
            ],
        ),
        migrations.CreateModel(
            name='ComprobanteVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receta', models.FileField(blank=True, null=True, upload_to='farmacia/receta_medica/%Y/%m/%d/')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.persona', verbose_name='Comprador')),
                ('farmaceuta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Profesional')),
            ],
            options={
                'verbose_name': 'Comprobante Venta',
                'verbose_name_plural': 'Comprobantes de Venta',
            },
        ),
        migrations.CreateModel(
            name='ProductoFarmacia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Activo')),
                ('marca_producto', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre del Producto')),
                ('p_a', models.CharField(blank=True, max_length=200, null=True, verbose_name='Componente Activo')),
                ('dosis', models.CharField(blank=True, max_length=200, null=True, verbose_name='Dosis del Producto')),
                ('presentacion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Presentacion del Producto')),
                ('f_ven', models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento')),
                ('precio', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Precio Producto')),
                ('n_lote', models.CharField(blank=True, max_length=200, null=True, verbose_name='Lote')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Producto Farmacia',
                'verbose_name_plural': 'Productos de Farmacia',
                'ordering': ['marca_producto', 'dosis'],
            },
        ),
        migrations.CreateModel(
            name='ProductoVendido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad Vendida')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('farmaceuta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('n_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmacia.comprobanteventa')),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farmacia.productofarmacia', verbose_name='Nombre Producto')),
            ],
            options={
                'verbose_name': 'Producto Vendido',
                'verbose_name_plural': 'Productos Vendidos',
                'ordering': ['-n_venta'],
            },
        ),
    ]
