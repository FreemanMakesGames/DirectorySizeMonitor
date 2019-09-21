import os
import tkinter as tk

class App:
    
    def __init__( self, master ):
        
        frame = tk.Frame( master )
        frame.grid( row = 0, column = 0 )
        
        self.dirPathInputBox = tk.Entry( frame )
        self.dirPathInputBox.grid( row = 0, column = 0 )
        
        self.scanButton = tk.Button( frame, text = "Scan", command = self.performScan )
        self.scanButton.grid( row = 0, column = 1 )

        self.dirContentTextBox = tk.Text( frame )
        self.dirContentTextBox.grid( row = 1, column = 0 )
        
        self.sizeTextBox = tk.Text( frame )
        self.sizeTextBox.grid( row = 1, column = 1 )
        
    def performScan( self ):

        currentDirPath = self.dirPathInputBox.get()
        
        for entry in os.scandir( currentDirPath ):
            
            self.dirContentTextBox.insert( tk.INSERT, entry.name + '\n' )
        
            if entry.is_file():
        
                sizeInBytes = os.path.getsize( entry )
        
            elif entry.is_dir():
        
                sizeInBytes = self.getDirSize( entry )
                
            self.sizeTextBox.insert( tk.INSERT, str( sizeInBytes ) + '\n' )
        
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
