import os
import tkinter as tk
        
class DisplayedDirInfo:
    
    def __init__( self ):
        
        self.path = ""
        
        self.entryNamesAndSizes = []

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
        
        # Display
        
        displayFrame = tk.Frame( masterFrame )
        displayFrame.grid( row = 1, column = 0 )

        self.dirContentTextBox = tk.Text( displayFrame, state = tk.DISABLED )
        self.dirContentTextBox.grid( row = 1, column = 0 )
        
        self.sizeTextBox = tk.Text( displayFrame, state = tk.DISABLED )
        self.sizeTextBox.grid( row = 1, column = 1 )
        
        """ Backend """
        
        self.displayedDirInfo = DisplayedDirInfo()
        
    """ Fill the text boxes with specified contents.
    
    An "entry" is either a file or a dir.
    
    :param entryNamesAndSizes: A list of pairs of entry name and size.
    """
    def display( self, entryNamesAndSizes ):
        
        self.toggleTextBoxesEditing( True )
        
        for entryName, entrySize in entryNamesAndSizes:
            
            self.dirContentTextBox.insert( tk.INSERT, entryName + '\n' )
            
            self.sizeTextBox.insert( tk.INSERT, str( entrySize ) + '\n' )
            
        self.toggleTextBoxesEditing( False )
        
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
        
        self.toggleTextBoxesEditing( True )
        
        self.dirContentTextBox.delete( 1.0, tk.END )
        self.sizeTextBox.delete( 1.0, tk.END )
        
        self.toggleTextBoxesEditing( False )
        
    def toggleTextBoxesEditing( self, enabled ):
        
        if enabled:
            
            self.dirContentTextBox.config( state = tk.NORMAL )
            self.sizeTextBox.config( state = tk.NORMAL )
            
        else:
            
            self.dirContentTextBox.config( state = tk.DISABLED )
            self.sizeTextBox.config( state = tk.DISABLED )
        
    def setDisplayedDirInfo( self, path, entryNamesAndSizes ):
        
        self.displayedDirInfo.path = path
        self.displayedDirInfo.entryNamesAndSizes = entryNamesAndSizes
        
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
                
            entryNamesAndSizes.append( ( entry.name, entrySize ) )
                
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
