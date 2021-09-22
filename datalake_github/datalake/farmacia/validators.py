from django.core.exceptions import ValidationError

PALABRAS_BLOQUEADAS = ['PUTO','MIERDA','PUTA']

def validacion_de_palabras(value):
    
    init_value = f"{value}".lower()
    init_items = set(init_value.split())
    bloqueo = set([x.lower() for x in PALABRAS_BLOQUEADAS])
    item_invalido = list(init_items & bloqueo)
    tiene_error = len(item_invalido) > 0

    if tiene_error:
        validaciones_error = []
        for i, invalido in enumerate(item_invalido):
            validaciones_error.append(ValidationError("%(value)s es una palabra bloqueada", params={'value': invalido}, code=f'palabra-bloqueada-{i}'))
        raise ValidationError(validaciones_error)
    return value
   

   