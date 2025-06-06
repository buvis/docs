## Flux

This is automated using [Github Action](https://github.com/buvis/clusters/blob/main/.github/workflows/update-flux-home.yaml). Sometimes the Flux components may fail to start due to outdated CRDs. In that case, make sure you are on the latest Flux CLI (`brew upgrade fluxcd/tap/flux`) and run `buvisctl update flux`.

## Calico

When Calico releases a new version of `tigera-operator`:

1. Determine latest version `<VERSION_TAG>`: [Calico Releases | GitHub](https://github.com/projectcalico/calico/releases)
2. Set temporary variable to use in following commands: `CALICO_VERSION=<VERSION_TAG>`
3. Get the updated manifest: `curl https://raw.githubusercontent.com/projectcalico/calico/$CALICO_VERSION/manifests/tigera-operator.yaml -O`
4. Initiate the upgrade: `kubectl apply -f tigera-operator.yaml`
5. Remove the manifest: `rm tigera-operator.yaml`

## Talos

TODO: Automate step 2

When siderolabs release a [new Talos version](https://github.com/siderolabs/talos/releases/latest) (`<VERSION_TAG>`):

1. Check for new [issues](https://github.com/siderolabs/talos/issues) to see if the new version is safe to use
2. Get installer image schematics ID from [Talos Linux Image Factory](https://factory.talos.dev)
   1. Choose latest Talos version
   2. Select `siderolabs/iscsi-tools` extension
   3. Submit
   4. Get Image schematic ID at `Your image schematic ID is:`
   5. Confirm it is the same as `echo $TALOS_SCHEMATIC_ID`
   6. If different, then update `.envrc`
3. Upgrade nodes: `upgrade-talos`
4. Check nodes version: `talosctl -n $NODE_IPS version | awk '/^[[:space:]]*Client:/{ctx="Client"} /^[[:space:]]*NODE:/{ctx=$2} /^[[:space:]]*Tag:/{printf "%s %s %s\n", (ctx=="client"?"0":"1"), ctx, $2}' | sort | awk 'BEGIN {printf "\n%-15s %-8s\n", "Node", "Version"; print "--------------- --------"} {printf "%-15s %-8s\n", $2, $3}'`

## Proxmox

1. Connect to Proxmox node: `ssh <NODE_NAME>`
2. Update packages: `apt update && apt dist-upgrade && apt autoremove`
3. Reboot: `reboot`
