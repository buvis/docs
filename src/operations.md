## Update

### Flux

This is automated using [Github Action](https://github.com/buvis/clusters/blob/main/.github/workflows/update-flux-home.yaml). Sometimes the Flux components may fail to start due to outdated CRDs. In that case, make sure you are on the latest Flux CLI (`brew upgrade flux`) and run `buvisctl update flux`.

### Calico

When Calico releases a new version of `tigera-operator`:

1. Determine `<VERSION_TAG>`: [Calico Releases | GitHub](https://github.com/projectcalico/calico/releases)
2. Set temporary variable to use in following commands: `CALICO_VERSION=<VERSION_TAG>`
3. Get the updated manifest: `curl https://raw.githubusercontent.com/projectcalico/calico/$CALICO_VERSION/manifests/tigera-operator.yaml -O`
4. Initiate the upgrade: `kubectl apply -f tigera-operator.yaml`
5. Remove the manifest: `rm tigera-operator.yaml`
6. Update Talos installation patch: `vim infrastructure/talos/patch-all.yaml` and update `<VERSION_TAG>` in `/cluster/network/cni/custom/urls`
7. Update all machineconfigs: `talosctl -n $NODE_IPS edit machineconfig --mode=no-reboot` and update `<VERSION_TAG>` in `/cluster/network/cni/custom/urls`

### Talos

When siderolabs release a [new Talos version](https://github.com/siderolabs/talos/releases/latest) (`<VERSION_TAG>`):

1. Check for new [issues](https://github.com/siderolabs/talos/issues) to see if the new version is safe to use
2. Set temporary variable to use in following commands: `TALOS_VERSION=<VERSION_TAG>`
3. Update the client (`talosctl`)
  a. Download amd64 binary: `curl -Lo /usr/local/bin/talosctl https://github.com/siderolabs/talos/releases/download/$TALOS_VERSION/talosctl-$(uname -s | tr "[:upper:]" "[:lower:]")-amd64`
  b. Make it executable: `chmod +x /usr/local/bin/talosctl`
4. Update all machineconfigs to `iscsi-tools` [latest version](https://github.com/siderolabs/extensions/pkgs/container/iscsi-tools) at `.machine.install.extensions`: `talosctl -n $NODE_IPS edit machineconfig --mode=no-reboot`
5. Update the nodes one by one. Important: don't forget the `--preserve` flag, because you are in single-node control plane scenario: `talosctl upgrade --nodes <NODE_IP> --image ghcr.io/siderolabs/installer:$TALOS_VERSION --preserve`
6. Check nodes version: `talosctl -n $NODE_IPS version`

### Proxmox

1. Connect to Proxmox node: `ssh <NODE_NAME>`
2. Update packages: `apt update && apt dist-upgrade && apt autoremove`
3. Reboot: `reboot`

## Recreate

### Backup

1. Run backup job manually for every PVC: `buvisctl backup -n <NAMESPACE> <PVC>`
2. Perform application specific backup for the applications considered critical
    - home-assistant
    - linkace
    - monica

### Destroy

Run `buvisctl destroy` in cluster's directory.

### Bootstrap

1. Set workstation's DNS to 1.1.1.1, because Blocky isn't running
2. Update VM template:
    a. Connect to Proxmox node: `ssh <NODE_NAME>`
    b. Remove old Talos image: `rm talos-amd64.iso`
    c. Destroy the old VM template: `qm destroy 9000`
    d. Create new VM template by repeating [installation - Create VM template](installation.md#create-vm-template)
3. Make sure that GitHub PAT (stored in GITHUB_TOKEN environment variable) is still valid, and update it eventually
4. Run `buvisctl bootstrap` in cluster's directory.

### Restore

Repeat for every PVC: `buvisctl restore -n <NAMESPACE> <PVC>`. The list of available snapshots can be retrieved from [Kopia UI](http://10.11.0.44/snapshots).

#### MariaDB

After restore, pods running MariaDB won't start and report that "Access denied for user 'root'@'localhost'" in the log. This is because credentials were generated when cluster bootstrapped.
1. Delete *mariadb* Secret for this database
2. Delete MariaDB helm release: `flux delete hr -n <NAMESPACE> <DB_RELEASE>`
3. Scale down the application using this database to zero replicas
4. Reconcile Flux: `flux reconcile ks flux-system --with-source`
5. Scale up the application using this database back to desired replicas count
6. You may need to restart the database pod and the application again (this is usually the case of Linkace)

When started for the first time, a secret is created with database user passwords. You need to remove that secret after restoring database data. Then delete


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

### Pod not starting because Jiva volume is already mounted at more than one place

This is rather brutal solution, but it works. I will improve it if I find a better way.

1. Get node name where Jiva volume is mounted: `kubectl get jivavolume -n storage -o 'jsonpath={.metadata.labels.nodeID}' <PVC_NAME>`
2. Get node IP: `kubectl get node -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}' <NODE_NAME>`
3. Restart node: `talosctl reboot -n <NODE_IP>`

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
- Get more information on helm release (start here when "install retries exhausted")
    ```bash
    kubectl describe helmrelease <RELEASE_NAME> -n <RELEASE_NAMESPACE>
    ```
- Restart when Flux gave up
    ```bash
    flux resume hr <RELEASE_NAME> -n <RELEASE_NAMESPACE>
    ```

### Get CPU temperature in Proxmox for Asus PN50

Look at k10temp-pci-00c3 in the output of `sensors` command.
