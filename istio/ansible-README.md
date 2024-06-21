---
- name: Create temporary file
  tempfile:
    suffix: .helm_values.yaml
  register: helm_values_file

- name: Template Helm values file
  template:
    src: "values-{{ env }}.yaml.j2"
    dest: "{{ helm_values_file.path }}"

- name: Deploy istio-base using Helm
  kubernetes.core.helm:
    name: istio-base
    chart_ref: roles/istio/files/istio-base-cht-1.21.1.tgz
    release_namespace: istio-system
    create_namespace: true
    state: present
    wait: yes

- name: Deploy istiod using Helm
  kubernetes.core.helm:
    name: istiod
    chart_ref: roles/istio/files/istiod-cht-1.21.1.tgz
    release_namespace: istio-system
    create_namespace: true
    state: present
    wait: yes

- name: Deploy istio-ingressgateway using Helm
  kubernetes.core.helm:
    name: istio-ingressgateway
    chart_ref: roles/istio/files/istio-gateway-cht-1.21.1.tgz
    release_namespace: istio-ingress
    create_namespace: true
    values_files:
      - "{{ helm_values_file.path }}"
    state: present
    wait: yes
# deploy

---
- name: Deploy Helm charts
  hosts: all
  vars_files:
    - "../roles/istio/vars/{{ env }}.yaml"
  roles:
    - istio
