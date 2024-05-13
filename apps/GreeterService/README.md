
# build
```sh
docker build -t greeter_service .
docker tag greeter_service:latest rsxyz123/greeter_service:latest
docker push rsxyz123/greeter_service_latest
```

# Mount path to certs tls.crt and tls.key and mount to /certs inside the container
```sh
docker run -v <PATH TO CERTS tls.crt and tls.key>:/certs  -e TLS_CERT=/certs/tls.crt -e S_KEY=/certs/tls.key -p 443:443 greeter_service 

https://localhost
https://localhost/greet
https://localhost/greet?name=Test
https://localhost/api/status
http://localhost:5001 if certs are not used

```