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


from enum import IntEnum


class EntryType( IntEnum ):

    Unset = 0
    File = 1
    Dir = 2


class IEntry:

    """ An "entry" is either a file or a directory.

    :var path: Full path name
    :var entry_type: An EntryType enum which can be either File or Dir.
    :var size: An entry's size, but for EntryDelta subclass, it's the delta of size..
    :var sub_entry_infos: If the entry is a dir, this will be an array of its sub-elements. Otherwise, it's empty.
    """

    def __init__( self, path, entry_type, size, sub_entries ):

        self.path = path
        self.entry_type = entry_type
        self.size = size
        self.sub_entries = sub_entries
