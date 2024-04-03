# Build
docker build -t hellotls .

# Run
docker run -p 443:443 -e TARGET="hello tls app" -e COLOR="blue" hellotls

# curl -k https://localhost

curl -k https://localhost
<h1 style="color: blue">Hello hello tls app</h1>~