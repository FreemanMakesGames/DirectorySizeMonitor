# Copyright 2020 FreemanMakesGames https://www.freemanmakesgames.pro

# This file is part of DirectorySizeMonitor.
#
# DirectorySizeMonitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DirectorySizeMonitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DirectorySizeMonitor. If not, see <https://www.gnu.org/licenses/>.


from entry_display import EntryDisplay

from entry_delta import *

import tkinter as tk


class EntryDeltasDisplay( EntryDisplay ):

    def _insert_entries( self, parent_key, i_entries, depth, unit, root_path_str_for_trimming ):

        for entry_delta in i_entries:

            super()._insert_entry( parent_key, entry_delta, "entry", "delta", unit, depth - 1,
                                   root_path_str_for_trimming )

            existing_tags = self.treeview.item( entry_delta.path )[ "tags" ]

            # Assign tag based on delta type, for highlighting.
            if entry_delta.delta_type == EntryDeltaType.NewEntry:
                self.treeview.item( entry_delta.path, tags = ( existing_tags, ) + ( "new_entry", ) )
            elif entry_delta.delta_type == EntryDeltaType.Deleted:
                self.treeview.item( entry_delta.path, tags = ( existing_tags, ) + ( "deleted", ) )

            self._insert_entries( entry_delta.path, entry_delta.sub_entries, depth + 1, unit,
                                  root_path_str_for_trimming )

    def _highlight_entries( self ):

        """ Highlight new and deleted entry rows based on their tag.

        In addition to base class's giving dir entries blue text."""

        super()._highlight_entries()

        self.treeview.tag_configure( "new_entry", background = "#81ed81" )  # Light green
        self.treeview.tag_configure( "deleted", background = "#ff9191" )  # Light red
