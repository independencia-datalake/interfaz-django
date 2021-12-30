# Generated by Django 3.2.8 on 2021-12-29 14:34

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
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre Mascota')),
                ('sexo', models.CharField(choices=[('1', 'Hembra'), ('2', 'Macho')], default='1', max_length=1, verbose_name='Sexo de Mascota')),
                ('especie', models.CharField(choices=[('1', 'Canino'), ('2', 'Felino')], default='1', max_length=1, verbose_name='Especie de Mascota')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.persona', verbose_name='dueño')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad vecinal')),
            ],
            options={
                'verbose_name': 'Mascota',
                'verbose_name_plural': 'Mascotas',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='SeguridadDIMAP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_ingreso', models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')),
                ('estatus', models.CharField(choices=[('1', 'Pendiente'), ('2', 'Realizado'), ('3', 'Anulado')], default='1', max_length=1, verbose_name='Estatus')),
                ('ficha', models.CharField(default='0', max_length=40, verbose_name='Ficha de Ingreso')),
                ('tipo_denuncia', models.CharField(choices=[('1', 'Zoonosis'), ('2', 'Trm'), ('3', 'Higiene Ambiental')], max_length=1, verbose_name='Tipo de Denuncia')),
                ('text_denuncia', models.TextField(blank=True, verbose_name='Motivo Denuncia')),
                ('nombre', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre Denunciado')),
                ('apellido', models.CharField(blank=True, max_length=30, null=True, verbose_name='Apellido Denunciado')),
                ('calle', models.CharField(blank=True, max_length=30, null=True, verbose_name='Calle Denunciado')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numeración')),
                ('telefono', models.CharField(blank=True, max_length=30, null=True, verbose_name='Teléfono Denunciado')),
                ('f_visita', models.DateField(verbose_name='Fecha de visita inspeccion')),
                ('l_transgrsion', models.CharField(choices=[('1', 'Vía Pública'), ('2', 'Domicilio')], max_length=1, verbose_name='Lugar de Transgresión')),
                ('i_visita', models.CharField(choices=[('1', 'Inspector'), ('2', 'Profesional')], max_length=1, verbose_name='Visita Inspectiva')),
                ('obs_insp', models.TextField(blank=True, null=True, verbose_name='Observación Inspector')),
                ('cat_visita', models.CharField(blank=True, choices=[('1', 'Se Visita, Hay Contacto'), ('2', 'Se Visita, No Hay Contacto'), ('3', 'Otra')], default='', max_length=1, verbose_name='Categorización de Visita')),
                ('notificacion', models.CharField(blank=True, choices=[('1', 'Con Notificación'), ('2', 'Sin Notificación')], default='', max_length=1, verbose_name='Notificación')),
                ('n_notificacion', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de notificación')),
                ('respuesta', models.TextField(blank=True, verbose_name='Respuesta Denunciante')),
                ('img_respuesta', models.FileField(blank=True, null=True, upload_to='dimap/denuncia/%Y/%m/%d/')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.persona', verbose_name='Denunciante')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad Vecinal Demandado')),
            ],
            options={
                'verbose_name': 'Seguridad DIMAP',
                'verbose_name_plural': 'Seguridad DIMAP',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Procedimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estatus', models.CharField(choices=[('1', 'Pendiente'), ('2', 'Realizado'), ('3', 'Anulado')], default='1', max_length=1, verbose_name='Estatus')),
                ('f_ingreso', models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')),
                ('f_cirugia', models.DateField(verbose_name='Fecha de Cirugia')),
                ('clinica', models.CharField(choices=[('1', 'Municipalidad (movil)'), ('2', 'Particular')], default='1', max_length=1, verbose_name='Clinica')),
                ('asistencia', models.CharField(choices=[('1', 'Asiste'), ('2', 'No Asiste'), ('3', 'Pendiente de Hora')], default='3', max_length=1, verbose_name='Asistencia')),
                ('ejecucion_cirugia', models.CharField(blank=True, choices=[('1', 'Realizada'), ('2', 'Rechazada')], default='', max_length=1, verbose_name='Ejecución Cirugía')),
                ('motivo_rechazo', models.TextField(blank=True, verbose_name='Motivo Rechazo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dimap.mascota', verbose_name='Mascota')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad vecinal')),
            ],
        ),
        migrations.CreateModel(
            name='ControlPlaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estatus', models.CharField(choices=[('1', 'Pendiente'), ('2', 'Realizado'), ('3', 'Anulado')], default='1', max_length=1, verbose_name='Estatus')),
                ('f_ingreso', models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')),
                ('ficha', models.CharField(default='0', max_length=40, verbose_name='Folio ingreso')),
                ('tipo_control', models.CharField(choices=[('1', 'Desratizar'), ('2', 'Fumigar'), ('3', 'Sanitizar')], max_length=1, verbose_name='Tipo de Control')),
                ('f_coordinacion', models.DateField(verbose_name='Fecha de Coordinacion')),
                ('jornada_servicio', models.CharField(choices=[('1', 'Mañana'), ('2', 'Tarde')], max_length=1, verbose_name='Jornada')),
                ('f_operacion', models.DateField(blank=True, null=True, verbose_name='Fecha de Operacion')),
                ('producto', models.CharField(blank=True, choices=[('1', 'Ratamix'), ('2', 'Delta Max'), ('3', 'Duplalim')], max_length=1, null=True, verbose_name='Producto')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.persona', verbose_name='Persona')),
                ('uv', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.uv', verbose_name='Unidad vecinal')),
            ],
            options={
                'verbose_name': 'Control de Plaga',
                'verbose_name_plural': 'Control de Plagas',
                'ordering': ['created'],
            },
        ),
    ]
