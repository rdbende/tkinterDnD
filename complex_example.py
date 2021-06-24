import tkinter as tk
import tkinterDnD


root = tkinterDnD.Tk()
root.title("tkinterDnD example")
root.geometry("300x300")

stringvar = tk.StringVar()
stringvar.set('Drop Here...')


def drop(event):
    stringvar.set(event.data)
    drop_label.config(bg="#ccc")

def drop_enter(event):
    drop_label.config(bg="#777")

def drop_leave(event):
    drop_label.config(bg="#ccc")
    
def drag_command(event):
    return (tkinterDnD.COPY, tkinterDnD.TEXT, "A nice little dragged text")


drop_label = tk.Label(root, textvar=stringvar, bg="#ccc", relief="solid")
drop_label.pack(fill="both", expand=True, padx=10, pady=10)
drop_label.register_drop_target(tkinterDnD.FILE)

drop_label.bind('<<DropEnter>>', drop_enter)
drop_label.bind('<<DropLeave>>', drop_leave)
drop_label.bind('<<Drop>>', drop)

drag_label = tk.Label(root, text="Drag from here!", bg="#ccc", relief="solid")
drag_label.pack(fill="both", expand=True, padx=10, pady=10)
drag_label.register_drag_source(tkinterDnD.TEXT)

drag_label.bind('<<DragInitCmd>>', drag_command)


root.mainloop()
