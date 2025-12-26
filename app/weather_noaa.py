import requests

HEADERS = {
    "User-Agent": "AI-Soil-Advisor/1.0",
    "Accept": "application/geo+json"
}

def get_weather(latitude: float, longitude: float):
    point_url = f"https://api.weather.gov/points/{latitude},{longitude}"

    point_resp = requests.get(point_url, headers=HEADERS, timeout=10)
    point_resp.raise_for_status()

    forecast_url = point_resp.json()["properties"]["forecast"]

    forecast_resp = requests.get(forecast_url, headers=HEADERS, timeout=10)
    forecast_resp.raise_for_status()

    today = forecast_resp.json()["properties"]["periods"][0]

    return {
        "today_temp": today["temperature"],
        "today_short_forecast": today["shortForecast"],
        "rain_probability": today.get("probabilityOfPrecipitation", {}).get("value", 0),
        "wind_speed": today["windSpeed"]
    }
