This hosts security related applications.

## Authentik

### Secure an application

TODO: automate this through buvisctl by using [Authentik Terraform provider](https://registry.terraform.io/providers/goauthentik/authentik/latest)

Follow these steps for `<appname>` in `<namespace>` hosted at `<app_external_url>`

1. Go to [Authentik administration interface](https://auth.buvis.net)
2. Create new provider: `Applications - Providers - Create`
  - name: `<namespace>-<appname>`
  - authorization flow: `default-provider-authorization-implicit-consent`
  - type: `Forward auth (single application)`
  - external host: `<app_external_url>`
3. Create new user group: `Directory - Groups - Create`
  - name: `<namespace>-<appname>-users`
4. Add users to the group
  1. Click group name
  2. Go to `Users` tab
  3. Add existing user
  4. Click plus icon
  5. Select user(s)
  6. Click `Add` button
5. Create new application: `Applications - Applications - Create`
  - name: `<namespace>-<appname>`
  - provider: `<namespace>-<appname>`
6. Bind the user group to the application
  1. Click application name
  2. Go to `Policy / Group / User Bindings`
  3. Click `Bind existing policy`
  4. Select `Group` tab
  5. Select `<namespace>-<appname>-users` group
  6. Click `Create`
7. Create new outpost
  - name: `<namespace>-<appname>`
  - applications: `<namespace>-<appname>`
  - configuration: change `kubernetes_ingress_class_name` to `nginx`
9. Annotate the ingress of the application by `authentik.home.arpa/enabled: "true"`. Kyverno will add the annotations enabling the authentication flow for the application.
10. Test authorized and unauthorized access to the application

### Automate basic authentication

If an application uses basic authentication, then it is possible to let Authentik do it on your behalf. The benefit is that you login once into the cluster and then you can use all the applications without entering passwords.

1. Add credentials to applications user group: `Directory - Groups - <namespace>-<appname>`
2. Click `Edit` button
3. Add attributes:
```
<appname>_username: <username_for_basic_auth_in_application>
<appname>_password: <password_for_basic_auth_in_application>
```
4. Map group attributes to Basic authentication fields: `Applications - Providers - <namespace>-<appname>`
5. Click `Edit` button
6. Unpack `Authentication settings`
7. Check `Send HTTP-Basic Authentication` checkbox
8. HTTP-Basic Username Key: `<appname>_username`
8. HTTP-Basic Password Key: `<appname>_password`

### Upgrade database

When upgrading authnetik, it may fail to start and report "FATAL:  database files are incompatible with server" error message. You need to migrate the database to higher version.

1. Downgrade authentik to previous version in its helmrelease
2. Delete `authentik-postgresql` StatefulSet
3. Force flux reconciliation: `flux reconcile ks flux-system --with-source`
4. Restart authentik release: `flux suspend hr -n security authentik && flux resume hr -n security authentik`
5. Stop authentik: `kubectl scale deploy --replicas 0 -n security authentik-server && kubectl scale deploy --replicas 0 -n security authentik-worker`
6. Dump the database: `kubectl exec -it authentik-postgresql-0 -n security -- env PGPASSWORD="<postgresql-postgres-password from authentik-postgresl secret>" /opt/bitnami/postgresql/bin/pg_dump -U postgres authentik > authentik-db-dumpfile`
7. Upgrade postgres: add this to authentik's `helmrelease.yaml`
```
postgresql:
  diagnosticMode:
    enabled: true
  image:
    tag: <NEWEST_TAG_FROM_HELM_CHART>
```
8. Force flux reconciliation: `flux reconcile ks flux-system --with-source`
9. Stop authentik: `kubectl scale deploy --replicas 0 -n security authentik-server && kubectl scale deploy --replicas 0 -n security authentik-worker`
10. Get a shell in authentik's postgres database pod: `kubectl exec -it authentik-postgresql-0 -n security -- bash`
11. Remove the old data: `cd /bitnami/postgresql/ && mv data data-11`
12. Restart authentik's postgres database by removing `diagnosticMode` from authentik's `helmrelease.yaml`
13. Force flux reconciliation: `flux reconcile ks flux-system --with-source`
14. Stop authentik: `kubectl scale deploy --replicas 0 -n security authentik-server && kubectl scale deploy --replicas 0 -n security authentik-worker`
15. Import the database: `kubectl exec -it authentik-postgresql-0 -n security -- env PGPASSWORD="<postgresql-postgres-password from authentik-postgresl secret>" psql -U postgres authentik < authentik-db-dumpfile`
16. Force flux reconciliation: `flux reconcile ks flux-system --with-source`
17. Restart authentik release: `flux suspend hr -n security authentik && flux resume hr -n security authentik`
18. Check that authentik works fine with the upgraded database
19. Remove `authentik-db-dumpfile`
20. Get a shell in authentik's postgres database pod: `kubectl exec -it authentik-postgresql-0 -n security -- bash`
21. Remove the old data: `cd /bitnami/postgresql/ && rm -rf data-11`
22. Remove `postgresql.image` from authentik's `helmrelease.yaml` and upgrade to latest helm chart version

### Set postgres user password

1. Shell to authentik-postgresql-0 pod: `kubectl exec -it authentik-postgresql-0 -n security -- bash`
2. Allow passwordless connection:
```bash
cat > /opt/bitnami/postgresql/conf/pg_hba.conf << EOF
host     all             all             0.0.0.0/0               trust
host     all             all             ::/0                    trust
local    all             all                                     trust
host     all             all        127.0.0.1/32                 trust
host     all             all        ::1/128                      trust
EOF
```
3. Reload postgresql config: `pg_ctl reload -D /bitnami/postgresql/data/`
4. Connect to dabase: `psql -U postgres`
5. Change password: `ALTER USER postgres WITH PASSWORD '<postgresql-postgres-password from authentik-postgresl secret>';`
6. `exit`
7. Restore permissions:
```bash
cat > /opt/bitnami/postgresql/conf/pg_hba.conf << EOF
host     all             all             0.0.0.0/0               md5
host     all             all             ::/0                    md5
local    all             all                                     md5
host     all             all        127.0.0.1/32                 md5
host     all             all        ::1/128                      md5
EOF
```
8. Reload postgresql config: `pg_ctl reload -D /bitnami/postgresql/data/`
