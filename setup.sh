#!/bin/bash
set -e

if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    exit 1
fi

sudo apt-get install -y xdotool gedit python3-pip 
pip install pyautogui
pyinstaller --onefile --console --name post_writer main.py

sudo cp ./dist/post_writer /usr/bin/post_writer
