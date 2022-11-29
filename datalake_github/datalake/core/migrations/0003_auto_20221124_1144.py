# Generated by Django 3.2.8 on 2022-11-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20221121_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='comentarios',
            field=models.CharField(max_length=200, null=True, verbose_name='Comentarios '),
        ),
        migrations.AddField(
            model_name='persona',
            name='prevision',
            field=models.CharField(choices=[('FONASA', 'Fonasa'), ('DIPRECA-CAPREDENA', 'Dipreca-Capredena'), ('ISAPRE: BANMEDICA', 'Isapre: Banmedica'), ('ISAPRE: ISALUD', 'Isapre: Isalud'), ('ISAPRE: COLMENA', 'Isapre: Colmena'), ('ISAPRE: CONSALUD', 'Isapre: Consalud'), ('ISAPRE: CRUZBLANCA', 'Isapre: Cruz Blanca'), ('ISAPRE: CRUZ DEL NORTE', 'Isapre: Cruz del Norte'), ('ISAPRE: NUEVA MASVIDA', 'Isapre: Nueva Masvida'), ('ISAPRE: FUNDACION', 'Isapre: Fundacion'), ('ISAPRE: VIDA TRES', 'Isapre: Vida Tres'), ('ISAPRE: ESENCIAL', 'Isapre: Esencial'), ('NINGUNA', 'Ninguna')], default='NINGUNA', max_length=30, verbose_name='Prevision de Salud'),
        ),
    ]
