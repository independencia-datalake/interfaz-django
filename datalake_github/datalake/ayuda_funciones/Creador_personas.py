import pandas as pd
import json
from datetime import datetime
from rut import calculadora_rut

def crear_personas_base(path, path_salida):
    df = pd.read_excel(path)
    dic = df.to_dict('records')
    resultado_persona = []
    resultado_correo = []
    resultado_direccion = []
    resultado_telefono = []
    resultado_salud = []

    contador = 2
    for row in dic:
        persona_dic = {}
        correo_dic = {}
        direccion_dic = {}
        telefono_dic = {}
        salud_dic = {}

        ##      Persona

        persona_dic['model'] = "core.persona"
        persona_dic['pk'] = contador
        
        ##  uv
        if pd.isna(row['UV']):
            uv = 1
        else:
            uv = int(row['UV']) + 1
        ##  tipo_identificacion
        if pd.isna(row['RUT']):
            tipo_identificacion = "OTRO"
        elif row['RUT'] == '-' or row['RUT'] == 'BERNARDO':
            tipo_identificacion = "OTRO"
        else:
            tipo_identificacion = "RUT"
        ##  numero_identificacion
        if pd.isna(row['RUT']):
            rut = ''
        else:
            rut = calculadora_rut(row['RUT'])
        ##  nombre_persona
        if pd.isna(row['NOMBRES']):
            nombre_persona = ''
        else:
            nombre_persona = row['NOMBRES']
        ##  apellido_paterno
        if pd.isna(row['APELLIDOS']):
            apellido_paterno = ''
            apellido_materno = ''
        elif type(row['APELLIDOS']) == str:
            apellido_paterno = row['APELLIDOS'].split(' ')[0]
            ##  apellido_materno
            try:
                apellido_materno = row['APELLIDOS'].split(' ')[1]
            except:
                apellido_materno = ''
        else:
            apellido_paterno = row['APELLIDOS']
            apellido_materno = ''
        ##  estado_civil
        if pd.isna(row['ESTADO CIVIL']):
            estado_civil = None
        else:
            estado_civil = row['ESTADO CIVIL']
        ##  hijos
        if pd.isna(row['HIJOS']):
            hijos = 0
        else:
            try:
                hijos = int(row['HIJOS'])
            except:
                hijos = 0
        ##  nacionalidad
        if pd.isna(row['NACIONALIDAD']):
            nacionalidad = ''
        else:
            nacionalidad = row['NACIONALIDAD']
        ##  enfermedad
        if pd.isna(row['ENFERMEDAD']):
            enfermedad = ''
        else:
            enfermedad = row['ENFERMEDAD']
        ##  medicamento
        if pd.isna(row['MEDICAMENTO']):
            medicamento = ''
        else:
            medicamento = row['MEDICAMENTO']
        ##  lugar_de_atencion
        if pd.isna(row['LUGAR DE ATENCIÓN']):
            lugar_de_atencion = ''
        else:
            lugar_de_atencion = row['LUGAR DE ATENCIÓN']  
        ##  discapacidad
        if pd.isna(row['DISCAPACIDAD']):
            discapacidad = False
        elif row['DISCAPACIDAD'] == 'NO':
            discapacidad = False
        elif row['DISCAPACIDAD'] == 'SI':
            discapacidad = True
        else:
            discapacidad = True
        ##  certificado_compin
        if pd.isna(row['CERTIFICADO COMPIN']):
            certificado_compin = False
        elif row['CERTIFICADO COMPIN'] == 'NO':
            certificado_compin = False
        elif row['CERTIFICADO COMPIN'] == 'SI':
            certificado_compin = True
        else:
            certificado_compin = False
        ##  embarazo
        if pd.isna(row['EMBARAZO']):
            embarazo = False
        elif row['EMBARAZO'] == 'NO':
            embarazo = False
        elif row['EMBARAZO'] == 'SI':
            embarazo = True
        else:
            embarazo = False
        ##  certificado_embarazo
        if pd.isna(row['CERTIFICADO EMBARAZO']):
            certificado_embarazo = False
        elif row['CERTIFICADO EMBARAZO'] == 'NO':
            certificado_embarazo = False
        elif row['CERTIFICADO EMBARAZO'] == 'SI':
            certificado_embarazo = True
        else:
            certificado_embarazo = False
        ##  created
        marca_temporal = datetime.strptime(row['MARCA TEMPORAL'], '%Y-%m-%d %H:%M:%S.%f %z')
        created = datetime.strftime(marca_temporal, '%Y-%m-%dT00:00:00.000')
        
        persona_dic['fields'] = {
            "uv": uv,
            "tipo_identificacion": tipo_identificacion,
            "numero_identificacion": rut,
            "nombre_persona": nombre_persona,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "fecha_nacimiento": None,
            "estado_civil": estado_civil,
            "hijos": hijos,
            "nacionalidad": nacionalidad,
            "enfermedad": enfermedad,
            "medicamento": medicamento,
            "lugar_de_atencion": lugar_de_atencion,
            "discapacidad": discapacidad,
            "certificado_compin": certificado_compin,
            "embarazo": embarazo,
            "certificado_embarazo": certificado_embarazo,
            "created": created,
            "updated": created
        }
        
        resultado_persona.append(persona_dic)
        contador += 1


    # print(resultado_persona)

    with open("out/persona.json", "w") as write_file:
        json.dump(resultado_persona, write_file,indent=4) # encode dict into JSON
        

if __name__ == '__main__':
    print('partieron....')
    crear_personas_base('Usuarios.xlsx', './out/')

