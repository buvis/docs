## Preparation

Clone [https://github.com/buvis/clusters/](https://github.com/buvis/clusters/) repository to your workstation. Please note that modifications will be necessary to make it work for you.

### Tools

1. Install the following tools on your workstation:
   - [pre-commit](https://pre-commit.com/#installation)
   - [direnv](https://direnv.net/docs/installation.html)
   - [gnupg and sops](https://fluxcd.io/docs/guides/mozilla-sops)
   - [talosctl](https://github.com/siderolabs/talos/releases)
   - [jq](https://stedolan.github.io/jq/download)
   - [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
   - [krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install)
   - [minio kubectl plugin](https://github.com/minio/operator/tree/master/kubectl-minio)
   - [helm](https://helm.sh/docs/intro/install)
2. Install scripts requirements: `pip install -r requirements.txt` in clusters repository root directory

### Services

Create accounts:

- [Slack](https://slack.com/get-started#/createnew) to get notifications from Flux

### Gitops

1. [Add renovate to Github](https://github.com/marketplace/renovate)
2. Export `GITHUB_TOKEN` environment variable into `.envrc` files with [GitHub personal access token](https://github.com/settings/tokens) generated specifically for Flux
3. Export `SLACK_WEBHOOK_URL` environment variable into `.envrc` files, get incoming webhook address `<SLACK_WEBHOOK_URL>` from [Slack](https://api.slack.com/apps)
4. Enable [SOPS](https://github.com/mozilla/sops) for Flux

   1. _(do only once in a lifetime)_ Generate GPG key with no password protection. You can't protect the key with password, because Flux has no way of entering it when decrypting the secrets.
   2. Get fingerprint of the key `<SOPS_KEY_FINGERPRINT>`

      ```bash
      gpg --list-secret-keys
      ```

   3. Export `SOPS_KEY_FINGERPRINT` environment variable into `.envrc` files with the value from previous step

### Network

1. SSH to network's router
2. Copy cluster's `infrastructure/router/etc/bgpd.conf` to network's router's `/etc` to configure bgpd to peer with the cluster
3. Enable bgpd on network's router: `rcctl enable bgpd`
4. Assign IP addresses to nodes and VMs in `/etc/dhcpd.conf`, push router's IP as DNS to them

## Home cluster

This cluster is based on Virtual Machines provided by Proxmox.

### Install Proxmox

1. Download [Proxmox installation iso](https://www.proxmox.com/en/downloads/category/iso-images-pve)
2. [Burn it to USB stick](https://pve.proxmox.com/wiki/Prepare_Installation_Media). Note: in macOS, use 1M instead of 1m as block size
3. Boot Proxmox machine from the USB stick
4. Unauthorized change message will display, confirm it
5. Set the correct date and time in BIOS
6. Disable onboard wifi and bluetooth
7. Check that disks are recognized
8. Boot - Secure Boot = Disabled
9. Exit, save, reboot
10. Install Proxmox following the installation wizard (use router's IP as DNS server)
11. Enter root's password to `PM_PASS` environment variable in `.envrc`
12. After completing the installation, SSH to Proxmox server
13. Use community repo: `sed -i '1i deb http://download.proxmox.com/debian bullseye pve-no-subscription\n' /etc/apt/sources.list`
14. Disable enterprise repo: `sed -i 's/deb https:\/\/enterprise.proxmox.com\/debian\/pve bullseye pve-enterprise/# deb https:\/\/enterprise.proxmox.com\/debian\/pve bullseye pve-enterprise/g' /etc/apt/sources.list.d/pve-enterprise.list`
15. Update the system: `apt update && apt full-upgrade`
16. Install temperature sensors reading tools: `apt install xsensors` (then use `sensors` to read temperature measurements)
17. Reboot: `reboot now`
18. Remove subscription notice:

    1. Go to UI site source: `cd /usr/share/javascript/proxmox-widget-toolkit/`
    2. Backup the file you'll modify: `cp proxmoxlib.js proxmoxlib.js.bak`
    3. Edit `proxmoxlib.js`: `vi proxmoxlib.js`

    - Find

    ```
    Ext.Msg.show({
      title: gettext('No valid subscription'),
    ```

    - Replace with

    ```
    void({
      title: gettext('No valid subscription'),
    ```

    4. Restart Proxmox UI: `systemctl restart pveproxy.service`
    5. Clear browser cache and reconnect UI

19. Create storage for Persistent Volumes:
    1. Double check device name: `lsblk`
    2. Remove previous partitions (assuming device is `/dev/sda`): `fdisk /dev/sda`, `g`,`<ENTER>`, `w`, `<ENTER>`
    3. Connect to Proxmox management UI at `https://<server_ip>:8006`
    4. Create LVM Volume Group: `<NODENAME> - Disks - LVM`, `Create: Volume Group`, `Name: <NODENAME>-tank` on entire `/dev/sda`

### Get Talos schematic ID

Currently, the Talos schematic ID of images used in home cluster is `decca0d019b92170b9c7101da90f1ec0de7e9841b3d126ac4111743778d8eb1a`. This corresponds the following customization:

```
customization:
    extraKernelArgs:
        - amd_pstate=active
    systemExtensions:
        officialExtensions:
            - siderolabs/amd-ucode
            - siderolabs/amdgpu
            - siderolabs/iscsi-tools
            - siderolabs/qemu-guest-agent
            - siderolabs/util-linux-tools
```

If different customization is needed, you can find the schematic ID through [Talos Image Factory](https://factory.talos.dev). Then you need to update it in `.envrc` and `infrastructure/talos/patch-all.yaml`.

### Bootstrap

Run `buvisctl bootstrap` in `cluster-home` directory.

## Office cluster

This cluster is based on Raspberry Pi 4 machines.

### Flash SD cards

Flash Talos to SD cards by following [Talos installation guide](https://www.talos.dev/v1.2/talos-guides/install/single-board-computers/rpi_4/).

### Bootstrap the cluster

Run `make install`
