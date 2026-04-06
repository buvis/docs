# Installation

## Prerequisites

### macOS

1. Install all pending OS updates (About This Mac - Software Update)
2. Set the desired machine name following [this guide](https://apple.stackexchange.com/questions/287760/set-the-hostname-computer-name-for-macos) if booted for the first time
3. Restart

The install script handles Xcode CLI tools, Homebrew, and all packages automatically.

### Windows

No manual prerequisites. The install script handles Scoop, packages, fonts, and environment variables.

### Linux

The install script bootstraps git and curl if missing, then handles mise, libffi, and fonts automatically. Supports apt, dnf, pacman, zypper, and apk. The only assumption is that `curl` is available to fetch the script and `sudo` is available for system packages.

### WSL

Currently not in active use. No specific instructions available.

## Install

### macOS, WSL, and Linux

```sh
curl -fsSL https://tinyurl.com/install-buvis | sh
```

### Windows

```powershell
irm https://tinyurl.com/install-ps-buvis | iex
```

The install script:

1. Bootstraps system package manager (Homebrew on macOS, Scoop on Windows)
2. Clones buvis/home as a bare repo to `~/.buvis`
3. Checks out files into `$HOME`, backing up any conflicts
4. Initializes git submodules
5. Installs all packages (Brewfile on macOS, Scoop on Windows, mise/libffi/fonts on Linux)
6. Runs `mise install` for dev tool versions
7. Configures git (credential helper, global excludesfile)
8. Creates `~/git/src` and clones tracked repositories from gita config
9. Sets up app config symlinks (macOS Application Support, Windows lazygit/PowerShell profile)
10. Configures WSL environment (wsl.conf, npm prefix, locale, .bashrc-wsl, Windows home symlinks)
11. Installs Claude CLI
12. Sets up private configs from buvis/cellar if accessible
