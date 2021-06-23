#
# Tcl package index file
#

set dir "/home/benedek/.local/lib/python3.8/site-packages/TkinterDND/"

package ifneeded tkdnd 2.8 \
  "source \{$dir/tkdnd.tcl\} ; \
   tkdnd::initialise \{$dir\} libtkdnd2.8.so tkdnd"
