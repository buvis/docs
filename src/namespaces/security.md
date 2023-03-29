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
