from entry_display import EntryDisplay

#from entry_info import *

import tkinter as tk


class EntryInfosDisplay( EntryDisplay ):

    def _insert_entries( self, parent_key, i_entries, depth, unit ):

        indent = "    " * ( depth - 1 )

        for entry_info in i_entries:

            self.treeview.insert( parent_key, tk.END, entry_info.path )
            self.treeview.set( entry_info.path, "content", indent + entry_info.path )
            self.treeview.set( entry_info.path, "size", str( entry_info.size / unit.divisor ) + unit.postfix )

            self._insert_entries( entry_info.path, entry_info.sub_entries, depth + 1, unit )
