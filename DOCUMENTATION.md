# tkinterDnD documentation

### Note: It seems like color drag-n-drop don't work on Windows


<br>

## DnD with virtual events
If you have a plain tk widget you have register the widget as drag source, or drop target (or even both), and then you have to bind the DnD event to the function you want to call. For ttk widgets there's a [cool feature](#dnd_hook), with `ttkwidgets.hook`, which does these for you

```python
label = tk.Label(master)
label.register_drop_target((tkinterDnD.FILE, tkinterDnD.COLOR))
label.register_drag_source("*")
label.bind("<<Drop:Color>>", change_bg_color)
label.bind("<<DragStart>>", start_drag)
```

#### Here are the methods with which you can register your widget as a drag source or drop target
Method name | Desription
-|-
`register_drag_source` | Register the widget as a drag source, the first argument must be a tuple with the [acceptable DnD types](#dnd_types_constants), or a string if just one type is specified, if this argument isn't specified, then it will register the widget for any (`"tkinterDnD.ALL"`) type. `button` is optional, specifies which mouse button can be used to drag (default is `1`). Valid values are `1` (left mouse button), `2` (middle mouse button - wheel) and `3` (right mouse button).
`unregister_drag_source` | If the widget was a drag source, unregiters it, so no drag can be started from the widget anymore.
`register_drop_target` | Register the widget as a drop target, any number of arguments can be given in a tuple to specify acceptable drop types, if this argument isn't specified, then it will register the widget for any (`"tkinterDnD.ALL"`) type.
`unregister_drop_target` | If the widget was a drop target, unregiters it, so nothing can be dropped into the widget anymore.

#### And here's the full list of DnD events, tkinterDnD has replaced the original events of tkdnd with simple and clear event names, although you can use the tkdnd names as well
DnD event | Generated at | Same as (deprecated)
-|-|-
`<<Drop:Any>>` | This event is generated when anything was dropped into the widget. | `<<Drop>>`, `<<Drop:*>>`
`<<Drop:Text>>` | This event is generated when a text was dropped into the widget. | `<<Drop:DND_Text>>`
`<<Drop:File>>` | This event is generated when a file was dropped into the widget, e.g from a file manager. | `<<Drop:DND_Files>>`
`<<Drop:Color>>` | This event is generated when a color was dropped into the widget, e.g from the Inkscape palette. | `<<Drop:DND_Color>>`
`<<DragStart>>` | This event is generated when the user starts a drag from the widget, the called function should return a list with the drop action (which can be any of `tkinterDnD.COPY`, `tkinterDnD.MOVE`, `tkinterDnD.LINK`, `tkinterDnD.ASK`, and `tkinterDnD.PRIVATE`), the type of the content (which can be `tkinterDnD.TEXT`, `tkinterDnD.FILE` or `tkinterDnD.COLOR`), and the actual content. | `<<DragInitCmd>>`
`<<DragEnd>>` | This event is generated when the drag action has finished. | `<<DragEndCmd>>`
`<<DragEnter>>` | This event is generated when the mouse enters the widget during a drop action. | `<<DropEnter>>`
`<<DragLeave>>` | This event is generated when the mouse leaves the widget, without a drop happening. | `<<DropLeave>>`
`<<DragMove>>` | This events is generated when the mouse moves inside the window during a drop action. Thus, the script can decide that the drop can only occur at certain coordinates. The script binding for such an event can get the mouse coordinates and is expected to return the drop action (which can be any of `tkinterDnD.COPY`, `tkinterDnD.MOVE`, `tkinterDnD.LINK`, `tkinterDnD.ASK`, and `tkinterDnD.PRIVATE`). This event is not mandatory, but if it is defined, it has to return an action. In case an action is not returned, the drop is refused. | `<<DropPosition>>`


<br><br>
<a name="dnd_hook"></a>
## DnD with arguments

This feature only works for ttk widgets. When you import tkinterDnD it implicitly creates a hook for ttk widgets, and passes all DnD arguments to tkinterDnD. This way you don't have to register the widget as a drag source, or as drop target, and bind it, because tkinterDnD does these for you.

```python
label = ttk.Label(master, oncolordrop=change_accent_color, ondragstart=start_drag)
```
Argument name | Description
-|-
`ontextdrop` | Registers the widget as text drop target, and binds the given function to `<<Drop:Text>>` event.
`onfiledrop` | Registers the widget as file drop target, and binds the given function to `<<Drop:File>>` event.
`oncolordrop` | Registers the widget as color drop target, and binds the given function to `<<Drop:Color>>` event.
`ondrop` | Registers the widget as any type drop target, and binds the given function to `<<Drop:Any>>` event.
`ondragstart` | Registers the widget as any type drag source, and binds the given function to `<<DragStart>>` event.
`ondragend` | Registers the widget as any type drag source, and binds the given function to `<<DragEnd>>` event.
`ondragenter` | Registers the widget as any type drop target, and binds the given function to `<<DragEnter>>` event.
`ondragleave` | Registers the widget as any type drop target, and binds the given function to `<<DragLeave>>` event.
`ondragmove` | Registers the widget as any type drop target, and binds the given function to `<<DragMove>>` event.


<br><br>
<a name="methods"></a>
## Other methods
Method | Description
-|-
`get_dropfile_tempdir` | This method will return the temporary directory used by tkinterDnD for storing temporary files. When the tkdnd package is loaded, this temporary directory will be initialised to a proper directory according to the operating system.
`set_dropfile_tempdir` | This method will change the temporary directory used by tkinterDnD for storing temporary files. The only argument is `tempdir`, which means the temporary directory path.



<br><br>
<a name="constants"></a>
## TkinterDnD constants

### DnD actions
Constant name | Description | Actual value
-|-|-
`NONE` | Used when DnD action is none | none
`COPY` | Used when DnD action is copy. Useful, if you don't want to move a file, instead copy it. | copy
`MOVE` | Used when DnD action is move. Useful, if you don't want to copy a file, just move it. | move
`LINK` | Used when DnD action is link. Useful, if you don't want either copy or move a file, instead create a shortcut for it. | link
`ASK` | Used when DnD action is ask. The drop target can decide, what action to happen. | ask
`PRIVATE` | Used when DnD action is private. The drop can only happen inside the tkinter window. | private
`REFUSE_DROP` | Used when DnD action is refuse_drop. Use it, when the drag action should be refused right after it starts (when the init function is returned this action) | refuse_drop

<a name="dnd_types_constants"></a>
### DnD types
Constant name | Description | Actual value
-|-|-
`TEXT` | The drag content should be interpreted as simple text. | DND_Text
`FILE` | The drag content should be interpreted as a file path. | DND_Files
`COLOR` | The drag content should be interpreted as a hex color name. | DND_Color
`ALL` | The drag content can be any of text, file, color | *


### Windows specific
Note: I currently didn't mess with these on Windows, so I can't provide any useful info
Constant name | Description | Actual value
-|-|-
`CF_UNICODETEXT` | Text transfer encoded in Unicode. | CF_UNICODETEXT
`CF_TEXT` | Text transfer with application dependent encoding. If an encoding locale is specified through `CF_LOCALE` it is used, else the system encoding is used for the conversion. | CF_TEXT
`CF_HDROP` | Files transfer encoded in UTF-8. | CF_HDROP
`FileGroupDescriptor` | These two types are used for transferring a set of files that do not appear physically on disk, like files from compressed folders or Outlook e-mail messages. File names are transferred as in the `CF_TEXT` type, while file contents are transferred in binary. tkinterDnD retrieves both the file names and the file contents, and saves then in a temporary directory. When the transfer is complete, the file names of the saved files in the temporary folder are returned. Note that tkinterDnD support this type pair only as drop targets and not as drag sources. | FileGroupDescriptor - FileContents
`FileGroupDescriptorW` | These two types are used for transferring a set of files that do not appear physically on disk, like files from compressed folders or Outlook e-mail messages. File names are transferred as in the `CF_UNICODETEXT` type, while file contents are transferred in binary. tkinterDnD retrieves both the file names and the file contents, and saves then in a temporary directory. When the transfer is complete, the file names of the saved files in the temporary folder are returned. Note that tkinterDnD support this type pair only as drop targets and not as drag sources. | FileGroupDescriptorW - FileContents
