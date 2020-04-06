from entry_display import EntryDisplay

from entry_delta import *

import tkinter as tk


class EntryDeltasDisplay( EntryDisplay ):

    def _insert_entries( self, parent_key, i_entries, depth, unit ):

        indent = "    " * ( depth - 1 )

        for entry_delta in i_entries:

            self.treeview.insert( parent_key, tk.END, entry_delta.path )
            self.treeview.set( entry_delta.path, "entry", indent + entry_delta.path )
            self.treeview.set( entry_delta.path, "delta", str( entry_delta.size / unit.divisor ) + unit.postfix )

            # Assign tag based on delta type, for highlighting.
            if entry_delta.delta_type == EntryDeltaType.NewEntry:
                self.treeview.item( entry_delta.path, tags = "new_entry" )
            elif entry_delta.delta_type == EntryDeltaType.Deleted:
                self.treeview.item( entry_delta.path, tags = "deleted" )

            self._insert_entries( entry_delta.path, entry_delta.sub_entries, depth + 1, unit )

        # Highlight rows based on their tag.
        self.treeview.tag_configure( "new_entry", background = "#81ed81" )  # Light green
        self.treeview.tag_configure( "deleted", background = "#ff9191" )  # Light red