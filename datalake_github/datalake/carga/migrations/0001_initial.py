# Generated by Django 3.2.8 on 2022-02-28 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargaDOM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(upload_to='carga/DOM/', verbose_name='Dom - Tramites y permisos')),
            ],
        ),
        migrations.CreateModel(
            name='CargaEmpresas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(upload_to='carga/empresas/', verbose_name='Empresas')),
            ],
        ),
        migrations.CreateModel(
            name='CargaEntregasPandemia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(upload_to='carga/pandemia/', verbose_name='Entrega Pandemia')),
            ],
        ),
        migrations.CreateModel(
            name='CargaExencionAseo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(upload_to='carga/exencion_aseo/', verbose_name='Exención pago derechos de aseo')),
            ],
        ),
        migrations.CreateModel(
            name='CargaLicenciasConducir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(upload_to='carga/patentes_vehiculares/', verbose_name='Patentes Vehiculares')),
            ],
        ),
        migrations.CreateModel(
            name='CargaPermisosCirculacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_producto', models.FileField(upload_to='carga/permiso_circulacion/', verbose_name='Permisos Circulacion')),
            ],
        ),
        migrations.CreateModel(
            name='PermisosCirculacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('calle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
        ),
        migrations.CreateModel(
            name='LicenciaConducir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.CharField(blank=True, max_length=200, null=True, verbose_name='Folio Licencia')),
                ('calle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('comuna', models.CharField(blank=True, max_length=200, null=True, verbose_name='Comuna')),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha Otorgamiento')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
            options={
                'verbose_name': 'licenciaconducir',
                'verbose_name_plural': 'licenciasconducir',
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='ExencionAseo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca_temporal', models.DateTimeField(blank=True, null=True, verbose_name='Marca Temporal')),
                ('tipo_documento', models.CharField(choices=[('RUT', 'Rut'), ('PASAPORTE', 'Pasaporte'), ('OTRO', 'Otro')], default='RUT', max_length=200, null=True, verbose_name='Tipo de Documento')),
                ('numero_identificacion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Número de Identidad')),
                ('nombres', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido Materno')),
                ('estado_civil', models.CharField(blank=True, max_length=500, null=True, verbose_name='Estado Civil')),
                ('ocupacion', models.CharField(blank=True, max_length=500, null=True, verbose_name='Ocupación')),
                ('tramo_rsh', models.PositiveSmallIntegerField(verbose_name='Tramo RSH')),
                ('calle', models.CharField(blank=True, max_length=500, null=True, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('complemento_direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Complemento de Dirección')),
                ('rol_propiedad', models.CharField(blank=True, max_length=500, null=True, verbose_name='Rol Propiedad')),
                ('telefono', models.CharField(blank=True, max_length=200, null=True, verbose_name='Teléfono')),
                ('paga_contribucion', models.CharField(choices=[('NO', 'No'), ('SI', 'Si'), ('OTRO', 'Otro')], max_length=200, null=True, verbose_name='Paga Contribucioens')),
                ('porcentaje_exencion', models.PositiveSmallIntegerField(verbose_name='Porcentaje de Exención')),
                ('causal', models.CharField(blank=True, max_length=200, null=True, verbose_name='Causal de Exención')),
                ('adj_docu', models.URLField(blank=True, max_length=1000, null=True, verbose_name='Adjuntar Documentos')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('serie', models.PositiveIntegerField(verbose_name='Serie')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
        ),
        migrations.CreateModel(
            name='EntregasPandemia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Numero ID')),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('tipo_identificacion', models.CharField(choices=[('RUT', 'Rut'), ('PASAPORTE', 'Pasaporte'), ('OTRO', 'Otro')], default='RUT', max_length=200, verbose_name='Tipo de Documento')),
                ('nombre_persona', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre Persona')),
                ('apellido_paterno', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido Materno')),
                ('telefono', models.CharField(blank=True, max_length=200, null=True, verbose_name='Teléfono')),
                ('calle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('complemento_direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Complemento de Dirección')),
                ('caja_mercaderia', models.PositiveIntegerField(blank=True, null=True, verbose_name='Caja Mercaderia')),
                ('pañal_adulto', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pañal Adulto')),
                ('pañal_niño_m', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pañal niño talla M')),
                ('pañal_niño_g', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pañal niño talla G')),
                ('pañal_niño_xg', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pañal niño talla XG')),
                ('pañal_niño_xxg', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pañal niño talla XXG')),
                ('leche_entera', models.PositiveIntegerField(blank=True, null=True, verbose_name='Leche entera')),
                ('leche_descremada', models.PositiveIntegerField(blank=True, null=True, verbose_name='Leche descremada')),
                ('nat_100', models.PositiveIntegerField(blank=True, null=True, verbose_name='NAT 100')),
                ('balon_gas', models.PositiveIntegerField(blank=True, null=True, verbose_name='Balon de gas 11 kg')),
                ('parafina', models.PositiveIntegerField(blank=True, null=True, verbose_name='Parafina')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
        ),
        migrations.CreateModel(
            name='Empresas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.PositiveIntegerField(blank=True, null=True, verbose_name='ROL')),
                ('razon_social', models.CharField(blank=True, max_length=60, verbose_name='Razon social')),
                ('rut', models.CharField(blank=True, max_length=200, verbose_name='Número de Identidad')),
                ('giro', models.CharField(blank=True, max_length=60, verbose_name='Giro')),
                ('calle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Avenida/Calle/Pasaje')),
                ('numeracion', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeracion')),
                ('tipo', models.CharField(max_length=200, null=True, verbose_name='Tipo Patente')),
                ('trabajadores_pais', models.PositiveIntegerField(blank=True, null=True, verbose_name='Trabajadores pais')),
                ('trabajadores_comuna', models.PositiveIntegerField(blank=True, null=True, verbose_name='Trabajadores Comuna')),
                ('trabajadores_patente', models.PositiveIntegerField(blank=True, null=True, verbose_name='Trabajadores Patente')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
            options={
                'verbose_name': 'empresas',
                'verbose_name_plural': 'empresas',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='DOM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tramite', models.CharField(blank=True, max_length=60, null=True, verbose_name='Tramite')),
                ('manzana', models.CharField(blank=True, max_length=200, null=True, verbose_name='Manzana')),
                ('predio', models.CharField(blank=True, max_length=200, null=True, verbose_name='Predio')),
                ('calle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('n_permiso', models.CharField(blank=True, max_length=200, null=True, verbose_name='Numero de Permiso')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
        ),
    ]