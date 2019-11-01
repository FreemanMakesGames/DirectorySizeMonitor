import tkinter as tk
import tkinter.ttk as ttk

class ReportWindow:

    def __init__( self, master, entryNamesAndDeltas ):

        masterFrame = tk.Frame( master )
        masterFrame.grid( row = 0, column = 0 )

        self.reportTreeview = ttk.Treeview( masterFrame )
        self.reportTreeview.config( show = ["headings"] )  # Hide the tree.
        self.reportTreeview.config( columns = ( "content", "size" ) )
        self.reportTreeview.heading( "content", text = "Content" )
        self.reportTreeview.heading( "size", text = "Size" )
        self.reportTreeview.grid( row = 0, column = 0 )
