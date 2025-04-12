#!/bin/bash

echo "Installing PortViz..."

# Get absolute path to this folder
BASEDIR="$(cd "$(dirname "$0")" && pwd)"

# Make scripts executable
chmod +x "$BASEDIR/portviz.py"
chmod +x "$BASEDIR/launch.sh"

# Symlink the .desktop file to the applications folder
DESKTOP_SRC="$BASEDIR/portviz.desktop"
DESKTOP_DEST="$HOME/.local/share/applications/portviz.desktop"

echo "Linking launcher..."
mkdir -p "$HOME/.local/share/applications"
ln -sf "$DESKTOP_SRC" "$DESKTOP_DEST"

echo "PortViz installed!"
echo "You can now launch it from your app menu (search for 'PortViz')"
