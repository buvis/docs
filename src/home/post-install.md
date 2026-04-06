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

## WSL only

1. Restart WSL after first install (`wsl --terminate Ubuntu` in cmd) to apply wsl.conf changes, then run `chmod -R a-x+X,u-x+rwX,go-wx+rX *` in affected directories to fix file coloring in vifm.

2. Let VS Code from Windows host use WSL:
    1. Install [WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
    2. Add VS Code to WSL's path: `echo 'export PATH=$PATH:/mnt/c/Users/<USERNAME>/.local/bin/vscode/bin' >> ~/.bashrc-wsl`
