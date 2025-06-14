# KittyNaut

**KittyNaut** is a Nautilus (GNOME Files) extension that allows you to open the [Kitty terminal](https://sw.kovidgoyal.net/kitty/) in the current folder directly from the right-click context menu.

Supports both:

- Right-clicking on a directory
- Right-clicking on empty space in a folder view

You can configure whether Kitty opens a **new tab** in an existing window or **launches a new window**.

## ✨ Features

- 🐱 Launch [Kitty](https://sw.kovidgoyal.net/kitty/) terminal from Nautilus.
- 📁 Context menu for both folders and background area.
- 🔀 Supports opening in a new **tab** (if Kitty is already running) or new **window**.
- ⚙️ Automatic installation script with support for most major Linux distributions.

## 🛠️ Installation

```bash
wget -qO- https://raw.githubusercontent.com/xinguohe/KittyNaut/refs/heads/main/install.sh | bash
```

## 🧪 Usage (Enable Kitty Remote Control)

To support opening new tabs in the same Kitty window, you must enable remote control in your Kitty configuration.

Edit your `~/.config/kitty/kitty.conf` and add the following:

```conf
allow_remote_control yes
listen_on unix:/tmp/kitty
```

Then restart Kitty to apply changes.

## 🔍 Configuration

Edit the `open_in_kitty.py` file and set:

```python
USE_TAB = True  # Set to False to always open a new Kitty window
```

## 📦 Uninstallation

```bash
rm ~/.local/share/nautilus-python/extensions/open_in_kitty.py
nautilus -q
```
