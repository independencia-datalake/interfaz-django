# Generated by Django 3.2.8 on 2021-12-14 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallesIndependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Calle ',
                'verbose_name_plural': 'Calles de Independencia',
                'ordering': ['calle'],
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_identificacion', models.CharField(choices=[('RUT', 'Rut'), ('PASAPORTE', 'Pasaporte'), ('OTRO', 'Otro')], default='RUT', max_length=30, verbose_name='Tipo de Documento')),
                ('numero_identificacion', models.CharField(blank=True, max_length=30, verbose_name='Número de Identidad')),
                ('nombre_persona', models.CharField(max_length=30, verbose_name='Nombre Persona')),
                ('apellido_paterno', models.CharField(max_length=30, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=30, verbose_name='Apellido Materno')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='UV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_uv', models.PositiveIntegerField(verbose_name='Numero de U.V.')),
            ],
            options={
                'verbose_name': 'Unidad Vecinal',
                'verbose_name_plural': 'Unidades Vecinales',
                'ordering': ['numero_uv'],
            },
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(blank=True, max_length=30, null=True, verbose_name='Teléfono')),
                ('tipo_telefono', models.CharField(choices=[('MOVIL', 'Movil'), ('CASA', 'Casa'), ('TRABAJO', 'Trabajo'), ('OTRO', 'Otro')], default='MOVIL', max_length=30, null=True, verbose_name='Tipo de Telefono')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.persona', verbose_name='Persona')),
            ],
            options={
                'verbose_name': 'Telefono Persona',
                'verbose_name_plural': 'Telefonos Personas',
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='persona',
            name='uv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal'),
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, null=True, verbose_name='Activo')),
                ('calle', models.CharField(max_length=30, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.PositiveIntegerField(verbose_name='Numeración')),
                ('complemento_direccion', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento de Dirección')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.persona', verbose_name='Persona')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.uv', verbose_name='UV')),
            ],
            options={
                'verbose_name': 'Dirrecion Persona',
                'verbose_name_plural': 'Direcciones Personas',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Correo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.EmailField(max_length=40, verbose_name='Email')),
                ('tipo_correo', models.CharField(choices=[('PERSONAL', 'Personal'), ('TRABAJO', 'Trabajo'), ('ESCUELA', 'Escuela'), ('OTRO', 'Otro')], default='PERSONAL', max_length=30, null=True, verbose_name='Tipo de Correo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.persona', verbose_name='Persona')),
            ],
            options={
                'verbose_name': 'Correo Persona',
                'verbose_name_plural': 'Correos Personas',
                'ordering': ['created'],
            },
        ),
    ]