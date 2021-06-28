"""
Author: rdbende
License: MIT license
Copyright: 2017 Michael Lange, 2021 rdbende
"""

import tkinter as tk


class DnDEvent:
    """
    Container for the properties of a DnD event, similar to a normal tk.Event.
    A DnDEvent instance has the following attributes:

        action: string
        actions: tuple
        button: int
        code: string
        codes: tuple
        commonsourcetypes: tuple
        commontargettypes: tuple
        data: string
        name: string
        types: tuple
        modifiers: tuple
        supportedsourcetypes: tuple
        sourcetypes: tuple
        type: string
        supportedtargettypes: (tuple
        widget: widget
        x_root: int
        y_root: int
    """
    pass


class DnDWrapper:
    _subst_format_dnd = ("%A", "%a", "%b", "%C", "%c", "{%CST}", "{%CTT}", "%D",
        "%e", "{%L}", "{%m}", "{%ST}", "%T", "{%t}", "{%TT}", "%W", "%X", "%Y")
    _subst_format_str_dnd = " ".join(_subst_format_dnd)

    tk.BaseWidget._subst_format_dnd = _subst_format_dnd
    tk.BaseWidget._subst_format_str_dnd = _subst_format_str_dnd

    def _substitute_dnd(self, *args):
        if len(args) != len(self._subst_format_dnd):
            return args

        action, actions, button, code, codes, cm_src_types, cm_trgt_types, data, name, types, modifiers, sp_src_types, type, src_types, sp_trgt_types, widget, x, y = args

        def getint_event(arg):
            try:
                return int(arg)
            except ValueError:
                return arg

        def splitlist_event(arg):
            try:
                return self.tk.splitlist(arg)
            except ValueError:
                return arg

        def proc_data(arg):
            if "color" in type:
                return splitlist_color(arg)
            else:
                return arg

        def splitlist_color(arg):
            """If the drop type is color converts it to hex"""
            return ("#" + "".join(i[4:] for i in self.tk.splitlist(arg)))[:7]

        event = DnDEvent()

        event.action = action
        event.actions = splitlist_event(actions)
        event.button = getint_event(button)
        event.code = code
        event.codes = splitlist_event(codes)
        event.commonsourcetypes = splitlist_event(cm_src_types)
        event.commontargettypes = splitlist_event(cm_trgt_types)
        event.data = proc_data(data)
        event.name = name
        event.modifiers = splitlist_event(modifiers)
        event.sourcetypes = splitlist_event(src_types)
        event.supportedsourcetypes = splitlist_event(sp_src_types)
        event.supportedtargettypes = splitlist_event(sp_trgt_types)
        event.type = type
        event.types = splitlist_event(types)
        try:
            event.widget = self.nametowidget(widget)
        except KeyError:
            event.widget = widget
        event.x_root = getint_event(x)
        event.y_root = getint_event(y)

        return (event, )  # It must be an iterable

    tk.BaseWidget._substitute_dnd = _substitute_dnd

    def _dnd_bind(self, what, sequence, func, add, needcleanup=True):
        """The method, that does the actual binding"""
        if isinstance(func, str):
            self.tk.call(what + (sequence, func))
        elif func:
            funcid = self._register(func, self._substitute_dnd, needcleanup)
            cmd = f"{add and '+' or ''}{funcid} {self._subst_format_str_dnd}"
            self.tk.call(what + (sequence, cmd))

            return funcid
        elif sequence:
            return self.tk.call(what + (sequence, ))
        else:
            return self.tk.splitlist(self.tk.call(what))

    tk.BaseWidget._dnd_bind = _dnd_bind

    def dnd_bind(self, sequence=None, func=None, add=None):
        """
        Overwrites the tk.BaseWidget.bind method
        so we don't have to use a separate method for regular and
        dnd binding, simply checks which one to call,
        and if a dnd sequence is specified, and converts the simple
        and clear tkinterDnD events to tkdnd events

        Original tkdnd events:

        <<Drop>>
        <<Drop:*>>
        <<Drop:DND_Text>>
        <<Drop:DND_Files>>
        <<Drop:DND_Color>>
        <<DragInitCmd>>
        <<DragEndCmd>>
        <<DropEnter>>
        <<DropLeave>>
        <<DropPosition>>

        Simple and clear tkinterDnD events:
        
        <<Drop:Any>>
        <<Drop:Text>>
        <<Drop:File>>
        <<Drop:Color>>
        <<DragStart>>
        <<DragEnd>>
        <<DragEnter>>
        <<DragLeave>>
        <<DragMove>>
        """

        bind_func = self._bind
        if sequence in {"<<Drop>>", "<<Drop:*>>", "<<Drop:DND_Text>>",
                        "<<Drop:DND_Files>>", "<<Drop:DND_Color>>",
                        "<<DragInitCmd>>", "<<DragEndCmd>>", "<<DropEnter>>",
                        "<<DropLeave>>", "<<DropPosition>>", "<<Drop:Any>>",
                        "<<Drop:Text>>", "<<Drop:File>>", "<<Drop:Color>>",
                        "<<DragStart>>", "<<DragEnd>>", "<<DragEnter>>",
                        "<<DragLeave>>", "<<DragMove>>"}:
            
            if sequence == "<<Drop:Text>>":
                sequence = "<<Drop:DND_Text>>"
            elif sequence == "<<Drop:File>>":
                sequence = "<<Drop:DND_Files>>"
            elif sequence == "<<Drop:Color>>":
                sequence = "<<Drop:DND_Color>>"
            elif sequence == "<<Drop:Any>>":
                sequence = "<<Drop:*>>"
            elif sequence == "<<DragStart>>":
                sequence = "<<DragInitCmd>>"
            elif sequence == "<<DragEnd>>":
                sequence = "<<DragEndCmd>>"
            elif sequence == "<<DragEnter>>":
                sequence = "<<DragEnter>>"
            elif sequence == "<<DropLeave>>":
                sequence = "<<DropLeave>>"
            elif sequence == "<<DragMove>>":
                sequence = "<<DropPosition>>"

            bind_func = self._dnd_bind

        return bind_func(("bind", self._w), sequence, func, add)

    tk.BaseWidget.bind = dnd_bind

    def register_drag_source(self, dndtypes="*", button=1):
        """Registers the widget as drag source"""
        if type(button) != int:
            raise TypeError("Mouse button number must be an integer between 1 and 3")
            
        if button > 3:
            raise ValueError(f"Invalid mouse button number: '{button}'")
        
        self.tk.call("tkdnd::drag_source", "register", self._w, dndtypes, button)

    tk.BaseWidget.register_drag_source = register_drag_source

    def unregister_drag_source(self):
        """Unregisters the widget from drag source"""
        self.tk.call("tkdnd::drag_source", "unregister", self._w)

    tk.BaseWidget.unregister_drag_source = unregister_drag_source

    def register_drop_target(self, dndtypes="*"):
        """Registers the widget as drop target"""        
        self.tk.call("tkdnd::drop_target", "register", self._w, dndtypes)

    tk.BaseWidget.register_drop_target = register_drop_target

    def unregister_drop_target(self):
        """Unregisters the widget from drop target"""
        self.tk.call("tkdnd::drop_target", "unregister", self._w)

    tk.BaseWidget.unregister_drop_target = unregister_drop_target

    def platform_independent_types(self, *dndtypes):
        return self.tk.split(self.tk.call("tkdnd::platform_independent_types", dndtypes))

    tk.BaseWidget.platform_independent_types = platform_independent_types

    def platform_specific_types(self, *dndtypes):
        return self.tk.split(self.tk.call("tkdnd::platform_specific_types", dndtypes))

    tk.BaseWidget.platform_specific_types = platform_specific_types

    def get_dropfile_tempdir(self):
        return self.tk.call("tkdnd::GetDropFileTempDirectory")

    tk.BaseWidget.get_dropfile_tempdir = get_dropfile_tempdir

    def set_dropfile_tempdir(self, tempdir):
        self.tk.call("tkdnd::SetDropFileTempDirectory", tempdir)

    tk.BaseWidget.set_dropfile_tempdir = set_dropfile_tempdir

