## Backup

1. Run backup job manually for every PVC: `buvisctl backup -n <NAMESPACE> <PVC>`
2. Perform application specific backup for the applications considered critical
   - baikal
   - home-assistant
   - linkace

## Destroy

Run `buvisctl destroy` in cluster's directory.

## Bootstrap

1. Set workstation's DNS to 1.1.1.1, because Blocky isn't running
2. Make sure that GitHub PAT (stored in GITHUB_TOKEN environment variable) is still valid, and update it eventually
3. Run `buvisctl bootstrap` in cluster's directory.
4. Wait for the bootstrap to finish. It may take a while, because it will download all images and install all applications.
5. Check status of kustomizations with `flux get ks -A`. If there are any errors, fix them.
6. Check status of helmreleases with `flux get hr -A`. If there are any errors, fix them.
   - if resources started after timeout, you can run `flux reconcile hr -n <NAMESPACE> <RELEASE>` to retry
   - if the helmrelease is still not ready, restart: `flux suspend hr -n <NAMESPACE> <RELEASE>` and then `flux resume hr -n <NAMESPACE> <RELEASE>`
   - as the last resort, you can delete the helmrelease and let Flux recreate it: `flux delete hr -n <NAMESPACE> <RELEASE>`

## Restore

Run `./operations/storage/kopia/scripts/restore-pvcs.sh` in cluster's directory.

## Create Authentik outpost

1. Login as `akadmin` to [Authentik](https://auth.buvis.net)
2. Go to `Admin Interface`
3. Select `Applications > Outposts` from the left menu
4. Edit `proxy-outpost` outpost
5. Remove all applications from the outpost
6. Add all applications back to the outpost
7. If you get HTTP 500 error, you may need to delete authentik pods
