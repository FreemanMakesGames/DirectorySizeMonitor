from entry_interface import *

import os
import tkinter as tk
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


import tkinter.ttk as ttk


class EntryDisplay:

    """ An abstract class that displays IEntry's. """

    # TODO: This can be refactored. Maybe take in parameters of column, column names, column widths,
    #  Hiding tree or not, and so on, and then build the tree inside the class constructor instead?
    def __init__( self, treeview ):

        self.treeview = treeview

    def display( self, i_entries, unit, root_path_str_for_trimming ):

        self.clear()

        self._insert_entries( "", i_entries, 1, unit, root_path_str_for_trimming )

        self._highlight_entries()

    def clear( self ):

        self.treeview.delete( *self.treeview.get_children() )

    def _insert_entries( self, parent_key, i_entries, depth, unit, root_path_str_for_trimming ):

        """ Insert all entries into the treeview.

        Different displays do it differently."""

        raise NotImplementedError

    def _insert_entry( self, parent_key, entry, path_column_name, size_column_name, unit, indent_count,
                       root_path_str_for_trimming ):

        """ Insert a single entry into the treeview.
        
        entry.path will be the "treeview key" of this entry.
        """

        self.treeview.insert( parent_key, tk.END, entry.path )

        trimmed_path = entry.path.replace( root_path_str_for_trimming + '/', "" )

        self.treeview.set( entry.path, path_column_name, "--" * indent_count + trimmed_path )

        self.treeview.set( entry.path, size_column_name, self._get_size_text( entry.size, unit ) )

        # Blue text for dir
        if entry.entry_type == EntryType.Dir:
            self.treeview.item( entry.path, tags = ( "is_dir", ) )

    def _highlight_entries( self ):

        """ Meant for override. Highlight entry rows if it's a dir, is a new or deleted entry, and so on.

        For base class, simply give dir entries blue text."""

        self.treeview.tag_configure( "is_dir", foreground = "#0000ff" )

    def _get_size_text( self, size_in_bytes, unit ):

        """ Trim an entry size to have less digits.

        If unit is byte, simply return size concatenated with "B".

        Otherwise, divide size with divisor.
        If the result's absolute value >= 1, round it to have 1 digit after decimal point.
        If the result's absolute value is between 0 and 1, round it to have 2 significant digits.
        """

        if unit.postfix == "B":

            return str( size_in_bytes ) + "B"

        else:

            size_in_unit = size_in_bytes / unit.divisor

            if abs( size_in_unit ) >= 1:

                return str( round( size_in_unit, 1 ) ) + unit.postfix

            else:

                # 2g means to drop digits after 2 significant digits.
                return "{0:.2g}".format( size_in_unit ) + unit.postfix
