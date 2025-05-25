## Démarrage du projet

1. **Appliquer le SecretStore ParameterStore :**
   ```sh
   kubectl apply -f lobembe/infra/postiz/parameterstore.yaml
   ```

2. **Appliquer les secrets :**
   ```sh
   kubectl apply -f lobembe/infra/postiz/secrets.yaml
   ```

3. **Installer l’application avec Helm :**
   ```sh
   helm install postiz-app -f custom-values.yml oci://ghcr.io/billmetangmo/postiz-helmchart/charts/postiz-app
   ```

**Remarque :**
Assurez-vous d’avoir `kubectl` et `helm` installés et configurés pour votre cluster Kubernetes.