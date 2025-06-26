from django.shortcuts import render
from .api_client import WorldBankClient, IMFClient, ACAPSClient
import json


def dashboard_view(request, country_code='UKR'):  # País por defecto cambiado a Ucrania
    """
    Vista principal que obtiene datos de múltiples APIs, incluyendo ACAPS,
    y los muestra en el dashboard.
    """
    # Instanciamos nuestros clientes de API
    wb_client = WorldBankClient()
    imf_client = IMFClient()
    # Cliente de ACAPS con tu token.
    acaps_client = ACAPSClient(token="a10d34ede6b3841f18cb72035365cdc680de1072")

    # --- Obtener Datos ---
    countries = wb_client.get_countries()
    selected_country_data = next((c for c in countries if c['code'] == country_code), None)

    # Datos del Banco Mundial y FMI
    population_data = wb_client.get_indicator_data(country_code, 'SP.POP.TOTL')
    gdp_data = wb_client.get_indicator_data(country_code, 'NY.GDP.PCAP.CD')
    gdp_growth_data = imf_client.get_real_gdp_growth(country_code)

    # Datos de crisis de ACAPS
    acaps_crisis_data = []
    if selected_country_data:
        acaps_crisis_data = acaps_client.get_crisis_info(selected_country_data['name'])

    # --- Preparar Datos para la Plantilla ---
    latest_population = population_data[-1][1] if population_data else 'N/A'
    latest_gdp = gdp_data[-1][1] if gdp_data else 'N/A'

    context = {
        'countries': countries,
        'selected_country': selected_country_data,
        'latest_population': latest_population,
        'latest_gdp': latest_gdp,
        'acaps_crises': acaps_crisis_data,
        'population_chart': {
            'labels': json.dumps([d[0] for d in population_data]),
            'data': json.dumps([d[1] for d in population_data]),
        },
        'gdp_chart': {
            'labels': json.dumps([d[0] for d in gdp_data]),
            'data': json.dumps([d[1] for d in gdp_data]),
        },
        'gdp_growth_chart': {
            'labels': json.dumps([d[0] for d in gdp_growth_data]),
            'data': json.dumps([d[1] for d in gdp_growth_data]),
        },
    }

    return render(request, 'dashboard/dashboard.html', context)
