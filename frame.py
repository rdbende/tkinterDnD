import tkinter as tk
from tkinter import ttk
import tkinterDnD

class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        onfiledrop = kwargs.pop("onfiledrop", None)
        ontextdrop = kwargs.pop("ontextdrop", None)
        ondrop = kwargs.pop("ondrop", None)
        ondragstart = kwargs.pop("ondragstart", None)
        ondragend = kwargs.pop("ondragend", None)
        ondragenter = kwargs.pop("onadragenter", None)
        ondragleave = kwargs.pop("ondragleave", None)
        ondragmove = kwargs.pop("ondragmove", None)
        
        tk.Frame.__init__(self, *args, **kwargs)
        
        if onfiledrop:
            self.bind("<<Drop:DND_Files>>", onfiledrop)
            self.register_drop_target("DND_Files")
        if ontextdrop:
            self.bind("<<Drop:DND_Text>>", ontextdrop)
            self.register_drop_target("DND_Text")
        if ondrop:
            self.bind("<<Drop>>", ondrop)
            self.register_drop_target("*")
        if ondragstart:
            self.bind("<<DragInitCmd>>", ondragstart)
            self.register_drag_source()
        if ondragend:
            self.bind("<<DragEndCmd>>", ondragend)
            self.register_drag_source()
        if ondragenter:
            self.bind("<<DropEnter>>", ondragenter)
            self.register_drop_target("*")
        if ondragleave:
            self.bind("<<DropLeave>>", ondragleave)
            self.register_drop_target("*")
        if ondragmove:
            self.bind("<<DropPosition>>", ondragmove)
            self.register_drop_target("*")
            
    def bind(self, sequence=None, func=None, add=None):
        """
        I want to handle simple events like <<Drop:File>> instead of
        <<Drop:DND_Files>>, but I can't do it with `event_add`,
        so I'm rewriting the bind
        """
        
        if sequence == "<<Drop:File>>":
            sequence = "<<Drop:DND_Files>>"
        elif sequence == "<<Drop:Text>>":
            sequence = "<<Drop:DND_Files>>"
        elif sequence == "<<Drop:Any>>":
            sequence = "<<Drop>>"
            
        return tk.Frame.bind(self, sequence, func, add)
        
if __name__ == "__main__":
    root = tkinterDnD.Tk()

    def drop(event):
        return ("copy", "DND_Text", "A nice little dragged text")
    
    drop_label = Frame(root, ondragstart=drop, bg="#ccc", relief="solid")
    drop_label.pack(fill="both", expand=True, padx=10, pady=10)
    
    
    root.mainloop()
