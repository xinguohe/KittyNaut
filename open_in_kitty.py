# Code reference: https://gitlab.gnome.org/GNOME/nautilus-python/-/blob/master/examples/open-terminal.py

from subprocess import CalledProcessError, Popen, check_output
from typing import List, Optional
from urllib.parse import unquote

from gi.repository import GObject, Nautilus

# Configuration: If True, open Kitty tabs in an existing window; else, always start a new window.
USE_TAB = True


def get_kitty_pid() -> Optional[str]:
    """
    Get the PID of the first running Kitty terminal process.

    Returns:
        str or None: The PID string if found, else None.
    """
    try:
        output = check_output(["pgrep", "-f", "kitty"], encoding="utf-8").strip()
        pids = output.splitlines()
        return pids[0] if pids else None
    except CalledProcessError:
        print("Info: No 'kitty' process found with 'pgrep'.")
    except FileNotFoundError:
        print("Error: 'pgrep' command not found. Please install it.")
    except Exception as e:
        print(f"Unexpected error in get_kitty_pid: {e}")
    return None


def launch_kitty(file_path: str, as_tab: bool) -> None:
    """
    Launch Kitty terminal in the given directory.

    Args:
        file_path (str): Directory to launch terminal in.
        as_tab (bool): Whether to launch as tab if Kitty is running.
    """
    print(f"Launching Kitty in: {file_path}")

    if as_tab:
        kitty_pid = get_kitty_pid()
        if kitty_pid:
            socket_path = f"unix:/tmp/kitty-{kitty_pid}"
            print(f"Using socket path: {socket_path}")
            try:
                Popen(
                    [
                        "kitty",
                        "@",
                        "--to",
                        socket_path,
                        "launch",
                        "--type=tab",
                        "--cwd",
                        file_path,
                    ]
                )
                return
            except Exception as e:
                print(f"Failed to open new Kitty tab: {e}, falling back to new window.")

    # Fallback or default: open a new Kitty window
    try:
        Popen(["kitty"], cwd=file_path)
    except FileNotFoundError:
        print("Error: 'kitty' command not found. Please ensure it is installed.")
    except Exception as e:
        print(f"Unexpected error while launching Kitty: {e}")


class OpenTerminalExtension(GObject.GObject, Nautilus.MenuProvider):
    """
    Nautilus extension to open Kitty terminal in selected directory.
    """

    def __init__(self) -> None:
        pass

    def _open_kitty_terminal(self, file_path: str) -> None:
        launch_kitty(file_path, USE_TAB)

    def menu_activate_cb(
        self, menu: Nautilus.MenuItem, file: Nautilus.FileInfo
    ) -> None:
        """
        Handler for context menu activation on a selected item.
        """
        path = unquote(file.get_uri()[7:])  # Remove 'file://' prefix
        self._open_kitty_terminal(path)

    def menu_background_activate_cb(
        self, menu: Nautilus.MenuItem, file: Nautilus.FileInfo
    ) -> None:
        """
        Handler for context menu activation on folder background.
        """
        path = unquote(file.get_uri()[7:])
        self._open_kitty_terminal(path)

    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:
        """
        Provide context menu item when a directory is selected.
        """
        if len(files) != 1:
            return []

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != "file":
            return []

        item = Nautilus.MenuItem(
            name="NautilusPython::open_in_kitty_file",
            label="Open in Kitty",
            tip=f"Open Kitty terminal in {file.get_name()}",
        )
        item.connect("activate", self.menu_activate_cb, file)
        return [item]

    def get_background_items(
        self, current_folder: Nautilus.FileInfo
    ) -> List[Nautilus.MenuItem]:
        """
        Provide context menu item for folder background.
        """
        item = Nautilus.MenuItem(
            name="NautilusPython::open_in_kitty_background",
            label="Open in Kitty",
            tip=f"Open Kitty terminal in {current_folder.get_name()}",
        )
        item.connect("activate", self.menu_background_activate_cb, current_folder)
        return [item]
