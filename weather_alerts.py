import requests

def get_weather_alerts(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    # Replace 'your_actual_openweather_api_key' with your actual OpenWeather API key
    weather_api_key = '4105e115781bcc407e5980d20cd0d5d6'
    location = input("Enter your location: ")
    weather_data = get_weather_alerts(weather_api_key, location)
    print(weather_data)

if __name__ == "__main__":
    main()
