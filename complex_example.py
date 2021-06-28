import tkinter as tk
from tkinter import ttk
import tkinterDnD


root = tkinterDnD.Tk()

root.title("tkinterDnD example")

stringvar = tk.StringVar()
stringvar.set('Drop here or drag from here!')


def drop(event):
    stringvar.set(event.data)
    if "color" in event.type:
        label_1.config(bg=event.data)
    
    
def drag_command(event):
    return (tkinterDnD.LINK, tkinterDnD.TEXT, "Some nice dropped text.")


# Without DnD hook you need to register the widget for every purpose,
# and bind it to the function you want to call
label_1 = tk.Label(root, textvar=stringvar, relief="solid")
label_1.pack(fill="both", expand=True, padx=10, pady=10)
label_1.register_drop_target(tkinterDnD.FILE)
label_1.register_drag_source("*")
label_1.bind("<<Drop>>", drop)
label_1.bind("<<DragInitCmd>>", drag_command)


# With DnD hook you just pass the command to the needed argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
label_2 = ttk.Label(root, onfiledrop=drop, ondragstart=drag_command,
                    textvar=stringvar, padding=50, relief="solid")
label_2.pack(fill="both", expand=True, padx=10, pady=10)


root.mainloop()

