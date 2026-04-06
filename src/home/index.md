# Home

[buvis/home](https://github.com/buvis/home) manages dotfiles, tool configurations, shell setup, Ansible playbooks, and dev tool versions for BUVIS machines.

## How it works

The repository is a [bare git repo](https://www.atlassian.com/git/tutorials/dotfiles) overlaid directly on `$HOME`. Running the install script clones it to `~/.buvis` and checks out configuration files into their expected locations. Conflicting files are backed up automatically.

Tracked files include:

- Shell configuration (bash, nushell, starship)
- Editor setup (neovim)
- Terminal emulators (alacritty, wezterm)
- Git tooling (git, lazygit, gita, gh)
- Dev tool versions managed by [mise](https://mise.jdx.dev/)
- Ansible playbooks for infrastructure provisioning
- Private configurations via [buvis/cellar](https://github.com/buvis/cellar) (separate private repo)

Secrets are handled with [git-secret](https://git-secret.io/) - encrypted files are committed alongside the rest of the configuration.

## Dev containers

These dotfiles also get installed into development containers running on the [cluster](../cluster/index.md). This provides a consistent, familiar environment for both interactive and unattended development work.
