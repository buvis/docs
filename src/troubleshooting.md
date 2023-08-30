## Pod not starting because Jiva volume is already mounted at more than one place

This is rather brutal solution, but it works. I will improve it if I find a better way.

1. Get `<NODE_IP>` of node running JivaVolume for PVC: `get-pvc-node` and then enter PVC name
2. Reboot the node: `talosctl reboot -n <NODE_IP>`

## Flux can't reconcile a helmrelease

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

## Get CPU temperature in Proxmox for Asus PN50

Look at k10temp-pci-00c3 in the output of `sensors` command.
