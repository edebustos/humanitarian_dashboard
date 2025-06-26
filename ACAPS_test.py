import requests

# --- ¡ACCIÓN CLAVE! ---
# Pon aquí el token que te dio ACAPS.
# Este es el token que me proporcionaste anteriormente.
ACAPS_TOKEN = "a10d34ede6b3841f18cb72035365cdc680de1072"

# Según los ejemplos de la API de ACAPS, la autenticación se hace
# pasando el token en la cabecera 'Authorization'.
headers = {
    'Authorization': f'Token {ACAPS_TOKEN}'
}

# La URL del endpoint al que queremos acceder. Vamos a pedir las crisis de Ucrania.
url = "https://api.acaps.org/api/v1/crisis"
params = {
    'country': 'Ukraine',
    'limit': 5
}

print(f"▶️  Intentando conectar a ACAPS con el token...")
print(f"   URL: {url}")
print(f"   Cabeceras: {headers}")

try:
    # Hacemos la petición GET con las cabeceras de autenticación
    response = requests.get(url, headers=headers, params=params, timeout=20)

    # raise_for_status() lanzará un error si la respuesta es 4xx o 5xx
    response.raise_for_status()

    # Si todo va bien, la conexión es exitosa.
    print("\n✅ ¡CONEXIÓN EXITOSA! La API de ACAPS ha aceptado el token.")
    print("   Datos recibidos:")
    # Imprimimos los resultados para verlos
    print(response.json())

except requests.exceptions.HTTPError as err:
    # Si la API nos rechaza, imprime el porqué
    print("\n❌ ¡ERROR! La API ha rechazado la petición.")
    print(f"   Status Code: {err.response.status_code}")
    print(f"   Respuesta del servidor: {err.response.text}")

except requests.exceptions.RequestException as err:
    # Si hay un error de red (timeout, etc.)
    print(f"\n❌ Error de conexión de red: {err}")

