# Post-install

Not all applications can be configured through dotfiles alone. The steps below require manual action after running the install script.

## Configure git

1. Navigate to dotfiles root: `cd $DOTFILES_ROOT`
2. Store credentials: `cfg config credential.helper store`
3. Honor global ignores: `git config --global core.excludesfile ~/.gitignore_global`

## Install dev tools

Run `mise install` while at `$HOME` to install all managed tool versions.

## Set up repository management

1. Create directory for git: `mkdir -p $HOME/git/src`
2. Clone the repositories you need
3. For each repository, register it with gita: `gita add .`

## Platform-specific steps

### macOS

- **ruff**: symlink `~/.config/ruff/pyproject.toml` to `~/Library/Application Support/ruff/pyproject.toml`
- **lazygit**: symlink `~/.config/lazygit/config.yml` to `~/Library/Application Support/lazygit/config.yml`

### Windows

- Add `~\scripts\bin` to PATH
- **PowerShell profile**: symlink `~/.config/powershell/Microsoft.PowerShell_profile.ps1` to the `PowerShell` folder in `shell:DocumentsLibrary`
- **lazygit**: symlink `~/.config/lazygit/config.yml` to `%LOCALAPPDATA%\lazygit\config.yml`

### WSL

1. Create symlinks in vifm (`yy` source, `al` in destination):
    - `windows-home` from `/mnt/c/Users/<WINDOWS_USERNAME>`
    - `Downloads` from `/mnt/c/Users/<WINDOWS_USERNAME>/Downloads`
    - `onedrive-company` from `/mnt/c/Users/<WINDOWS_USERNAME>/<OneDrive - company>`
    - `onedrive-private` from `/mnt/c/Users/<WINDOWS_USERNAME>/<OneDrive - private>`
    - `z` from `/mnt/c/Users/<WINDOWS_USERNAME>/<OneDrive - private>/z`

2. Fix file coloring in vifm by adding to `/etc/wsl.conf`:

    ```ini
    [automount]
    enabled = true
    options = "metadata,uid=1000,gid=1000,umask=0022,fmask=11,case=off"
    mountFsTab = false
    crossDistro = true

    [filesystem]
    umask = 0022
    ```

    Then restart WSL (`wsl --terminate Ubuntu` in cmd) and run `chmod -R a-x+X,u-x+rwX,go-wx+rX *` in affected directories.

3. Fix permissions for global npm packages: `npm config set prefix '~/.local/'`

4. Fix locale: `sudo tic -xe alacritty,alacritty-direct ~/.config/alacritty/alacritty.info`

5. Add WSL-specific overrides to `$HOME/.bashrc-wsl`:

    ```text
    export P_PROPERTIES_FILE="/home/bob/.pdata-wsl.properties"
    export GITA_PROJECT_HOME="/home/bob/.config/wsl/"
    ```

6. Let VS Code from Windows host use WSL:
    1. Install [WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
    2. Add VS Code to WSL's path: `echo 'export PATH=$PATH:/mnt/c/Users/tbouska/.local/bin/vscode/bin' >> ~/.bashrc-wsl`
