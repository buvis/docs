## Flux

This is automated using [Github Action](https://github.com/buvis/clusters/blob/main/.github/workflows/update-flux-home.yaml). Sometimes the Flux components may fail to start due to outdated CRDs. In that case, make sure you are on the latest Flux CLI (`brew upgrade fluxcd/tap/flux`) and run `buvisctl update flux`.

## Cilium

When new release of Cilium is available, you can update it using their [upgrade guide](https://docs.cilium.io/en/stable/operations/upgrade/).

## Talos

When siderolabs release a [new Talos version](https://github.com/siderolabs/talos/releases/latest) (`<VERSION_TAG>`):

1. Check for new [issues](https://github.com/siderolabs/talos/issues) to see if the new version is safe to use
2. Update nodes: `buvisctl update talos`
3. Check nodes versions: `talosctl -n $NODE_IPS version | awk '/^[[:space:]]*Client:/{ctx="Client"} /^[[:space:]]*NODE:/{ctx=$2} /^[[:space:]]*Tag:/{printf "%s %s %s\n", (ctx=="client"?"0":"1"), ctx, $2}' | sort | awk 'BEGIN {printf "\n%-15s %-8s\n", "Node", "Version"; print "--------------- --------"} {printf "%-15s %-8s\n", $2, $3}'`
4. Push Talos version changes to the repository

## Proxmox

1. Connect to Proxmox node: `ssh <NODE_NAME>`
2. Update packages: `apt update && apt dist-upgrade && apt autoremove`
3. Reboot: `reboot`
