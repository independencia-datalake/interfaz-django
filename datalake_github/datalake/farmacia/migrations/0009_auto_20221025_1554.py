# Generated by Django 3.2.8 on 2022-10-25 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmacia', '0008_auto_20221021_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productofarmacia',
            name='cenabast',
        ),
        migrations.RemoveField(
            model_name='productofarmacia',
            name='f_ven',
        ),
        migrations.RemoveField(
            model_name='productofarmacia',
            name='n_lote',
        ),
    ]