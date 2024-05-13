# build
```sh
docker build -t weather_service .
docker tag weather_service:latest rsxyz123/weather_service:latest
docker push rsxyz123/weather_service_latest
```

# Mount path to certs tls.crt and tls.key and mount to /certs inside the container
```sh
docker run -v <PATH TO CERTS tls.crt and tls.key>:/certs  -e TLS_CERT=/certs/tls.crt -e S_KEY=/certs/tls.key -p 443:443 weather_service 

https://localhost
https://localhost/weather
https://localhost/api/status
http://localhost:5002 if certs are not used

```