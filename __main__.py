from reportwindow import ReportWindow

import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import json

class EntryInfo:

    """
    An "entry" is either a file or a directory.
    """

    def __init__( self, name, size ):

        self.name = name

        self.size = size

class DirInfo:

    def __init__( self, path, entryInfos ):

        self.path = path

        self.entryInfos = entryInfos

class MainWindow:

    def __init__( self, master ):

        """ UI """

        masterFrame = tk.Frame( master )
        masterFrame.grid( row = 0, column = 0 )

        # Input

        inputFrame = tk.Frame( masterFrame )
        inputFrame.grid( row = 0, column = 0, sticky = tk.W )

        self.scanButton = tk.Button( inputFrame, text = "Scan", command = self.onScanButtonClicked )
        self.scanButton.grid( row = 0, column = 0 )

        self.sortLexicallyButton = tk.Button( inputFrame, text = "Sort Lexically",
                                              command = lambda:
                                              self.onSortButtonClicked( self.getEntryInfosSortedLexically ) )
        self.sortLexicallyButton.grid( row = 0, column = 1 )

        self.sortBySizeButton = tk.Button( inputFrame, text = "Sort By Size",
                                           command = lambda:
                                           self.onSortButtonClicked( self.getEntryInfosSortedBySize ) )
        self.sortBySizeButton.grid( row = 0, column = 2 )

        self.saveButton = tk.Button( inputFrame, text = "Save Result", command = self.saveResult )
        self.saveButton.grid( row = 0, column = 3 )

        self.loadButton = tk.Button( inputFrame, text = "Load and Compare", command = self.loadAndCompare )
        self.loadButton.grid( row = 0, column = 4 )

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

        self.currentDirInfo = DirInfo( "", [] )

    def onScanButtonClicked( self ):

        targetDirPath = tkfiledialog.askdirectory()

        # If the dialog is closed with "Cancel"
        if targetDirPath == "":
            return

        self.clearDisplays()

        targetEntryInfos = self.getDirInfo( targetDirPath )

        self.setCurrentDirInfo( targetDirPath, targetEntryInfos )

        self.display( targetEntryInfos )

    def onSortButtonClicked( self, sortingFunction ):

        if self.currentDirInfo.path == "":
            tkmessagebox.showerror( "Error", "You haven't scanned any directory yet." )
            return

        self.clearDisplays()

        targetEntryInfos = sortingFunction()

        self.display( targetEntryInfos )

    def display( self, entryInfos ):

        """ Fill the text boxes with specified contents.

        An "entry" is either a file or a dir.

        :param entryInfos: A list of EntryInfo
        """

        for entryInfo in entryInfos:

            entryName = entryInfo.name
            entrySize = entryInfo.size

            self.dirInfoTreeview.insert( "", tk.END, entryName )
            self.dirInfoTreeview.set( entryName, "content", entryName )
            self.dirInfoTreeview.set( entryName, "size", str( entrySize ) )

    def clearDisplays( self ):

        self.dirInfoTreeview.delete( *self.dirInfoTreeview.get_children() )

    def setCurrentDirInfo( self, path, entryInfos ):

        self.currentDirInfo.path = path
        self.currentDirInfo.entryInfos = entryInfos

    def saveResult( self ):

        file = tkfiledialog.asksaveasfile( mode = 'w' )

        # If the dialog is closed with "Cancel"
        if file is None:
            return

        json.dump( self.currentDirInfo.__dict__, file, default = lambda o: o.__dict__, indent = 4 )

        file.close()

    def loadAndCompare( self ):

        file = tkfiledialog.askopenfile()

        # If the dialog is closed with "Cancel"
        if file is None:
            return

        # Load and validate.

        try:
            loadedDirInfo = json.load( file )
        except ValueError:
            tkmessagebox.showerror( "Error", "The file you opened is not of JSON format, thus it's not saved from this "
                                             "program." )
            return

        file.close()

        # TODO: Refactor: '2' is hardcoded here.
        if len( loadedDirInfo.keys() ) != 2:
            tkmessagebox.showerror( "Error", "Although the file you opened is of JSON format, it's not saved from this "
                                             "program." )
            return

        try:
            loadedDirPath = loadedDirInfo[ "path" ]
        except KeyError:
            tkmessagebox.showerror( "Error", "Although the file you opened is of JSON format, it's not saved from this "
                                             "program." )
            return
        else:
            if ( loadedDirPath != self.currentDirInfo.path):
                tkmessagebox.showerror( "Error",
                                        "The result you loaded isn't describing the same directory of what's currently "
                                        "displayed." )
                return


        try:
            loadedEntryInfos = loadedDirInfo[ "entryInfos" ]
        except KeyError:
            tkmessagebox.showerror( "Error", "The file is corrupted." )
            return

        # Compare.

        entryDeltas = []  # TODO: Refactoring: Should it use a new class, despite having the same data types as fields?

        for entryInfo in self.currentDirInfo.entryInfos:

            entryMatches = False

            for loadedEntryInfo in loadedEntryInfos:  # loadedEntryInfo is a dict.

                if entryInfo.name == loadedEntryInfo[ "name" ]:

                    entryMatches = True

                    if entryInfo.size != loadedEntryInfo[ "size" ]:

                        entryDeltas.append( EntryInfo( entryInfo.name, entryInfo.size - loadedEntryInfo[ "size" ] ) )

                    break

            if not entryMatches:

                entryDeltas.append( EntryInfo( entryInfo.name, entryInfo.size ) )

        for loadedEntryInfo in loadedEntryInfos:

            entryDeleted = True

            for entryInfo in self.currentDirInfo.entryInfos:

                if loadedEntryInfo[ "name" ] == entryInfo.name:

                    entryDeleted = False

                    break

            if entryDeleted:

                entryDeltas.append( EntryInfo( loadedEntryInfo[ "name" ], -loadedEntryInfo[ "size" ] ) )

        print( entryDeltas )

        reportWindowWidget = tk.Tk()
        reportWindowWidget.title( "Report" )
        reportWindow = ReportWindow( reportWindowWidget, entryDeltas )

        reportWindowWidget.mainloop()

    def getDirInfo( self, targetDirPath ):

        """ Get a directory's info from scratch.

        This is expensive because it calls getDirSize.

        :return entryNamesAndSizes: A list of pairs of entry name and size, automatically sorted lexically.
        """

        entryInfos = []

        for entry in os.scandir( targetDirPath ):

            if entry.is_file():

                entrySize = os.path.getsize( entry )

            elif entry.is_dir():

                entrySize = self.getDirSize( entry )

            entryInfos.append( EntryInfo( entry.name, entrySize  ) )

        return entryInfos

    def getEntryInfosSortedLexically( self ):

        return sorted( self.currentDirInfo.entryInfos, key = lambda item: item.name.casefold() )

    def getEntryInfosSortedBySize( self ):

        return sorted( self.currentDirInfo.entryInfos, key = lambda item: item.size )

    def getDirSize( self, dirPath ):

        """ Calculate a directory's size.

        This is expensive.
        """

        dirSize = 0

        for subDirPath, subDirNames, fileNames in os.walk( dirPath ):

            for fileName in fileNames:

                filePath = os.path.join( subDirPath, fileName )

                if not os.path.islink( filePath ):
                    dirSize += os.path.getsize( filePath )

        return dirSize

mainWindowWidget = tk.Tk()
mainWindowWidget.title( "Folder Size Monitor" )
mainWindow = MainWindow( mainWindowWidget )

mainWindowWidget.mainloop()
