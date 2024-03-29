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
            name='ClasificacionDelito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, verbose_name='Clasificacion de delito')),
            ],
            options={
                'verbose_name': 'Clasificación del delito',
                'verbose_name_plural': 'Clasificaciones de los delitos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Delito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Delito')),
                ('clasificacion_delito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguridad.clasificaciondelito', verbose_name='Clasificacion del delito')),
            ],
            options={
                'verbose_name': 'Delito',
                'verbose_name_plural': 'Delitos',
                'ordering': ['clasificacion_delito', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Denunciante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre')),
                ('apellido', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido')),
                ('telefono', models.CharField(blank=True, max_length=200, null=True, verbose_name='Teléfono denunciante')),
                ('correo', models.EmailField(blank=True, max_length=40, null=True, verbose_name='Correo electrónico')),
            ],
            options={
                'verbose_name': 'Denunciante',
                'verbose_name_plural': 'Denunciantes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LlamadoSeguridad',
            fields=[
                ('numero_requerimiento', models.AutoField(primary_key=True, serialize=False, verbose_name='Número de requerimiento')),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de ingreso')),
            ],
            options={
                'verbose_name': 'Llamado seguridad',
                'verbose_name_plural': 'Llamados de seguridad',
                'ordering': ['numero_requerimiento'],
            },
        ),
        migrations.CreateModel(
            name='Requerimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estatus', models.CharField(choices=[('1', 'Recepcionado'), ('2', 'Pendiente'), ('3', 'En Curso'), ('4', 'Resuelto')], default='1', max_length=1, verbose_name='Estatus')),
                ('via_ingreso', models.CharField(choices=[('1', 'Fono 1469'), ('2', 'Patrullaje Preventivo'), ('3', 'Patrullaje colaborativo (carabineros)'), ('4', 'Demanda espontánea'), ('5', 'Fiscalización'), ('6', 'Otro:_____')], default='1', max_length=1, verbose_name='Vía de Ingreso')),
                ('via_ingreso_otro', models.CharField(blank=True, max_length=200, null=True, verbose_name=' ')),
                ('delito_otro', models.TextField(blank=True, null=True, verbose_name='Comentario')),
                ('calle', models.CharField(max_length=200, verbose_name='Avenida/Calle/Pasaje')),
                ('numero', models.IntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('complemento_direccion', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento de Dirección')),
                ('interseccion', models.CharField(blank=True, max_length=50, null=True, verbose_name='Intersección')),
                ('prioridad', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], default='0', max_length=1, verbose_name='Prioridad')),
                ('resolucion', models.CharField(choices=[('1', 'Cursar infracción'), ('2', 'Proceso judicial'), ('3', 'Derivación Área Prevención'), ('4', 'Territorial'), ('5', 'Atención a Víctimas'), ('6', 'Convivencia'), ('7', 'Derivación Unidad especializada'), ('8', 'Intramunicipal ¿cuál?'), ('9', 'Extramunicipal ¿cuál?')], default='1', max_length=1, verbose_name='Forma de resolución del requerimiento')),
                ('resolucion_otro', models.CharField(blank=True, max_length=50, null=True, verbose_name='¿Cuál?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('delito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguridad.delito', verbose_name='Delito')),
                ('denunciante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguridad.denunciante', verbose_name='denunciante')),
                ('numero_requerimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguridad.llamadoseguridad', verbose_name='Número de requerimiento')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal')),
            ],
            options={
                'verbose_name': 'Requerimiento',
                'verbose_name_plural': 'Requerimientos',
                'ordering': ['numero_requerimiento'],
            },
        ),
    ]
