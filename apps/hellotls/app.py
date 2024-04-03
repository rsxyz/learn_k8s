import os
from flask import Flask

app = Flask(__name__)


def format_output(target, color):
    return f'<h1 style="color: {color}">Hello {target}</h1>'

@app.route('/')
def hello():
    target = os.getenv('TARGET', 'World')
    color = os.getenv('COLOR', 'black')
    return format_output(target, color)

if __name__ == '__main__':
    # Run HTTP server on port 8080
    #app.run(host='0.0.0.0', port=8080)
    
    # Run HTTPS server on port 443 with adhoc SSL certificate
    app.run(ssl_context='adhoc', host='0.0.0.0', port=443)
