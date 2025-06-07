## Backup

1. Run backup job manually for every PVC: `buvisctl backup -n <NAMESPACE> <PVC>`
2. Perform application specific backup for the applications considered critical
   - home-assistant
   - linkace

## Destroy

Run `buvisctl destroy` in cluster's directory.

## Disable monitoring

First reconciliation by Flux will fail for multiple reasons. Avoid this by changing some manifests temporarily:

TODO: CRDs should be installed first, however I need to find out how to keep them updated

1. Disable ServiceMonitor for cert-manager: set `.spec.values.prometheus.servicemonitor.enabled=false` in `operations/kube-tools/cert-manager/helmrelease.yaml`
2. Disable ServiceMonitor for kyverno: set `.spec.values.*.serviceMonitor.enabled=false` in `operations/kube-tools/kyverno/helmrelease.yaml`
3. Disable ServiceMonitor for ingress-nginx: set `.spec.values.controller.metrics.serviceMonitor.enabled=false` in `operations/kube-tools/ingress-nginx/helmrelease.yaml`

## Bootstrap

1. Set workstation's DNS to 1.1.1.1, because Blocky isn't running
2. Make sure that GitHub PAT (stored in GITHUB_TOKEN environment variable) is still valid, and update it eventually
3. Run `buvisctl bootstrap` in cluster's directory.
4. Fix all Flux reconciliation errors
5. Enable monitoring by reversing the changes from [Disable monitoring chapter](operations.md#disable-monitoring)

## Restore

Run `./operations/storage/kopia/scripts/restore-pvcs.sh` in cluster's directory.

### Authentik outpost

Even after restoring the PVC, the outpost will not start. You need to login to authentik admin panel and remove applications from the `proxy-outpost` outpost, then add them again.

### MariaDB

After restore, pods running MariaDB won't start and report that "Access denied for user 'root'@'localhost'" in the log. This is because credentials were generated when cluster bootstrapped.

1. Delete _mariadb_ Secret for this database
2. Delete MariaDB helm release: `flux delete hr -n <NAMESPACE> <DB_RELEASE>`
3. Scale down the application using this database to zero replicas
4. Reconcile Flux: `flux reconcile ks flux-system --with-source`
5. Scale up the application using this database back to desired replicas count
6. You may need to restart the database pod and the application again (this is usually the case of Linkace)

When started for the first time, a secret is created with database user passwords. You need to remove that secret after restoring database data. Then delete
