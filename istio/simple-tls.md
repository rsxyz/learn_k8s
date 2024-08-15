apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: example-gateway
  namespace: test
spec:
  selector:
    istio: ingressgateway # Use Istio's default ingress gateway
  servers:
  - port:
      number: 443
      name: https-hello
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: hello-cert # Secret containing the TLS certificate
    hosts:
    - hello.example.com
  - port:
      number: 443
      name: https-greet
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: greet-cert # Secret containing the TLS certificate
    hosts:
    - greet.example.com

---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello-virtual-service
  namespace: test
spec:
  hosts:
  - hello.example.com
  gateways:
  - example-gateway
  http:
  - match:
    - uri:
        prefix: /hello1
    route:
    - destination:
        host: helloworld1.test.svc.cluster.local
        port:
          number: 8080
  - match:
    - uri:
        prefix: /hello2
    route:
    - destination:
        host: helloworld2.test.svc.cluster.local
        port:
          number: 8080

---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: greet-virtual-service
  namespace: test
spec:
  hosts:
  - greet.example.com
  gateways:
  - example-gateway
  http:
  - match:
    - uri:
        prefix: /greet1
    route:
    - destination:
        host: greetworld1.test.svc.cluster.local
        port:
          number: 8085
  - match:
    - uri:
        prefix: /greet2
    route:
    - destination:
        host: greetworld2.test.svc.cluster.local
        port:
          number: 8085

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: helloworld-destination-rule
  namespace: test
spec:
  host: helloworld1.test.svc.cluster.local
  trafficPolicy:
    tls:
      mode: SIMPLE
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: greetworld-destination-rule
  namespace: test
spec:
  host: greetworld1.test.svc.cluster.local
  trafficPolicy:
    tls:
      mode: SIMPLE

---

kubectl apply -f istio-tls-gateway.yaml -n test
---

Step 1: Generate Self-Signed Certificates
We'll use OpenSSL to generate the certificates.

Generate a Certificate for hello.example.com
bash
Copy code
# Create a private key
openssl genrsa -out hello.example.com.key 2048

# Create a certificate signing request (CSR)
openssl req -new -key hello.example.com.key -out hello.example.com.csr \
  -subj "/CN=hello.example.com/O=YourOrganization"

# Generate the self-signed certificate
openssl x509 -req -in hello.example.com.csr -signkey hello.example.com.key -out hello.example.com.crt -days 365
Generate a Certificate for greet.example.com
bash
Copy code
# Create a private key
openssl genrsa -out greet.example.com.key 2048

# Create a certificate signing request (CSR)
openssl req -new -key greet.example.com.key -out greet.example.com.csr \
  -subj "/CN=greet.example.com/O=YourOrganization"

# Generate the self-signed certificate
openssl x509 -req -in greet.example.com.csr -signkey greet.example.com.key -out greet.example.com.crt -days 365
Step 2: Create Kubernetes Secrets
Now, we'll create Kubernetes secrets in the test namespace for the certificates.

Create a Secret for hello.example.com
bash
Copy code
kubectl create secret tls hello-cert \
  --cert=hello.example.com.crt \
  --key=hello.example.com.key \
  -n test
Create a Secret for greet.example.com
bash
Copy code
kubectl create secret tls greet-cert \
  --cert=greet.example.com.crt \
  --key=greet.example.com.key \
  -n test
Step 3: Update the Istio Configuration
Make sure your Istio Gateway configuration references the correct secret names:

yaml
Copy code
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: example-gateway
  namespace: test
spec:
  selector:
    istio: ingressgateway # Use Istio's default ingress gateway
  servers:
  - port:
      number: 443
      name: https-hello
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: hello-cert # Secret containing the TLS certificate
    hosts:
    - hello.example.com
  - port:
      number: 443
      name: https-greet
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: greet-cert # Secret containing the TLS certificate
    hosts:
    - greet.example.com
Step 4: Apply the Configuration
If you haven't already applied your Istio configuration, do so now:

bash
Copy code
kubectl apply -f istio-tls-gateway.yaml -n test
Step 5: Verify the Certificates
To ensure the secrets were created successfully and are being used by Istio:

List the Secrets:

bash
Copy code
kubectl get secrets -n test
Check the Gateway and VirtualService:

bash
Copy code
kubectl get gateway,virtualservice -n test
Test the HTTPS Endpoints:
Use curl or a web browser to test the routes and confirm that the certificates are being presented correctly:

bash
Copy code
curl -v https://hello.example.com/hello1 --cacert hello.example.com.crt
curl -v https://greet.example.com/greet1 --cacert greet.example.com.crt

---

Yes, you can create a wildcard certificate for *.example.com to cover both hello.example.com and greet.example.com. This simplifies the certificate management since a single certificate can be used for multiple subdomains.

Step 1: Generate a Wildcard Certificate
Use OpenSSL to generate a wildcard certificate for *.example.com.

bash
Copy code
# Create a private key
openssl genrsa -out example.com.key 2048

# Create a certificate signing request (CSR)
openssl req -new -key example.com.key -out example.com.csr \
  -subj "/CN=*.example.com/O=YourOrganization"

# Generate the self-signed wildcard certificate
openssl x509 -req -in example.com.csr -signkey example.com.key -out example.com.crt -days 365
Step 2: Create a Kubernetes Secret
Store the wildcard certificate as a Kubernetes secret.

bash
Copy code
kubectl create secret tls example-cert \
  --cert=example.com.crt \
  --key=example.com.key \
  -n test
Step 3: Update the Istio Configuration
Modify your Istio Gateway to use the wildcard certificate for both hosts.

yaml
Copy code
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: example-gateway
  namespace: test
spec:
  selector:
    istio: ingressgateway # Use Istio's default ingress gateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: example-cert # Wildcard certificate secret
    hosts:
    - hello.example.com
    - greet.example.com
Step 4: Apply the Configuration
Apply the updated configuration:

bash
Copy code
kubectl apply -f istio-tls-gateway.yaml -n test
Step 5: Verify the Setup
Test the HTTPS endpoints to ensure they are correctly secured with the wildcard certificate:

bash
Copy code
curl -v https://hello.example.com/hello1 --cacert example.com.crt
curl -v https://greet.example.com/greet1 --cacert example.com.crt
Summary
By using a wildcard certificate for *.example.com, you can secure multiple subdomains with a single certificate, simplifying your configuration. The wildcard certificate will be applied to both hello.example.com and greet.example.com in your Istio setup.


