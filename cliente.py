import requests

api_url = "http://127.0.0.1:5000/api/datos/7839"
# capturamos la respuesta


response = requests.get(api_url)
# convertimos la respuesta a objeto diccionario


empleado = response.json()

print(empleado["Apellido"])
print(empleado["Oficio"])
print(empleado["Salario"])