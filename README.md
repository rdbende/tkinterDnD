# tkinterDnD
A nice and easy-to-use wrapper around the tkdnd package. No tcl installation, no build is required, **just install and use it!**

## Install
The Pypi name is python-tkdnd, because tkinterDnD was already taken, but you can import the package as `tkinterDnD`

```
pip3 install python-tkdnd
```
or if you're using a distro like Windows 7, 10, or 11 replace `pip3` with `pip`


## Credits
```
Copyright (c) 2021 rdbende
Copyright (c) 2012-2020 Petasis - the tkdnd package
Copyright (c) 2020 Philippe Gagné - for Mac binaries
Copyright (c) 2017 Michael Lange - the TkinterDnD package
```

## Little example
```python
import tkinter as tk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module

# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()  
root.title("tkinterDnD example")

stringvar = tk.StringVar()
stringvar.set('Drop here or drag from here!')


def drop(event):
    # This function is called, when stuff is dropped into a widget
    stringvar.set(event.data)
    
def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")


# Without DnD hook you need to register the widget for every purpose,
# and bind it to the function you want to call
label_1 = tk.Label(root, textvar=stringvar, relief="solid")
label_1.pack(fill="both", expand=True, padx=10, pady=10)

label_1.register_drop_target("*")
label_1.bind("<<Drop>>", drop)

label_1.register_drag_source("*")
label_1.bind("<<DragInitCmd>>", drag_command)


# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
label_2 = ttk.Label(root, ondrop=drop, ondragstart=drag_command,
                    textvar=stringvar, padding=50, relief="solid")
label_2.pack(fill="both", expand=True, padx=10, pady=10)


root.mainloop()
```
