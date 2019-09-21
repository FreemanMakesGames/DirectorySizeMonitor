import os
import tkinter as tk

class App:
    
    def __init__( self, master ):
        
        frame = tk.Frame( master )
        frame.grid( row = 0, column = 0 )
        
        self.dirPathInputBox = tk.Entry( frame )
        self.dirPathInputBox.grid( row = 0, column = 0 )
        
        self.sortLexicallyButton = tk.Button( frame, text = "Sort Lexically", command = self.displayAndSortLexically )
        self.sortLexicallyButton.grid( row = 0, column = 1 )
        
        self.sortBySizeButton = tk.Button( frame, text = "Sort By Size", command = self.displayAndSortBySize )
        self.sortBySizeButton.grid( row = 0, column = 2 )

        self.dirContentTextBox = tk.Text( frame )
        self.dirContentTextBox.grid( row = 1, column = 0 )
        
        self.sizeTextBox = tk.Text( frame )
        self.sizeTextBox.grid( row = 1, column = 1 )
        
    """ Fill the text boxes with specified contents.
    
    An "entry" is either a file or a dir.
    
    :param entryNamesAndSizes: A list of pairs of entry name and size.
    """
    def display( self, entryNamesAndSizes ):
        
        for entryName, entrySize in entryNamesAndSizes:
            
            self.dirContentTextBox.insert( tk.INSERT, entryName + '\n' )
            
            self.sizeTextBox.insert( tk.INSERT, str( entrySize ) + '\n' )
        
    def displayAndSortLexically( self ):
        
        self.clearDisplays()
        
        self.display( self.getDirInfoSortedLexically( self.dirPathInputBox.get() ) )
        
    def displayAndSortBySize( self ):
        
        self.clearDisplays()
        
        self.display( self.getDirInfoSortedBySize( self.dirPathInputBox.get () ) )
        
    def clearDisplays( self ):
        
        self.dirContentTextBox.delete( 1.0, tk.END )
        self.sizeTextBox.delete( 1.0, tk.END )
        
    """
    :return entryNamesAndSizes: A list of pairs of entry name and size, automatically sorted lexically.
    """
    def getDirInfoSortedLexically( self, targetDirPath ):
        
        entryNamesAndSizes = []
        
        for entry in os.scandir( targetDirPath ):
        
            if entry.is_file():
        
                entrySize = os.path.getsize( entry )
        
            elif entry.is_dir():
        
                entrySize = self.getDirSize( entry )
                
            entryNamesAndSizes.append( ( entry.name, entrySize ) )
                
        return entryNamesAndSizes
    
    """
    :return entryNamesAndSizes: A list of pairs of entry name and size, sorted by size.
    """
    def getDirInfoSortedBySize( self, targetDirPath ):
        
        # TODO: Optimize?
        entryNamesAndSizes = self.getDirInfoSortedLexically( targetDirPath )
        
        entryNamesAndSizes.sort( key = lambda item: item[1] )
        
        return entryNamesAndSizes
        
    """ Calculate a directory's size.
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
