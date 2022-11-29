from random import randint

def calculadora_rut(rut):
    rut = str(rut)
    tiene_guion = False
    tiene_punto = False

    for caracter in rut:
        if caracter == '-':
            tiene_guion = True
        if caracter == '.':
            tiene_punto = True
    
    if not tiene_guion and not tiene_punto:
        return poner_punto_guion(rut)

    elif tiene_guion and not tiene_punto:
        nuevo_rut = rut.replace('-','')
        return poner_punto_guion(nuevo_rut)
    
    elif not tiene_guion and tiene_punto:
        nuevo_rut = rut.replace('.','')
        return poner_punto_guion(nuevo_rut)

    elif tiene_guion and tiene_punto:
        nuevo_rut = rut.replace('-','')
        nuevo_rut = nuevo_rut.replace('.','')
        return poner_punto_guion(nuevo_rut)


def poner_punto_guion(rut):
    if not rut:
        return randint(10, 10000)
    rut_con_guion = rut[:-1] + '-' + rut[-1]
    rut_resto = rut_con_guion.split('-')[0]
    rut_resto_invertido = rut_resto[::-1]
    contador = 0
    contador_largo_str = 0
    nuevo_rut_invertido = ''
    for caracter in rut_resto_invertido:
        nuevo_rut_invertido += caracter
        contador += 1
        contador_largo_str += 1
        if contador == 3 and contador_largo_str != len(rut_resto_invertido):
            nuevo_rut_invertido += '.'
            contador = 0
    nuevo_rut = nuevo_rut_invertido[::-1]
    rut_punto_guion = nuevo_rut + '-' + rut[-1]
    if len(rut) == 1:
        return rut
    else:
        return rut_punto_guion
