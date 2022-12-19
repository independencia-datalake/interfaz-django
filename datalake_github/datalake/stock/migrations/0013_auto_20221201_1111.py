
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_auto_20221123_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodegavirtual',
            name='stock',
            field= models.IntegerField(blank=True, null=True, verbose_name='Stock del producto'),
        ),
        migrations.AddField(
            model_name='bodegavirtual',
            name='stock_min',
            field=models.IntegerField(blank=True, null=True, verbose_name='Stock minimo del producto'),
        ),
        migrations.AddField(
            model_name='bodegavirtual',
            name='stock_max',
            field=models.IntegerField(blank=True, null=True, verbose_name='Stock maximo del producto'),
        ),
        migrations.RemoveField(
            model_name='bodegavirtual',
            name='stock_max',
        ),
        migrations.RemoveField(
            model_name='bodegavirtual',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='bodegavirtual',
            name='stock_min',
        ),
    ]
