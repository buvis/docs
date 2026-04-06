# High Availability

If you have two Proxmox hosts only, then it is better to have a single control plane node. It means that cluster can't operate when the machine with control plane node reboots, however this will happen anyway:

- two control plane nodes, each on separate Proxmox host => cluster not available when rebooting any Proxmox host
- three control plane nodes, host A has two, host B has one => cluster not available when rebooting host A

I was thinking about adding one Raspberry to act as third control plane node. It would work, but I don't like it, because:

- SD card will fail due to etcd writes (it was happening quite often when I had a cluster of Raspberries only)
- cluster bootstrap procedure would require flashing Talos to Raspberry manually

*Conclusion:* I need at least three Proxmox hosts for Kubernetes control plane high availability

References:
- [Why should a kubernetes control plane be three nodes | Sidero Labs](https://www.siderolabs.com/blog/why-should-a-kubernetes-control-plane-be-three-nodes/)
- [Virtual (shared) IP | Sidero Labs](https://www.talos.dev/v1.2/talos-guides/network/vip/)
