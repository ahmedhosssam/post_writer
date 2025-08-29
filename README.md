# Post Writer

## Requirements

Currently it only works on Linux with x11.

**System Requirements**:
- `gedit` - A Gnome Text Editor
- `xdotool`  - X11 automation tool
- `xorg`  - Linux display server
- `conda`  - Package manager system

**Python Dependencies**:
- `pyautogui` GUI automation library
- `pyinstaller` Bundles Python applications into a single executable.

## Installation

You can simply install it with:
**Note** You need to activate a Python environment first.
```bash
chmod +x setup.sh
./setup.sh
```
That will install `post_writer` in `/usr/bin/post_writer`.

## X11 Configuration for WSL

If you are running on WSL you need to do the following configurations:

```bash
touch ~/.Xauthority
chmod 600 ~/.Xauthority
export XAUTHORITY="$HOME/.Xauthority"
echo 'export DISPLAY=$(grep -m1 nameserver /etc/resolv.conf | awk '{print $2}'):0' >> ~/.bashrc
source ~/.bashrc
xhost +
```
This let the application know that the X server is running and they should use display `:0`.
