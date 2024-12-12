from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

WEATHER_API_KEY = 'b0965a394df3b894a072f7dd09b5bb62'  # Replace with your actual WeatherAPI key

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/fetch_weather', methods=['POST'])
def fetch_weather():
    location = request.json.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return jsonify({
            'temperature': weather_data['current']['temp_c'],
            'humidity': weather_data['current']['humidity'],
            'rainfall': weather_data['current']['precip_mm']
        })
    return jsonify({'error': 'Failed to fetch weather data.'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
