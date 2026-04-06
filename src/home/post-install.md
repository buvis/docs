# Post-install

Most setup is handled by the install script. The steps below require manual action.

## WSL only

1. Restart WSL after first install (`wsl --terminate Ubuntu` in cmd) to apply wsl.conf changes, then run `chmod -R a-x+X,u-x+rwX,go-wx+rX *` in affected directories to fix file coloring in vifm.

2. Let VS Code from Windows host use WSL:
    1. Install [WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
    2. Add VS Code to WSL's path: `echo 'export PATH=$PATH:/mnt/c/Users/<USERNAME>/.local/bin/vscode/bin' >> ~/.bashrc-wsl`
