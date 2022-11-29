# Generated by Django 3.2.8 on 2022-11-24 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20221124_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonaInfoSalud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prevision', models.CharField(choices=[('FONASA', 'Fonasa'), ('DIPRECA-CAPREDENA', 'Dipreca-Capredena'), ('ISAPRE: BANMEDICA', 'Isapre: Banmedica'), ('ISAPRE: ISALUD', 'Isapre: Isalud'), ('ISAPRE: COLMENA', 'Isapre: Colmena'), ('ISAPRE: CONSALUD', 'Isapre: Consalud'), ('ISAPRE: CRUZBLANCA', 'Isapre: Cruz Blanca'), ('ISAPRE: CRUZ DEL NORTE', 'Isapre: Cruz del Norte'), ('ISAPRE: NUEVA MASVIDA', 'Isapre: Nueva Masvida'), ('ISAPRE: FUNDACION', 'Isapre: Fundacion'), ('ISAPRE: VIDA TRES', 'Isapre: Vida Tres'), ('ISAPRE: ESENCIAL', 'Isapre: Esencial'), ('NINGUNA', 'Ninguna')], default='NINGUNA', max_length=30, verbose_name='Prevision de Salud')),
                ('comentarios', models.CharField(max_length=200, null=True, verbose_name='Comentarios ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.persona', verbose_name='Persona')),
            ],
            options={
                'verbose_name': 'Informacion de salud Persona',
                'verbose_name_plural': 'Informacion de salud Personas',
                'ordering': ['created'],
            },
        ),
    ]
