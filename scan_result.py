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


class ScanResult:

    """ Scan result

    :var entry_infos: An array of every entry scanned. This isn't necessarily just the root's sub-entries.
                      If the depth is more than 1, this excludes root's sub-entries, and includes
                      the sub-entries below that.
    """

    def __init__( self, root_path, depth, entry_infos ):
        self.root_path = root_path
        self.depth = depth
        self.entry_infos = entry_infos
