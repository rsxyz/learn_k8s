from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# Get the URLs of the GreeterService and WeatherService from environment variables
greeter_service_url = os.getenv('GREETER_SERVICE_URL', 'http://greeter-service:5001')
weather_service_url = os.getenv('WEATHER_SERVICE_URL', 'http://weather-service:5002')
target = os.getenv('TARGET', 'v1')

@app.route('/')
def index():
    return f"Hello Service is running! {target}"

@app.route('/api/status')
def names():
    data = {"status": ["Service is started", "It is up.",target ]}
    return jsonify(data)

@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', 'World')
    greeting = requests.get(greeter_service_url + '/greet', params={'name': name}).json()["greeting"]
    weather_message = requests.get(weather_service_url + '/weather').json()["weather_message"]
    return jsonify({"message": f"{greeting}. {weather_message}!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
