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

    def _insert_entry( self, parent_key, path, path_column_name, path_text, size_column_name, size_text ):

        """ Insert a single entry into the treeview."""

        self.treeview.insert( parent_key, tk.END, path )

        self.treeview.set( path, path_column_name, path_text )

        self.treeview.set( path, size_column_name, size_text )
