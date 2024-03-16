from datetime import datetime
from requests import get

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}"
        r = get(url=url)
        weather_data = r.json()
        if weather_data["cod"] == "200":
            template = """
            Weather Report for {city}, {country}

            Coordinates: 🌐 {lat}, {lon}
            Current Weather: ☁️ {weather_desc}
            Temperature: 🌡️ {temp} °C (Feels Like: {feels_like} °C)
            Min/Max Temperature: {temp_min} °C / {temp_max} °C)
            Wind: 💨 {wind_speed} m/s (Direction: {wind_deg}°)
            Humidity: 💧 {humidity}%
            Visibility: 🌬️ {visibility} meters
            Timezone: ⏰ UTC{timezone}
            Sunrise: 🌅 {sunrise} | Sunset: 🌇 {sunset}
                """
            formatted_message = template.format(
                city=weather_data['name'],
                country=weather_data['sys']['country'],
                lon=round(weather_data['coord']['lon'], 2),
                lat=round(weather_data['coord']['lat'], 2),
                weather_desc=weather_data['weather'][0]['description'],
                temp=round(weather_data['main']['temp']-273.15, 2),
                feels_like=round(weather_data['main']['feels_like']-273.15, 2),
                temp_min=round(weather_data['main']['temp_min']-273.15, 2),
                temp_max=round(weather_data['main']['temp_max']-273.15, 2),
                wind_speed=round(weather_data['wind']['speed'], 2),
                wind_deg=weather_data['wind']['deg'],
                humidity=weather_data['main']['humidity'],
                visibility=weather_data['visibility'],
                timezone=weather_data['timezone'] // 3600,
                sunrise=datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M'),
                sunset=datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
            )
            return formatted_message
        elif weather_data["cod"] == "404":
            return weather_data["message"]

    except Exception as e:
        return str(e)