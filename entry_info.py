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


from entry_interface import IEntry


class EntryInfo( IEntry ):

    def __init__( self, path, entry_type, size, sub_entry_infos ):

        super().__init__( path, entry_type, size, sub_entry_infos )
