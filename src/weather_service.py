import requests

class WeatherService:
    def __init__(self, lat=40.7128, lon=-74.0060): # Default to New York
        self.lat = lat
        self.lon = lon
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(self):
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current_weather": True
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("current_weather")
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None

if __name__ == "__main__":
    ws = WeatherService()
    print(ws.get_current_weather())
