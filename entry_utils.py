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


class EntryUtils:

    @staticmethod
    def get_flat_entries( entries, target_depth ):

        return EntryUtils.__get_flat_entries( entries, target_depth, 1 )

    @staticmethod
    def __get_flat_entries( entries, target_depth, operating_depth ):

        if operating_depth == target_depth:

            return entries.copy()

        result = []

        for entry in entries:

            if len( entry.sub_entries ) >= 1:

                result += EntryUtils.__get_flat_entries( entry.sub_entries, target_depth, operating_depth + 1 )

            else:

                result.append( entry )

        return result
