"""
Author: rdbende
License: MIT license
Copyright: 2017 Michael Lange, 2021 rdbende
"""

import tkinter as tk
from .dnd import DnDWrapper
import os.path


def _init_tkdnd(master: tk.Tk) -> None:
    """Add the tkdnd package to the auto_path, and import it"""

    platform = master.tk.call("tk", "windowingsystem")

    if platform == "win32":
        folder = "windows"
    elif platform == "x11":
        folder = "linux"
    elif platform == "aqua":
        folder = "mac"

    package_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder)

    master.tk.call('lappend', 'auto_path', package_dir)

    TkDnDVersion = master.tk.call('package', 'require', 'tkdnd')

    return TkDnDVersion


class Tk(tk.Tk, DnDWrapper):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.TkDnDVersion = _init_tkdnd(self)
