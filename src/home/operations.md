# Operations

## Update

### macOS, WSL, and Linux

1. Open terminal
2. Go home: `cd $HOME`
3. Pull updates: `cfgl`
4. Stage updates: `cfgapa`
5. Commit with a message: `cfgm "<MESSAGE>"`
6. Push: `cfgp`

### Windows

1. Open cmd
2. Go home: `cd %userprofile%`
3. Pull updates: `cfgl.bat`
4. Stage updates: `cfgapa.bat`
5. Commit with a message: `cfgm.bat "<MESSAGE>"`
6. Push: `cfgp.bat`

## Add encrypted file

1. Register file for encryption: `cfg secret add path/to/file`
2. Encrypt and check status: `cfgs`
3. Stage encrypted file and metadata: `cfga path/to/file.secret .gitsecret`
4. Commit: `cfgm "<MESSAGE>"`
5. Push: `cfgp`

## Add default Python package

1. Add package name to `$HOME/.default-python-packages`
2. Install: `pip install -r $HOME/.default-python-packages`
