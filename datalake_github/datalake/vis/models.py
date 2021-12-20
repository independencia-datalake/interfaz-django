from django.db import models

class VisFarmacia(models.Model):
    farmacia_archivo = models.FileField(upload_to='vis/data/farmacia/', verbose_name="Archivo Farmacia")

    def __str__(self):
        return f'{self.id}'
