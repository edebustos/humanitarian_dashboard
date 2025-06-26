import requests

# --------------------------------------------------------------------------
# CLASE BASE PARA CLIENTES DE API
# --------------------------------------------------------------------------
class BaseApiClient:
    """Cliente base que maneja la creación de sesiones y errores comunes."""
    BASE_URL = ""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "GlobalDataDashboard/1.0"
        })

    def make_request(self, endpoint, params=None):
        """
        Realiza una petición GET y maneja errores comunes.
        La autenticación ahora se gestiona directamente en las cabeceras de la sesión.
        """
        try:
            url = f"{self.BASE_URL}{endpoint}"
            response = self.session.get(url, params=params, timeout=25)
            response.raise_for_status()
            print(f"✅ Petición exitosa para: {response.url}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ Error HTTP para {getattr(http_err.response, 'url', url)}: {http_err} | Response: {http_err.response.text}")
        except requests.exceptions.RequestException as req_err:
            print(f"❌ Error de Petición para {url}: {req_err}")
        return None

# --------------------------------------------------------------------------
# CLIENTE PARA LA API DE ACAPS (CON TOKEN AUTH)
# --------------------------------------------------------------------------
class ACAPSClient(BaseApiClient):
    """Cliente específico para la API de ACAPS usando Token Authentication."""
    BASE_URL = "https://api.acaps.org/api/v1/"

    def __init__(self, token):
        super().__init__()
        # Se añade el token a las cabeceras para autenticar cada petición.
        self.session.headers.update({
            'Authorization': f'Token {token}'
        })

    def get_crisis_info(self, country_name):
        """Obtiene la información más reciente de la crisis para un país."""
        params = {'country': country_name, 'limit': 5}
        data = self.make_request("crisis", params=params)
        return data['results'] if data and 'results' in data else []

# --------------------------------------------------------------------------
# CLIENTE PARA LA API DEL BANCO MUNDIAL
# --------------------------------------------------------------------------
class WorldBankClient(BaseApiClient):
    """Cliente específico para la API v2 del Banco Mundial."""
    BASE_URL = "https://api.worldbank.org/v2/"

    def get_countries(self):
        """Obtiene la lista de todos los países."""
        params = {'format': 'json', 'per_page': 350}
        data = self.make_request("country", params=params)
        if data and len(data) > 1:
            countries = [{'code': c['id'], 'name': c['name']} for c in data[1] if c['region']['value'] != "Aggregates"]
            return sorted(countries, key=lambda x: x['name'])
        return []

    def get_indicator_data(self, country_code, indicator_code, date_range="2010:2023"):
        """Obtiene datos de un indicador específico."""
        endpoint = f"country/{country_code}/indicator/{indicator_code}"
        params = {'format': 'json', 'date': date_range, 'per_page': 100}
        data = self.make_request(endpoint, params=params)
        if data and len(data) > 1 and data[1] is not None:
            return sorted([(d['date'], d['value']) for d in data[1] if d['value'] is not None], key=lambda x: x[0])
        return []

# --------------------------------------------------------------------------
# CLIENTE PARA LA API DEL FMI
# --------------------------------------------------------------------------
class IMFClient(BaseApiClient):
    """Cliente específico para la API DataMapper del FMI."""
    BASE_URL = "https://www.imf.org/external/datamapper/api/v1/"

    def get_real_gdp_growth(self, country_code):
        """Obtiene el crecimiento del PIB real."""
        endpoint = f"NGDP_RPCH/{country_code}"
        data = self.make_request(endpoint)
        if data and 'values' in data and country_code in data.get('values', {}):
            return sorted(data['values'][country_code].items())
        return []
