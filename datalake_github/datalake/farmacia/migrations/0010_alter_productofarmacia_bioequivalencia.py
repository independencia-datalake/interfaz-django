# Generated by Django 3.2.8 on 2022-10-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmacia', '0009_auto_20221025_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productofarmacia',
            name='bioequivalencia',
            field=models.CharField(blank=True, choices=[('Si', 'True'), ('No', 'False')], max_length=5, null=True),
        ),
    ]