#validación cedula profesional
#Reliza el match de cedula para vaalidar titulación.
# ejecutar llamando el modulo y pasando como argumento el número de cedula.
import json
import sys
import requests


def getCedula(cedulaProfesional):
    url = "https://www.cedulaprofesional.sep.gob.mx/cedula/buscaCedulaJson.action"

    cedula = str(cedulaProfesional)

    payload = "json=%7B%22maxResult%22%3A%221000%22%2C%22nombre%22%3A%22%22%2C%22paterno%22%3A%22%22%2C%22materno%22%3A%22%22%2C%22idCedula%22%3A%22"+cedula+"%22%7D" 
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-Requested-With': 'XMLHttpReques',
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
    }

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

    response = requests.request("POST", url, headers=headers, data = payload)

    data = response.json()

    items = data['items']
    

    datos = dict();

    for item in items:
        datos['universidad'] = item["desins"]
        datos['titulo']      = item["titulo"]
        datos['cedula']      = item["idCedula"]
        datos['nombre']      = item["nombre"]
        datos['paterno']     = item["paterno"]
        datos['materno']     = item["materno"]
        if cedulaProfesional == str(item["idCedula"]):
            datos['status']  = "True"
        else:
            datos['status']  = "False"
    
    print(datos)
    
    return datos





if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None
    
    return_value = getCedula(arg)


#print(getCedula(cedulaProfesional = str(input("Introduce cedula:\n"))))
