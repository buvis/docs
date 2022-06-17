## Preparation

### Tools

Install the following tools on your workstation:

- [pre-commit](https://pre-commit.com/#installation)
- [direnv](https://direnv.net/docs/installation.html)
- [gnupg and sops](https://fluxcd.io/docs/guides/mozilla-sops/)
- [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/)
- [minio kubectl plugin](https://github.com/minio/operator/tree/master/kubectl-minio)

### Services

Create accounts:

- [ZeroSSL](https://app.zerossl.com/signup) to get certificates for ingress
- [Slack](https://slack.com/get-started#/createnew) to get notifications from Flux

### Gitops

1. [Add renovate to Github](https://github.com/marketplace/renovate)
2. Make sure that postgres database `kubernetes` doesn't exist on datastore server
3. Update EAB Credentials for ZeroSSL ACME
    1. Generate new key-secret pair at [ZeroSSL | Developer](https://app.zerossl.com/developer)
    2. Update secrets for cert-manager (do this in all cluster directories):
        ```bash
        sops operations/kube-system/cert-manager/secrets.yaml
        ```
    3. Update keyID in `operations/kube-system/cert-manager/operators/zerossl.yaml` (do this in all cluster directories)
4. Export `GITHUB_TOKEN` environment variable into `.envrc` files with [GitHub personal access token](https://github.com/settings/tokens) generated specifically for Flux
5. Export `SLACK_WEBHOOK_URL` environment variable into `.envrc` files, get incoming webhook address `<SLACK_WEBHOOK_URL>` from [Slack](https://api.slack.com/apps)
6. Enable [SOPS](https://github.com/mozilla/sops) for Flux
    1. *(do only once in a lifetime)* Generate GPG key with no password protection. You can't protect the key with password, because Flux has no way of entering it when decrypting the secrets.
    2. Get fingerprint of the key `<SOPS_KEY_FINGERPRINT>`
        ```bash
        gpg --list-secret-keys
        ```
    3. Export `SOPS_KEY_FINGERPRINT` environment variable into `.envrc` files with the value from previous step

### Network

1. SSH to home router
2. Assign IP addresses to nodes and VMs in `/etc/dhcpd.conf`, push router's IP as DNS to them
3. Install bgpd on home router
4. Copy `network/router/etc/bgpd.conf` to home router's `/etc` to configure bgpd to peer with the cluster

## Production cluster

Anything that follows supposes you are working in [production directory](https://github.com/buvis/clusters/tree/main/production).
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
12. Check that you can connect to Proxmox management UI at `https://<server_ip>:8006`
13. Remove subscription notice
    1. SSH to proxmox server
    2. Go to UI site source: `cd /usr/share/javascript/proxmox-widget-toolkit/`
    3. Backup the file you'll modify: `cp proxmoxlib.js proxmoxlib.js.bak`
    4. Edit `proxmoxlib.js`: `vi proxmoxlib.js`
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
    5. Restart Proxmox UI: `systemctl restart pveproxy.service`
    6. Clear browser cache and reconnect UI
14. Use community repo
    1. Edit sources: `vi /etc/apt/sources.list`
    2. Add `deb http://download.proxmox.com/debian bullseye pve-no-subscription`
15. Disable enterprise repo
    1. Go to apt sources directory: `cd /etc/apt/sources.list.d`
    2. Backup enterprise list: `cp pve-enterprise.list pve-enterprise.list.bak`
    3. Edit enterprise list: `vi pve-enterprise.list`
    4. Comment out this line: `deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise`
16. Update the system: `apt update && apt dist-upgrade`
17. Create storage for Persistent Volumes: `<NODENAME> - Disks - ZFS`, create `<NODENAME>-tank` on entire /dev/sda
18. Install temperature sensors reading tools: `apt install xsensors` (then use `sensors` to  read temperature measurements)

### Fix Proxmox on Asus PN50

I faced the following issues in spring 2022 when installing Proxmox to Asus PN50. In May 2022, I installed Proxmox to Asus PN51 and there were no issues with that.

1. Network will be down on the first boot. Restart it: `systemctl restart networking`
2. Reboot gets stuck when exiting KVM. Upgrade to kernel 5.15: `apt install pve-kernel-5.15 pve-kernel-5.15.5-1-pve pve-headers-5.15 pve-headers-5.15.5-1-pve`

References:

- [Realtek 8125 issues | Proxmox forum](https://forum.proxmox.com/threads/another-realtek-8125-funny.102240/)
- [Shutdown hangs on kvm exiting | Proxmox forum](https://forum.proxmox.com/threads/shutdown-hangs-on-kvm-exiting-hardware-virtualization.101914/)

### Create VM template

1. SSH to proxmox machine
2. Get the image for VM: `wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img`.
    Note: I couldn't use the following images:
    - Arch Linux: it lacks overlay module, so k3s won't run
    - CentOS: all VMs are named localhost, so Kubernetes will add one node only
3. Create VM: `qm create 9000 --name "ubuntu-cloudimg" --memory 4096 --cpu cputype=host --cores 4 --serial0 socket --vga serial0 --net0 virtio,bridge=vmbr0,tag=20 --agent enabled=1,fstrim_cloned_disks=1`
4. Import the image to local storage: `qm importdisk 9000 focal-server-cloudimg-amd64.img local-lvm --format qcow2`
5. Attach the disk to VM: `qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0`
6. Add cloudinit CDROM drive: `qm set 9000 --ide2 local-lvm:cloudinit`
7. Set disk to boot: `qm set 9000 --boot c --bootdisk scsi0`
8. Convert VM to template: `qm template 9000`
9. Repeat steps 2-8 on every node in Proxmox cluster. ID 9000 must be incremented as this ID must be unique inside the cluster.

### Bootstrap

1. Set workstation's DNS to 1.1.1.1, because Blocky isn't running
2. Run `make install` in cluster's directory.

## Staging cluster

Anything that follows supposes you are working in [staging directory](https://github.com/buvis/clusters/tree/main/staging).

### Bootstrap the cluster

1. Flash the nodes: `ansible-playbook infrastructure/ansible/flash-node`
2. Get kube config: `ansible-playbook infrastructure/ansible/get-cluster-config`
3. Limit workloads scheduling to master nodes:
```bash
kubectl taint node <master> node-role.kubernetes.io/master:NoSchedule`
```

### CNI deployment

1. Install bgpd on home router
2. Copy `infrastructure/etc/bgpd.conf` to home router's `/etc` to configure bgpd to peer with the cluster
3. Install Calico operator (manifest from [Calico multi-node install](https://docs.projectcalico.org/getting-started/kubernetes/k3s/multi-node-install) modified to refer to arm64 images):
```bash
kubectl apply -f infrastructure/manifests/deploy-tigera-operator.yaml`
```
4. Install Calico (manifest modified to use BGP peering with home router):
```bash
kubectl apply -f infrastructure/manifests/install-calico.yaml`
```

### Workloads deployment

[Flux](https://github.com/fluxcd/flux2) watches my [clusters repository](https://github.com/buvis/clusters) and makes the changes to them based on the YAML manifests.

To install Flux, run `make flux`

## Persistent volumes migration

Longhorn connects to NAS backup directory and the backups aren't linked to the previous installation, so they can be used in the new cluster without any problems.

1. Connect to Longhorn frontend
2. Go to Backups
3. Restore all volumes from backup
4. The Longhorn volumes and PVs have a static name, so the workloads will pick the volumes restored from backup if you keep the name (check `Use Previous Name` checkbox in Restore Backup dialog)
