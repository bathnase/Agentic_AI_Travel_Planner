import requests

def get_weather(latitude, longitude, days):
    """
    Fetches daily max temperature using Open-Meteo API
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&daily=temperature_2m_max"
        "&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    temperatures = data["daily"]["temperature_2m_max"]
    return temperatures[:days]
