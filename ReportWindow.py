import tkinter as tk
import tkinter.ttk as ttk

class ReportWindow:

    def __init__( self, master, entryDeltas ):

        masterFrame = tk.Frame( master )
        masterFrame.grid( row = 0, column = 0 )

        self.reportTreeview = ttk.Treeview( masterFrame )
        self.reportTreeview.config( show = ["headings"] )  # Hide the tree.
        self.reportTreeview.config( columns = ( "content", "size" ) )
        self.reportTreeview.heading( "content", text = "Content" )
        self.reportTreeview.heading( "size", text = "Size" )
        self.reportTreeview.grid( row = 0, column = 0 )

        # TODO: Refactoring: Duplicate code in __main.py__ display function.
        for entryDelta in entryDeltas:

            entryName = entryDelta.name
            entrySizeDelta = entryDelta.size

            self.reportTreeview.insert( "", tk.END, entryName )
            self.reportTreeview.set( entryName, "content", entryName )
            self.reportTreeview.set( entryName, "size", str( entrySizeDelta ) )
