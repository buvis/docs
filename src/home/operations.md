# Operations

All dotfile operations use the `dot` CLI provided by [buvis-gems](https://pypi.org/project/buvis-gems/). For interactive use, `dot tui` launches a terminal UI for staging, committing, and managing dotfiles.

## Update

1. Pull updates: `dot pull`
2. Stage updates: `dot add`
3. Commit with a message: `dot commit "<MESSAGE>"`
4. Push: `dot push`

## Add encrypted file

1. Register file for encryption: `dot encrypt path/to/file`
2. Check status: `dot status`
3. Stage encrypted file: `dot add path/to/file.secret`
4. Commit: `dot commit "<MESSAGE>"`
5. Push: `dot push`

## Add default Python package

1. Add package name to `$HOME/.default-python-packages`
2. Install: `pip install -r $HOME/.default-python-packages`
