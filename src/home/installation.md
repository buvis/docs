# Installation

## Prerequisites

Install the following before running the install script:

1. [NerdFonts for Powerline](https://github.com/romkatv/powerlevel10k-media) (MesloLGS NF):
    - [Regular](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf)
    - [Bold](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf)
    - [Italic](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf)
    - [Bold Italic](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf)
2. Python and pip
3. Node.js
4. lazygit:
    - macOS: `brew install jesseduffield/lazygit/lazygit`
    - Windows: `scoop bucket add extras; scoop install lazygit`
5. libffi-dev:
    - macOS: `brew install libffi`
    - Linux/WSL: `sudo apt install libffi-dev`

## OS-specific preparation

### macOS

1. Install all pending OS updates (About This Mac - Software Update)
2. Install Xcode command line tools: `xcode-select --install`
3. Verify curl is installed: `command -v curl`
4. Set the desired machine name following [this guide](https://apple.stackexchange.com/questions/287760/set-the-hostname-computer-name-for-macos) if booted for the first time
5. Restart

### Windows

1. Configure git to keep line endings as-is: `git config --global core.autocrlf false`
2. Create home environment variables:

    ```powershell
    [Environment]::SetEnvironmentVariable("HOME", "$env:USERPROFILE", [System.EnvironmentVariableTarget]::User)
    [Environment]::SetEnvironmentVariable("XDG_CONFIG_HOME", "$env:USERPROFILE\.config", [System.EnvironmentVariableTarget]::User)
    ```

3. Install useful tools: `scoop install ag fd fzf neovim ripgrep vifm wget wezterm`

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

1. Clones buvis/home as a bare repo to `~/.buvis`
2. Checks out files into `$HOME`, backing up any conflicts
3. Initializes git submodules
4. Runs `mise install` if mise is available
5. Installs Claude CLI
6. Sets up private configs from buvis/cellar if accessible
