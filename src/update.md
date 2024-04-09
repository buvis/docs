[##](##.md) Flux

This is automated using [Github Action](https://github.com/buvis/clusters/blob/main/.github/workflows/update-flux-home.yaml). Sometimes the Flux components may fail to start due to outdated CRDs. In that case, make sure you are on the latest Flux CLI (`brew upgrade flux`) and run `buvisctl update flux`.

## Calico

When Calico releases a new version of `tigera-operator`:

1. Determine `<VERSION_TAG>`: [Calico Releases | GitHub](https://github.com/projectcalico/calico/releases)
2. Set temporary variable to use in following commands: `CALICO_VERSION=<VERSION_TAG>`
3. Get the updated manifest: `curl https://raw.githubusercontent.com/projectcalico/calico/release-<VERSION_TAG_MAIN>/manifests/tigera-operator.yaml -O`
4. Initiate the upgrade: `kubectl apply -f tigera-operator.yaml`
5. Remove the manifest: `rm tigera-operator.yaml`
6. Update Talos installation patch: `vim infrastructure/talos/patch-all.yaml` and update `<VERSION_TAG>` in `/cluster/network/cni/custom/urls`
7. Update all machineconfigs: `talosctl -n $NODE_IPS edit machineconfig --mode=no-reboot` and update `<VERSION_TAG>` in `/cluster/network/cni/custom/urls`

## Talos

TODO: Automate step 4

When siderolabs release a [new Talos version](https://github.com/siderolabs/talos/releases/latest) (`<VERSION_TAG>`):

1. Check for new [issues](https://github.com/siderolabs/talos/issues) to see if the new version is safe to use
2. Set temporary variable to use in following commands: `export TALOS_VERSION=<VERSION_TAG>`
3. Update the client (`talosctl`)
  a. Download amd64 binary: `curl -Lo ~/.local/bin/talosctl https://github.com/siderolabs/talos/releases/download/$TALOS_VERSION/talosctl-$(uname -s | tr "[:upper:]" "[:lower:]")-amd64`
  b. Make it executable: `chmod +x ~/.local/bin/talosctl`
4. Get installer image schematics ID from [Talos Linux Image Factory](https://factory.talos.dev)
    a. Choose latest Talos version
    b. Select `siderolabs/iscsi-tools` extension
    c. Submit
    d. Get Image schematic ID at `Your image schematic ID is:`
    e. Confirm it is the same as `echo $TALOS_SCHEMATIC_ID`
    f. If different, then update `.envrc`
5. Upgrade nodes: `upgrade-talos`
6. Check nodes version: `talosctl -n $NODE_IPS version`

## Proxmox

1. Connect to Proxmox node: `ssh <NODE_NAME>`
2. Update packages: `apt update && apt dist-upgrade && apt autoremove`
3. Reboot: `reboot`
