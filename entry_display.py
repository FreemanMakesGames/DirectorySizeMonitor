import tkinter as tk
import tkinter.ttk as ttk


class EntryDisplay:

    """ An abstract class that displays IEntry's. """

    def __init__( self, treeview ):

        self.treeview = treeview

    def display( self, i_entries, sorting_function, unit ):

        self.clear()

        i_entries = sorting_function( i_entries )

        self._insert_entries( "", i_entries, 1, unit )

    def clear( self ):

        self.treeview.delete( *self.treeview.get_children() )

    def _insert_entries( self, parent_key, i_entries, depth, unit ):

        raise NotImplementedError
