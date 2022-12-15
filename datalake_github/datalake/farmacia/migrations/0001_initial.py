# Generated by Django 3.2.8 on 2022-12-11 23:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('farmaceuta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Profesional')),
            ],
            options={
                'verbose_name': 'Comprobante Venta',
                'verbose_name_plural': 'Comprobantes de Venta',
            },
        ),
        migrations.CreateModel(
            name='Laboratorios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_laboratorio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre del Laboratorio')),
            ],
            options={
                'verbose_name': 'Laboratorio',
                'verbose_name_plural': 'Laboratorios',
            },
        ),
        migrations.CreateModel(
            name='ProductoFarmacia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca_producto', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre del Producto')),
                ('proveedor', models.CharField(blank=True, max_length=25, null=True, verbose_name='Proveedor')),
                ('p_a', models.CharField(blank=True, max_length=200, null=True, verbose_name='Componente Activo')),
                ('dosis', models.CharField(blank=True, max_length=200, null=True, verbose_name='Dosis del Producto')),
                ('presentacion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Presentacion del Producto')),
                ('precio', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Precio Producto')),
                ('cenabast', models.BooleanField(blank=True, default=False, null=True, verbose_name='Cenabast')),
                ('bioequivalencia', models.BooleanField(blank=True, default=False, null=True, verbose_name='Bioequivalencia')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farmacia.laboratorios', verbose_name='Laboratorio')),
            ],
            options={
                'verbose_name': 'Producto Farmacia',
                'verbose_name_plural': 'Productos de Farmacia',
                'ordering': ['marca_producto', 'dosis'],
            },
        ),
        migrations.CreateModel(
            name='Recetas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receta', models.FileField(blank=True, null=True, upload_to='farmacia/receta_medica/%Y/%m/%d/')),
                ('comprobante_venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farmacia.comprobanteventa', verbose_name='Venta asociada')),
            ],
            options={
                'verbose_name': 'Receta Medica',
                'verbose_name_plural': 'Recetas Medicas',
            },
        ),
        migrations.CreateModel(
            name='ProductoVendido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad Vendida')),
                ('precio_venta', models.PositiveIntegerField(blank=True, null=True, verbose_name='Precio Producto de la Venta')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
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
