from entry_display import EntryDisplay

from entry_delta import *

import tkinter as tk


class EntryDeltasDisplay( EntryDisplay ):

    def _insert_entries( self, parent_key, i_entries, depth, unit ):

        for entry_delta in i_entries:

            super()._insert_entry( parent_key, entry_delta, "entry", "delta", unit, depth - 1 )

            existing_tags = self.treeview.item( entry_delta.path )[ "tags" ]

            # Assign tag based on delta type, for highlighting.
            if entry_delta.delta_type == EntryDeltaType.NewEntry:
                self.treeview.item( entry_delta.path, tags = ( existing_tags, ) + ( "new_entry", ) )
            elif entry_delta.delta_type == EntryDeltaType.Deleted:
                self.treeview.item( entry_delta.path, tags = ( existing_tags, ) + ( "deleted", ) )

            self._insert_entries( entry_delta.path, entry_delta.sub_entries, depth + 1, unit )

    def _highlight_entries( self ):

        """ Highlight new and deleted entry rows based on their tag.

        In addition to base class's giving dir entries blue text."""

        super()._highlight_entries()

        self.treeview.tag_configure( "new_entry", background = "#81ed81" )  # Light green
        self.treeview.tag_configure( "deleted", background = "#ff9191" )  # Light red
