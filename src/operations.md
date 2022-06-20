## Upgrade

### Flux

This is automated using [Github Action](https://github.com/buvis/clusters/blob/main/.github/workflows/update-flux-production.yaml).

### Nodes

1. Determine latest k3s version at [k3s release channels](https://update.k3s.io/v1-release/channels)
2. Update the version in [ansible group vars - k3s_version](https://github.com/buvis/clusters/blob/main/production/infrastructure/ansible/group_vars/all/all.yaml)
3. Run `buvis-upgrade` provided by [buvis dotfiles](https://github.com/buvis/home)

## Recreate

### Backup

1. Go to Longhorn UI and take note of volume names and size which you want to restore into recreated cluster
2. Check that daily backup is available for volumes from step 1
3. Perform application specific backup for the applications considered critical
    - home-assistant
    - linkace
    - monica
4. Scale down the deployments with fresh data and trigger a backup

### Destroy

Run `make destroy` in cluster's directory.

### Bootstrap

1. Set workstation's DNS to 1.1.1.1, because Blocky isn't running
2. Run `make install` in cluster's directory.

## Usage

### Use secret values in manifests directly
1. Define key-value pair in [cluster-secrets](https://github.com/buvis/clusters/blob/main/production/operations/flux-system/extras/cluster-secrets.yaml)
    ```bash
    sops flux-system/extras/cluster-secrets.yaml
    ```
2. Refer to the secret value in manifest file
    ``` yaml
    password: ${SECRET_PASSWORD}
    ```

### Use secret values in manifests from a file
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
    ``` yaml
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

### Wait for another helm release (dependency)
Some releases depend on others. You may get errors when reconciling such releases too early.

Flux will reconcile something only once something else it depends on is available when **dependsOn** is mentionned in helm release manifest. It can refer to a name of another helm release across all namespaces.

See [Flux documentation](https://fluxcd.io/docs/components/helm/helmreleases/)

#### Example

```yaml
---
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
name: longhorn
namespace: longhorn-system
spec:
dependsOn:
- name: ingress-nginx
    namespace: kube-system
- name: oauth2-proxy
    namespace: kube-system
- name: cert-manager
    namespace: kube-system
```

## Troubleshooting

### Flux can't reconcile a helmrelease
- Get status of all helmreleases
    ```bash
    flux get helmreleases --all-namespaces
    ```
    or shorter
    ```bash
    flux get hr -A
    ```
- Make sure that sources can be accessed (as there might be typos)
    ```bash
    flux get sources helm -A
    flux get sources git -A
    flux get sources chart -A
    ```
- Get more information on helm release
    ```bash
    kubectl describe helmrelease <RELEASE_NAME> -n <RELEASE_NAMESPACE>
    ```
- Restart when Flux gave up
    ```bash
    flux resume hr <RELEASE_NAME> -n <RELEASE_NAMESPACE>
    ```

### Get CPU temperature in Proxmox for Asus PN50

Look at k10temp-pci-00c3 in the output of `sensors` command.
