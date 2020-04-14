import tkinter as tk
import tkinter.ttk as ttk


class EntryDisplay:

    """ An abstract class that displays IEntry's. """

    def __init__( self, treeview ):

        self.treeview = treeview

    def display( self, i_entries, unit ):

        self.clear()

        self._insert_entries( "", i_entries, 1, unit )

    def clear( self ):

        self.treeview.delete( *self.treeview.get_children() )

    def _insert_entries( self, parent_key, i_entries, depth, unit ):

        """ Insert all entries into the treeview.

        Different displays do it differently."""

        raise NotImplementedError

    def _insert_entry( self, parent_key, entry, path_column_name, size_column_name, unit, indent_count ):

        """ Insert a single entry into the treeview.
        
        entry.path will be the "treeview key" of this entry.
        """

        self.treeview.insert( parent_key, tk.END, entry.path )

        self.treeview.set( entry.path, path_column_name, "  " * indent_count + entry.path )

        self.treeview.set( entry.path, size_column_name, self._get_size_text( entry.size, unit ) )

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
