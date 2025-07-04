
from django.shortcuts import render
from .api_client import WorldBankClient, IMFClient, ACAPSClient
import json

def dashboard_view(request, country_code='UKR'):
    """
    Vista principal que obtiene datos de múltiples APIs, incluyendo ACAPS,
    y los muestra en el dashboard.
    """
    wb_client = WorldBankClient()
    imf_client = IMFClient()
    acaps_client = ACAPSClient(token="a10d34ede6b3841f18cb72035365cdc680de1072")

    countries = wb_client.get_countries()
    selected_country_data = next((c for c in countries if c['code'] == country_code), None)

    population_data = wb_client.get_indicator_data(country_code, 'SP.POP.TOTL')
    gdp_data = wb_client.get_indicator_data(country_code, 'NY.GDP.PCAP.CD')
    gdp_growth_data = imf_client.get_real_gdp_growth(country_code)

    acaps_crisis_data = []
    if selected_country_data and 'name' in selected_country_data:
        try:
            acaps_crisis_data = acaps_client.get_crisis_info(selected_country_data['name'])
        except Exception:
            acaps_crisis_data = []

    # Validaciones para evitar errores si los datos están vacíos o mal formateados
    latest_population = (
        population_data[-1][1] if population_data and isinstance(population_data[-1], (list, tuple)) and len(population_data[-1]) > 1
        else 'N/A'
    )
    latest_gdp = (
        gdp_data[-1][1] if gdp_data and isinstance(gdp_data[-1], (list, tuple)) and len(gdp_data[-1]) > 1
        else 'N/A'
    )

    context = {
        'countries': countries,
        'selected_country': selected_country_data,
        'latest_population': latest_population,
        'latest_gdp': latest_gdp,
        'acaps_crises': acaps_crisis_data,
        'population_chart': {
            'labels': json.dumps([d[0] for d in population_data]) if population_data else '[]',
            'data': json.dumps([d[1] for d in population_data]) if population_data else '[]',
        },
        'gdp_chart': {
            'labels': json.dumps([d[0] for d in gdp_data]) if gdp_data else '[]',
            'data': json.dumps([d[1] for d in gdp_data]) if gdp_data else '[]',
        },
        'gdp_growth_chart': {
            'labels': json.dumps([d[0] for d in gdp_growth_data]) if gdp_growth_data else '[]',
            'data': json.dumps([d[1] for d in gdp_growth_data]) if gdp_growth_data else '[]',
        },
    }

    return render(request, 'dashboard/dashboard.html', context)
