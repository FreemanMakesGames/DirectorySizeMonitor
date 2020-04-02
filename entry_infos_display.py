import tkinter as tk
import tkinter.ttk as ttk

class EntryInfosDisplay:

    def __init__( self, treeview ):

        self.treeview = treeview

    def display( self, entry_infos, sorting_function, unit ):

        self.clear()

        entry_infos = sorting_function( entry_infos )

        self.insert_entry_infos( "", entry_infos, 1, unit )

    def clear( self ):

        self.treeview.delete( *self.treeview.get_children() )

    def insert_entry_infos( self, parent_key, entry_infos, depth, unit ):

        indent = "    " * ( depth - 1 )

        for entry_info in entry_infos:

            self.treeview.insert( parent_key, tk.END, entry_info.path )
            self.treeview.set( entry_info.path, "content", indent + entry_info.path )
            self.treeview.set( entry_info.path, "size", str( entry_info.size / unit.divisor ) + unit.postfix )

            self.insert_entry_infos( entry_info.path, entry_info.sub_entry_infos, depth + 1, unit )
