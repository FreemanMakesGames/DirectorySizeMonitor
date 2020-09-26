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

#from entry_info import *

import tkinter as tk


class EntryInfosDisplay( EntryDisplay ):

    def _insert_entries( self, parent_key, i_entries, depth, unit, root_path_str_for_trimming ):

        for entry_info in i_entries:

            super()._insert_entry( parent_key, entry_info, "content", "size", unit, depth - 1,
                                   root_path_str_for_trimming )

            self._insert_entries( entry_info.path, entry_info.sub_entries, depth + 1, unit,
                                  root_path_str_for_trimming )
