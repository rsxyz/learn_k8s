# Generate a private key
openssl genpkey -algorithm RSA -out tls.key

# Generate a certificate signing request
openssl req -new -key tls.key -out tls.csr

# Generate a self-signed certificate using the CSR and private key
openssl x509 -req -days 365 -in tls.csr -signkey tls.key -out tls.crt

# Optional: View the content of the generated certificate
openssl x509 -text -noout -in tls.crt

kubectl create secret tls nginx-tls-secret --cert=tls.crt --key=tls.key
kubectl create configmap nginx-config --from-file=default.conf
kubectl apply -f nginx-deploy.yaml
kubectl exec -it nginx-deployment-cf8c4c64f-t44tx -- /bin/sh
kubectl port-forward service/nginx-service 8443:443