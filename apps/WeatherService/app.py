from flask import Flask, jsonify
import random
import os


app = Flask(__name__)

# Check if certificate and key paths are provided as environment variables
certificate_path = os.environ.get('TLS_CERT')
key_path = os.environ.get('TLS_KEY')
print(f"certificate_path={certificate_path}, key_path={key_path}")
target = os.getenv('TARGET', 'v1')

# Define functions to start HTTP and HTTPS servers
def start_http_server():
    app.run(host='0.0.0.0', port=5002, debug=True)

def start_https_server():
    if certificate_path and key_path:
        # Create HTTPS server with provided certificate and key
        app.run(host='0.0.0.0', port=443, debug=True, ssl_context=(certificate_path, key_path))
    else:
        print("Certificate and key paths not provided. HTTPS server cannot be started.")



weather_messages = [
    "It's sunny today!",
    "Expect showers later today.",
    "Wrap up warm, it's cold outside.",
    "Windy weather expected.",
    "Clear skies tonight."
]

# Create HTTP server
@app.route('/')
def index():
    return f"Weather Service is running! {target}"

@app.route('/weather', methods=['GET'])
def weather():
    message = random.choice(weather_messages) + " " + target
    return jsonify({"weather_message": message})

@app.route('/api/status')
def names():
    data = {"status": ["Service is started", "It is up.",target ]}
    return jsonify(data)

# Run HTTP or HTTPS server based on environment variables
if __name__ == '__main__':
    if certificate_path and key_path:
        print("start https")
        start_https_server()  # Start HTTPS server
        start_http_server()  # Start HTTP server
    else:
        print("start http")
        start_http_server()  # Start only HTTP server

