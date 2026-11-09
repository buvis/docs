# Post-install

Most setup is handled by the install script. The steps below are optional or require manual action.

## Clone tracked repositories

The install script does not clone repositories automatically. This keeps dev container installs lightweight. To clone all tracked repositories from gita config:

```sh
GITA_CSV="$HOME/.config/gita/repos.csv"
while IFS=',' read -r repo_path repo_name _ _; do
  [ -d "$repo_path" ] && continue
  url_part=$(echo "$repo_path" | sed 's|.*/git/src/||')
  host=$(echo "$url_part" | cut -d/ -f1)
  remainder=$(echo "$url_part" | cut -d/ -f2-)
  git clone "git@${host}:${remainder}.git" "$repo_path"
done < "$GITA_CSV"
```

On WSL, use `$HOME/.config/wsl/gita/repos.csv` instead if it exists.

## Reveal secrets

On machines with your GPG key, decrypt git-secret managed files:

```sh
cfg secret reveal -f
```

## Herdr pager (phone notifications)

Herdr's `pager` mod reads its ntfy settings from `~/.local/.config/herdr-app/pager.local.json`. It is not in dotfiles. `~/.local` is the only thing you move to a new machine, so restoring `~/.local` is enough. On a machine without it, create the file (mode `0600`):

```json
{"url": "https://<ntfy-host>", "topic": "<topic>", "credentials": "<user>:<password>"}
```

`credentials` may be `""` if the server allows anonymous publishing. `NTFY_URL` and `NTFY_TOPIC` environment variables override `url` and `topic`. Without the file, phone delivery fails; desktop notifications still work.

## WSL only

1. Restart WSL after first install (`wsl --terminate Ubuntu` in cmd) to apply wsl.conf changes, then run `chmod -R a-x+X,u-x+rwX,go-wx+rX *` in affected directories to fix file coloring in vifm.

2. Let VS Code from Windows host use WSL:
    1. Install [WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
    2. Add VS Code to WSL's path: `echo 'export PATH=$PATH:/mnt/c/Users/<USERNAME>/.local/bin/vscode/bin' >> ~/.bashrc-wsl`
