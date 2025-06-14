#!/bin/bash

set -e

echo "[INFO] Checking and installing nautilus-python dependency..."

install_package() {
  local pkg_name=$1

  echo "[INFO] Installing package: $pkg_name"

  if type sudo >/dev/null 2>&1; then
    sudo_cmd="sudo"
  else
    echo "[ERROR] 'sudo' not found. Please install $pkg_name manually."
    exit 1
  fi

  if type pacman >/dev/null 2>&1; then
    if ! pacman -Qi "$pkg_name" >/dev/null 2>&1; then
      $sudo_cmd pacman -S --noconfirm "$pkg_name"
    else
      echo "[INFO] $pkg_name is already installed (pacman)."
    fi

  elif type apt >/dev/null 2>&1; then
    if ! dpkg -s "$pkg_name" >/dev/null 2>&1; then
      $sudo_cmd apt update
      $sudo_cmd apt install -y "$pkg_name"
    else
      echo "[INFO] $pkg_name is already installed (apt)."
    fi

  elif type dnf >/dev/null 2>&1; then
    if ! rpm -q "$pkg_name" >/dev/null 2>&1; then
      $sudo_cmd dnf install -y "$pkg_name"
    else
      echo "[INFO] $pkg_name is already installed (dnf)."
    fi

  elif type zypper >/dev/null 2>&1; then
    if ! rpm -q "$pkg_name" >/dev/null 2>&1; then
      $sudo_cmd zypper install -y "$pkg_name"
    else
      echo "[INFO] $pkg_name is already installed (zypper)."
    fi

  else
    echo "[ERROR] Unsupported package manager. Please install '$pkg_name' manually."
    exit 1
  fi
}

# Debian/Ubuntu branch: Determine whether the package name is supported by apt
if type apt >/dev/null 2>&1; then
  if apt list python3-nautilus 2>/dev/null | grep -q "python3-nautilus"; then
    install_package python3-nautilus
  elif apt list python-nautilus 2>/dev/null | grep -q "python-nautilus"; then
    install_package python-nautilus
  else
    echo "[ERROR] Neither 'python3-nautilus' nor 'python-nautilus' found in apt repositories."
    exit 1
  fi
else
  # Other distributions use nautilus-python
  install_package nautilus-python
fi

echo "[INFO] Installing Kitty Nautilus extension..."

EXT_DIR="$HOME/.local/share/nautilus-python/extensions"
EXT_FILE="$EXT_DIR/open_in_kitty.py"
REPO_URL="https://raw.githubusercontent.com/xinguohe/KittyNaut/refs/heads/main/open_in_kitty.py"

mkdir -p "$EXT_DIR"
rm -f "$EXT_FILE"

wget --show-progress -q -O "$EXT_FILE" "$REPO_URL"

echo "[INFO] Reloading Nautilus..."
nautilus -q

echo "[✅] Installation complete! You can now right-click in Nautilus to use 'Open in Kitty'."
