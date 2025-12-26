import requests

def get_weather(latitude: float, longitude: float):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m"
        "&hourly=precipitation_probability"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    return {
        "today_temp": data["current"]["temperature_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
        "rain_probability": (
            data["hourly"]["precipitation_probability"][0]
            if "hourly" in data else 0
        ),
        "today_short_forecast": "Derived from Open-Meteo"
    }
