"""
Author: rdbende
License: MIT license
Copyright: 2021 rdbende
"""

from ttkwidgets.hook import hook_ttk_widgets, is_hooked


HOOK_OPTIONS = {"ontextdrop": None, "onfiledrop": None, "oncolordrop": None, "ondrop": None,
                "ondragstart": None, "ondragend": None, "ondragenter": None,
                "ondragleave": None, "ondragmove": None}


def dnd_options_hook(self, option, value) -> None:
    if option in HOOK_OPTIONS:
        dnd_hook_bind(self, option, value)
    else:  # This isn't really necessary, but it's good to have
        raise RuntimeError(f"Invalid tkinterDnD hook option: '{option}'")


def dnd_hook_bind(self, option, value) -> None:
    if callable(value):
        if option == "ontextdrop":
            self.bind("<<Drop:Text>>", value)
            self.register_drop_target("DND_Text")
        elif option == "onfiledrop":
            self.bind("<<Drop:File>>", value)
            self.register_drop_target("DND_Files")
        elif option == "oncolordrop":
            self.bind("<<Drop:Color>>", value)
            self.register_drop_target("DND_Color")
        elif option == "ondrop":
            self.bind("<<Drop:Any>>", value)
            self.register_drop_target("*")
        elif option == "ondragstart":
            self.bind("<<DragStart>>", value)
            self.register_drag_source("*")
        elif option == "ondragend":
            self.bind("<<DragEnd>>", value)
            self.register_drag_source("*")
        elif option == "ondragenter":
            self.bind("<<DragEnter>>", value)
            self.register_drop_target("*")
        elif option == "ondragleave":
            self.bind("<<DragLeave>>", value)
            self.register_drop_target("*")
        elif option == "ondragmove":
            self.bind("<<DragMove>>", value)
            self.register_drop_target("*")
    elif value is not None and not callable(value):
        raise TypeError(f"Cant bind '{option}' to '{value}', '{value}' is not callable!")


if not is_hooked(HOOK_OPTIONS):
    hook_ttk_widgets(dnd_options_hook, HOOK_OPTIONS)
