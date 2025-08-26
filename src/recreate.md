## Backup

1. Run `./operations/storage/kopia/scripts/backup-pvcs.sh` in cluster's directory.
2. Perform application specific backup for the applications considered critical
   - baikal
   - home-assistant
   - linkace

## Destroy

Run `buvisctl destroy` in cluster's directory. It may fail if providers versions were updated. In that case, run `terraform init -upgrade` in `infrastructure/terraform` directory and try again.

## Bootstrap

1. Set workstation's DNS to 1.1.1.1, because Blocky isn't running
2. Make sure that GitHub PAT (stored in GITHUB_TOKEN environment variable) is still valid, and update it eventually
3. Run `buvisctl bootstrap` in cluster's directory.
4. Wait for the bootstrap to finish. It may take a while, because it will download all images and install all applications.
5. Really, be patient, wait for no new workloads being created.
6. Check status of kustomizations with `flux get ks -A`. If there are any errors, fix them.
7. Check status of helmreleases with `flux get hr -A`. If there are any errors, fix them.
   - if helmrelease's resources started after it reached timeout, you can run `flux reconcile hr -n <NAMESPACE> <RELEASE>` to retry
   - if the helmrelease is still not ready, restart: `flux suspend hr -n <NAMESPACE> <RELEASE>` and then `flux resume hr -n <NAMESPACE> <RELEASE>`
   - as the last resort, you can delete the helmrelease and let Flux recreate it: `flux delete hr -n <NAMESPACE> <RELEASE>`

## Restore storage

1. Run `./operations/storage/kopia/scripts/restore-pvcs.sh` in cluster's directory.
1. Run `./operations/storage/kopia/scripts/recreate-backup-jobs.sh` in cluster's directory.

## Recreate Authentik outpost

Run `./operations/security/authentik/scripts/restore-pvcs.sh` in cluster's directory.
