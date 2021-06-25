"""
Author: rdbende
License: MIT license
Copyright: 2017 Michael Lange, 2021 rdbende
"""

import tkinter as tk


class DnDEvent:
    """
    Container for the properties of a drag-and-drop event, similar to a normal tk.Event.
    An instance of the DnDEvent class has the following attributes:

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

        def getint_event(arg):
            try:
                return int(arg)
            except ValueError:
                return arg

        def splitlist_event(arg):
            if "color" in args[12]: # Slice 12 is event.type
                return splitlist_color(arg)
            else:
                try:
                    return self.tk.splitlist(arg)
                except ValueError:
                    return arg
            
        def splitlist_color(arg):
            """If the drop type is color converts it to hex"""
            return ("#" + "".join(i[4:] for i in self.tk.splitlist(arg)))[:7]

        A, a, b, C, c, CST, CTT, D, e, L, m, ST, T, t, TT, W, X, Y = args
        event = DnDEvent()

        event.action = A
        event.actions = splitlist_event(a)
        event.button = getint_event(b)
        event.code = C
        event.codes = splitlist_event(c)
        event.commonsourcetypes = splitlist_event(CST)
        event.commontargettypes = splitlist_event(CTT)
        event.data = splitlist_event(D)
        event.name = e
        event.types = splitlist_event(L)
        event.modifiers = splitlist_event(m)
        event.supportedsourcetypes = splitlist_event(ST)
        event.sourcetypes = splitlist_event(t)
        event.type = T
        event.supportedtargettypes = splitlist_event(TT)
        try:
            event.widget = self.nametowidget(W)
        except KeyError:
            event.widget = W
        event.x_root = getint_event(X)
        event.y_root = getint_event(Y)

        return (event, ) # It must be an iterable

    tk.BaseWidget._substitute_dnd = _substitute_dnd

    def _dnd_bind(self, what, sequence, func, add, needcleanup=True):
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
        <<Drop:DND_Files>>
        <<Drop:DND_Text>>
        <<Drop:DND_Color>>
        <<DragInitCmd>>
        <<DragEndCmd>>
        <<DropEnter>>
        <<DropLeave>>
        <<DropPosition>>
        
        Simple and clear tkinterDnD events:
        
        <<Drop:File>>
        <<Drop:Text>>
        <<Drop:Color>>
        <<Drop:Any>>
        <<DragStart>>
        <<DragEnd>>
        <<DragEnter>>
        <<DragLeave>>
        <<DragMove>>
        """
        
        bind_func = self._bind
        if sequence in {"<<DropEnter>>", "<<DropPosition>>",
                        "<<DropLeave>>", "<<Drop>>", "<<Drop:DND_Files>>",
                        "<<Drop:DND_Text>>", "<<Drop:DND_Color>>",
                        "<<DragInitCmd>>", "<<DragEndCmd>>", "<<Drop:File>>",
                        "<<Drop:Text>>", "<<Drop:Color>>", "<<Drop:Any>>",
                        "<<DragStart>>", "<<DragEnd>>", "<<DragEnter>>",
                        "<<DragLeave>>", "<<DragMove>>"}:
            
            if sequence == "<<Drop:File>>":
                sequence = "<<Drop:DND_Files>>"
            elif sequence == "<<Drop:Text>>":
                sequence = "<<Drop:DND_Text>>"
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
                sequence = "<<DropPosotion>>"
            
            bind_func = self._dnd_bind

        return bind_func(("bind", self._w), sequence, func, add)

    tk.BaseWidget.bind = dnd_bind

    def register_drag_source(self, button=None, *dndtypes):
        """Registers the widget as drag source"""
        if button is None:
            button = 1
        else:
            try:
                button = int(button)
            except ValueError:
                dndtypes = (button, ) + dndtypes
                button = 1

        self.tk.call("tkdnd::drag_source", "register", self._w, dndtypes, button)

    tk.BaseWidget.register_drag_source = register_drag_source

    def unregister_drag_source(self):
        """Unregisters the widget from drag source"""
        self.tk.call("tkdnd::drag_source", "unregister", self._w)

    tk.BaseWidget.unregister_drag_source = unregister_drag_source

    def register_drop_target(self, *dndtypes):
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
