from entry_display import EntryDisplay

#from entry_info import *

import tkinter as tk


class EntryInfosDisplay( EntryDisplay ):

    def _insert_entries( self, parent_key, i_entries, depth, unit ):

        for entry_info in i_entries:

            super()._insert_entry( parent_key, entry_info, "content", "size", unit, depth - 1 )

            self._insert_entries( entry_info.path, entry_info.sub_entries, depth + 1, unit )
