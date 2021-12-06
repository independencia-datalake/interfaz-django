from django.contrib.auth.models import User
from django.db import models

class Requerimiento(models.Model):
    n_requerimiento = models.PositiveIntegerField(null=True, verbose_name="Numero de requermineto")
    identidad = models.CharField(
        max_length=1,
        default='3',
        choices=(
            ('1','Identidad'),
            ('2','Seudonimo'),
            ('3','Anonimo')
            ),
        verbose_name='Identidad',
        )
    numero_identificacion = models.CharField(null=True, blank=True, max_length=30, verbose_name="Número de Identidad")
    nombre = models.CharField(null=True, blank=True, max_length=30,verbose_name='Nombre Denunciado')
    apellido = models.CharField(null=True, blank=True, max_length=30,verbose_name='Apellido Denunciado')
    calle = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(null=True, blank=True, verbose_name="Numeración")
    interseccion = models.CharField(max_length=50, verbose_name='Intersección',blank=True,null=True)
    delito_social = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ('1','Robo con violencia e intimidación'),
            ('2','Robo en lugar no habitado'),
            ('3','Hurto'),
            ('4','Robo por sorpresa'),
            ('5','Robo de vehículo'),
            ('6','Homicidio'),
            ('7','Violación'),
            ('8','Robo desde vehículo'),
            ),
        verbose_name='Delito de mayor connotación social',
        )
    violencia_intrafamiliar = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ('1','VIF contra mujer'),
            ('2','VIF contra hombre'),
            ('3','VIF contra NNA'),
            ('4','VIF contra adulto/a mayor'),
            ),
        verbose_name='Violencia Intrafamiliar',
        )
    incivilidades = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ('1','Amenaza'),
            ('2','Riñas callejeras'),
            ('3','Comercio informal'),
            ('4','Consumo de alcohol y/o drogas en vía pública'),
            ('5','Daños'),
            ('6','Desordenes'),
            ('7','Ruidos molestos'),
            ('8','Otro'),
            ),
        verbose_name='Incivilidades',
        )
    abuso_sexual = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ('1','Abusos sexuales'),
            ('2','Abusos sexuales mayor 14 años'),
            ('3','Abusos sexuales menor 14 años'),
            ('4','Otros delitos sexuales'),
            ),
        verbose_name='Abusos sexuales',
        )
    accidente = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ('1','Accidente de tránsito'),
            ('2','Incendio'),
            ),
        verbose_name='Accidentes e incendios',
        )
    comentario = models.TextField(null=True, blank=True, verbose_name='Comentario')
    prioridad = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Alta'),
            ('2','Media'),
            ('3','Leve')
            ),
        verbose_name='Prioridad',
        )
    resolucion = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Cursar infracción'),
            ('2','Proceso judicial'),
            ('3','Derivación Área Prevención'),
            ('4','Territorial'),
            ('5','Atención a Víctimas'),
            ('6','Convivencia'),
            ('7','Derivación Unidad especializada'),
            ('8','Intramunicipal ¿cuál?'),
            ('9','Extramunicipal ¿cuál?'),
            ),
        verbose_name='Forma de resolución del requerimiento',
        )
    des_resolucion = models.CharField(max_length=50, verbose_name='¿Cuál?',blank=True,null=True)
    estatus = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Recepcionado'),
            ('2','Pendiente'),
            ('3','En Curso'),
            ('4','Resuelto'),
            ),
        verbose_name='Estatus',
        )
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Autor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)
