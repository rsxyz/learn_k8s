
I have backend cluster api services api, ui, backend running on port 8080,5000,3829. I want to access these services using istio ingress https like https://example.com/svc/api https://example.com/svc/ui and https://example.com/svc/backend. example.com is already has dns entry mapped to istio-ingressgateway lb ip 10.11.12.13 and has a certificate for example.com/*.
I want sticky sessions for ui. How do I create various istio resources like Gateway, VS, DestinationRules for this?
ChatGPT
To configure Istio to route traffic to your backend services using HTTPS and implement sticky sessions for the UI service, you need to create several Istio resources: Gateway, VirtualService, and DestinationRule. Here are the steps to achieve this:

1. Gateway Configuration
The Gateway resource will configure the Istio ingress gateway to handle HTTPS traffic for your domain (example.com).

yaml
Copy code
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: example-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway # use Istio default ingress gateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: example-com-credential # must be the same as your secret
    hosts:
    - "example.com"
2. DestinationRules Configuration
The DestinationRule resource defines policies that apply to traffic intended for a service after routing has occurred. You can specify sticky sessions for the ui service here.

yaml
Copy code
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: example-destination-rule
spec:
  host: "*.svc.cluster.local"
  subsets:
  - name: api
    labels:
      app: api
  - name: ui
    labels:
      app: ui
  - name: backend
    labels:
      app: backend
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpCookie:
          name: ui-session-cookie
          ttl: 0s # Adjust TTL as needed for session duration
3. VirtualService Configuration
The VirtualService resource routes the incoming requests to the appropriate backend services based on the request path.

yaml
Copy code
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: example-virtualservice
spec:
  hosts:
  - "example.com"
  gateways:
  - example-gateway
  http:
  - match:
    - uri:
        prefix: "/svc/api"
    route:
    - destination:
        host: api.default.svc.cluster.local
        subset: api
        port:
          number: 8080
  - match:
    - uri:
        prefix: "/svc/ui"
    route:
    - destination:
        host: ui.default.svc.cluster.local
        subset: ui
        port:
          number: 5000
  - match:
    - uri:
        prefix: "/svc/backend"
    route:
    - destination:
        host: backend.default.svc.cluster.local
        subset: backend
        port:
          number: 3829
4. TLS Secret for HTTPS
Ensure you have created the Kubernetes secret (example-com-credential) for the TLS certificate used by the Istio ingress gateway.

sh
Copy code
kubectl create -n istio-system secret tls example-com-credential --key /path/to/tls.key --cert /path/to/tls.crt
Steps Summary:
Create a Gateway: To configure the ingress gateway to listen for HTTPS traffic on example.com.
Create DestinationRules: To define load balancing policies, including sticky sessions for the ui service.
Create a VirtualService: To route requests based on the URL path to the appropriate backend services.
Create a TLS Secret: To store the TLS certificate used by the Istio ingress gateway.
By following these steps, you will configure Istio to route HTTPS traffic to your backend services and implement sticky sessions for the UI service.







