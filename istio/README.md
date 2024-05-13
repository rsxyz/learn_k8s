kubectl create -n istio-ingress \
secret tls app1-tls-credential \
--key=app1_key.pem \
--cert=app1_cert.pem 

kubectl describe secret app1-tls-credential -n istio-ingress
Name:         app1-tls-credential
Namespace:    istio-ingress
Labels:       <none>
Annotations:  <none>

Type:  kubernetes.io/tls

Data
====
tls.crt:  1009 bytes
tls.key:  1704 bytes


curl  -k -HHost:app1.techguru.net --resolve "app1.techguru.net:443:172.18.255.200"   "https://app1.techguru.net:443"
Hello v1!