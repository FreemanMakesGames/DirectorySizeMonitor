import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import json

class DisplayedDirInfo:

    def __init__( self ):

        self.path = ""

        self.entryNamesAndSizes = []  # An "entry" is either a file or a directory.


class App:

    def __init__( self, master ):

        """ UI """

        masterFrame = tk.Frame( master )
        masterFrame.grid( row = 0, column = 0 )

        # Input

        inputFrame = tk.Frame( masterFrame )
        inputFrame.grid( row = 0, column = 0, sticky = tk.W )

        self.dirPathInputLabel = tk.Label( inputFrame, text = "Directory Path:" )
        self.dirPathInputLabel.grid( row = 0, column = 0 )

        self.dirPathInputBox = tk.Entry( inputFrame )
        self.dirPathInputBox.grid( row = 0, column = 1 )

        self.sortLexicallyButton = tk.Button( inputFrame, text = "Sort Lexically", command = self.displayAndSortLexically )
        self.sortLexicallyButton.grid( row = 0, column = 2 )

        self.sortBySizeButton = tk.Button( inputFrame, text = "Sort By Size", command = self.displayAndSortBySize )
        self.sortBySizeButton.grid( row = 0, column = 3 )

        self.saveButton = tk.Button( inputFrame, text = "Save Result", command = self.saveResult )
        self.saveButton.grid( row = 0, column = 4 )

        self.loadButton = tk.Button( inputFrame, text = "Load and Compare", command = self.loadAndCompare )
        self.loadButton.grid( row = 0, column = 5 )

        # Display

        displayFrame = tk.Frame( masterFrame )
        displayFrame.grid( row = 1, column = 0 )

        self.dirInfoTreeview = ttk.Treeview( displayFrame )
        self.dirInfoTreeview.config( show = ["headings"] )  # Hide the tree.
        self.dirInfoTreeview.config( columns = ( "content", "size" ) )
        self.dirInfoTreeview.heading( "content", text = "Content" )
        self.dirInfoTreeview.heading( "size", text = "Size" )
        self.dirInfoTreeview.grid( row = 0, column = 0 )

        """ Backend """

        self.displayedDirInfo = DisplayedDirInfo()

    """ Fill the text boxes with specified contents.
    
    An "entry" is either a file or a dir.
    
    :param entryNamesAndSizes: A list of pairs of entry name and size.
    """

    def display( self, entryNamesAndSizes ):

        for entryName, entrySize in entryNamesAndSizes:

            self.dirInfoTreeview.insert( "", tk.END, entryName )
            self.dirInfoTreeview.set( entryName, "content", entryName )
            self.dirInfoTreeview.set( entryName, "size", str( entrySize ) )

    """
    Display and *always* sort, because displayed content may go unsorted.
    The sorting functions will decide whether or not to recompute directory sizes,
    Based on if target dir path is different from displayed dir path.
    """

    def displayAndSortLexically( self ):

        self.clearDisplays()

        targetDirPath = self.dirPathInputBox.get()

        targetEntryNamesAndSizes = self.getDirInfoSortedLexically( targetDirPath )

        self.setDisplayedDirInfo( targetDirPath, targetEntryNamesAndSizes )

        self.display( targetEntryNamesAndSizes )

    """
    ( Similar to displayAndSortLexically above )
    """

    def displayAndSortBySize( self ):

        self.clearDisplays()

        targetDirPath = self.dirPathInputBox.get()

        targetEntryNamesAndSizes = self.getDirInfoSortedBySize( targetDirPath )

        self.setDisplayedDirInfo( targetDirPath, targetEntryNamesAndSizes )

        self.display( targetEntryNamesAndSizes )

    def clearDisplays( self ):

        self.dirInfoTreeview.delete( *self.dirInfoTreeview.get_children() )

    def setDisplayedDirInfo( self, path, entryNamesAndSizes ):

        self.displayedDirInfo.path = path
        self.displayedDirInfo.entryNamesAndSizes = entryNamesAndSizes

    def saveResult( self ):

        file = tkfiledialog.asksaveasfile( mode = 'w' )

        # If the dialog is closed with "Cancel"
        if file is None:
            return

        json.dump( self.displayedDirInfo.__dict__, file, indent = 4 )

        file.close()

    def loadAndCompare( self ):

        # Load

        file = tkfiledialog.askopenfile()

        # If the dialog is closed with "Cancel"
        if file is None:
            return

        try:
            loadedDirInfo = json.load( file )
        except ValueError:
            tkmessagebox.showerror( "Error", "The file you opened doesn't seem to be saved from this program." )
            return

        # Compare

        try:
            loadedDirPath = loadedDirInfo[ "path" ]
        except KeyError:
            tkmessagebox.showerror( "Error", "The result you loaded isn't from the same directory of what's currently displayed." )
            return

        

        file.close()

    """ Get a directory's info from scratch.
    
    This is expensive because it calls getDirSize.
    This should only be called if target dir path is different from displayed dir path.
    
    :return entryNamesAndSizes: A list of pairs of entry name and size, automatically sorted lexically.
    """

    def getDirInfo( self, targetDirPath ):

        entryNamesAndSizes = []

        for entry in os.scandir( targetDirPath ):

            if entry.is_file():

                entrySize = os.path.getsize( entry )

            elif entry.is_dir():

                entrySize = self.getDirSize( entry )

            entryNamesAndSizes.append( ( entry.name,  ) )

        return entryNamesAndSizes

    """
    Getting directory sizes is the most expensive computation here.
    Only do it if target dir path is different from displayed dir path.
    Always sort, which is relatively inexpensive.
    
    :return entryNamesAndSizes: A list of pairs of entry name and size, automatically sorted lexically.
    """

    def getDirInfoSortedLexically( self, targetDirPath ):

        if self.displayedDirInfo.path == targetDirPath:

            return sorted( self.displayedDirInfo.entryNamesAndSizes, key = lambda item: item[0].casefold() )

        else:

            entryNamesAndSizes = self.getDirInfo( targetDirPath )

        entryNamesAndSizes.sort( key = lambda item: item[0].casefold() )

        return entryNamesAndSizes

    """
    ( Similar to getDirInfoSortedLexically above )
    """

    def getDirInfoSortedBySize( self, targetDirPath ):

        if self.displayedDirInfo.path == targetDirPath:

            return sorted( self.displayedDirInfo.entryNamesAndSizes, key = lambda item: item[1] )

        else:

            entryNamesAndSizes = self.getDirInfo( targetDirPath )

        entryNamesAndSizes.sort( key = lambda item: item[1] )

        return entryNamesAndSizes

    """ Calculate a directory's size.
    
    This is expensive.
    """

    def getDirSize( self, dirPath ):

        dirSize = 0

        for subDirPath, subDirNames, fileNames in os.walk( dirPath ):

            for fileName in fileNames:

                filePath = os.path.join( subDirPath, fileName )

                if not os.path.islink( filePath ):
                    dirSize += os.path.getsize( filePath )

        return dirSize


window = tk.Tk()
window.title( "Folder Size Monitor" )
app = App( window )

window.mainloop()
