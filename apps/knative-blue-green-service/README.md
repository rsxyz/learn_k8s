
### Specify a global domain name: 
- You can specify a global domain name if you do not want to specify a domain name for each Knative Service. After you complete the configuration, all Knative Services can use the specified global domain name.
```sh
kubectl patch configmap/config-domain -n knative-serving --type merge --patch "{\"data\":{\"127.0.0.1.sslip.io\":\"\"}}"
```