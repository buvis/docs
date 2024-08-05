## Use secret values in manifests directly

1. Define key-value pair in [cluster-secrets](https://github.com/buvis/clusters/blob/main/production/operations/flux-system/extras/cluster-secrets.yaml)
   ```bash
   sops flux-system/extras/cluster-secrets.yaml
   ```
2. Refer to the secret value in manifest file
   ```yaml
   password: ${SECRET_PASSWORD}
   ```

## Use secret values in manifests from a file

1. Create `secret.yaml`
   ```yaml
   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: oauth2-proxy-secrets
   type: Opaque
   stringData:
     clientID: "<secret_value>"
     clientSecret: "<secret_value>"
   ```
2. Include secrets into manifest
   ```yaml
   clientID:
   valueFrom:
     secretKeyRef:
     name: oauth2-proxy-secrets
     key: clientID
   ```
3. Encrypt the secrets before pushing (TODO: use pre-commit hook)
   ```bash
   sops --encrypt --in-place secret.yaml
   ```

## Wait for another helm release (dependency)

Some releases depend on others. You may get errors when reconciling such releases too early.

Flux will reconcile something only once something else it depends on is available when **dependsOn** is mentionned in helm release manifest. It can refer to a name of another helm release across all namespaces.

See [Flux documentation](https://fluxcd.io/docs/components/helm/helmreleases/)

### Example

```yaml
---
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: speedtest-exporter
  namespace: monitoring
spec:
  dependsOn:
    - name: kube-prometheus-stack
      namespace: monitoring
```

## Wait for another kustomization (dependency)

Some releases depend on other Flux Kustomization. If reconciled too early, it may result in unexpected errors.

## Example

Especially in case of databases, it is necessary to set the passwords that the clients are then using. When using variables substitution in Flux, it may happen that the referenced value isn't created yet and the database is then created with unexpected password. This can be solved by waiting for `flux-system-extras`.

- kustomization.yaml

```
---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
metadata:
  name: authentik
  namespace: flux-system
resources:
  - authentik.yaml
  - helmrelease.yaml
  - pvc.yaml
```

- authentik.yaml

```
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: authentik
  namespace: flux-system
spec:
  dependsOn:
    - name: flux-system-extras
  interval: 5m
  path: "./cluster-home/operations/security/authentik"
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  postBuild:
    substitute: {}
    substituteFrom:
      - kind: Secret
        name: cluster-secret-vars
      - kind: ConfigMap
        name: cluster-config
```
