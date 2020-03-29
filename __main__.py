from reportwindow import ReportWindow

import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import json


class EntryType:
    Unset = 0
    File = 1
    Dir = 2


class EntryInfo:

    """ An "entry" is either a file or a directory.

    :var path: Full path name
    :var entry_type: An EntryType enum which can be either File or Dir.
    :var sub_entry_infos: If the entry is a dir, this will be an array of its sub-elements. Otherwise, it's empty.
    """

    def __init__( self, path, entry_type, size, sub_entry_infos ):
        self.path = path
        self.entry_type = entry_type
        self.size = size
        self.sub_entry_infos = sub_entry_infos


class EntryDelta:

    """ How much has the size of an entry at a certain path changed"""

    def __init__( self, path, delta ):
        self.path = path
        self.delta = delta


class ScanResult:

    """ Scan result

    :var entry_infos: An array of every entry scanned. This isn't necessarily just the root's sub-entries.
                      If the depth is more than 1, this excludes root's sub-entries, and includes
                      the sub-entries below that.
    """

    def __init__( self, root_path, depth, entry_infos ):
        self.root_path = root_path
        self.depth = depth
        self.entry_infos = entry_infos

class MainWindow:

    def __init__( self, master ):

        """ UI """

        master_frame = tk.Frame( master )
        master_frame.grid( row = 0, column = 0 )

        # Input

        input_frame = tk.Frame( master_frame )
        input_frame.grid( row = 0, column = 0, sticky = tk.W )

        self.scan_button = tk.Button( input_frame, text = "Scan", command = self.on_scan_button_clicked )
        self.scan_button.grid( row = 0, column = 0 )

        self.sort_lexically_button = tk.Button( input_frame, text = "Sort Lexically",
                                                command = lambda:
                                              self.on_sort_button_clicked( self.get_entry_infos_sorted_lexically ) )
        self.sort_lexically_button.grid( row = 0, column = 1 )

        self.sort_by_size_button = tk.Button( input_frame, text = "Sort By Size",
                                              command = lambda:
                                           self.on_sort_button_clicked( self.get_entry_infos_sorted_by_size ) )
        self.sort_by_size_button.grid( row = 0, column = 2 )

        self.save_button = tk.Button( input_frame, text = "Save Result", command = self.save_result )
        self.save_button.grid( row = 0, column = 3 )

        self.load_button = tk.Button( input_frame, text = "Load and Compare", command = self.load_and_compare )
        self.load_button.grid( row = 0, column = 4 )

        ## Unit options
        self.unit_options_label = tk.Label( input_frame, text = "Unit" )
        self.unit_options_label.grid( row = 1, column = 0 )
        self.unit_divisor = 1
        self.unit_options = ["B", "KB", "MB", "GB"]
        self.unit_option = tk.StringVar()
        self.unit_option.set( self.unit_options[ 0] )
        self.unit_options_menu = tk.OptionMenu( input_frame, self.unit_option, *self.unit_options, command = lambda selected:
                                              self.on_unit_selected( selected ) )
        self.unit_options_menu.grid( row = 1, column = 1 )

        ## Depth input
        self.depth_label = tk.Label( input_frame, text = "Depth" )
        self.depth_label.grid( row = 1, column = 2 )
        self.depth_entry_box = tk.Entry( input_frame )
        self.depth_entry_box.grid( row = 1, column = 3 )
        self.depth = 1
        self.depth_entry_box.insert( 0, self.depth )

        # Display

        display_frame = tk.Frame( master_frame )
        display_frame.grid( row = 1, column = 0 )

        self.dir_info_tree_view = ttk.Treeview( display_frame )
        self.dir_info_tree_view.config( show = ["headings"] )  # Hide the tree.
        self.dir_info_tree_view.config( columns = ("content", "size") )
        # Set column width
        self.dir_info_tree_view.column( "content", width = 600 )
        self.dir_info_tree_view.column( "size", width = 200 )
        self.dir_info_tree_view.heading( "content", text = "Content" )
        self.dir_info_tree_view.heading( "size", text = "Size" )
        self.dir_info_tree_view.grid( row = 0, column = 0 )

        """ Backend """

        self.current_scan_result = ScanResult( "", self.depth, [] )

        self.MAXDEPTH = 5

    def on_scan_button_clicked( self ):

        """This function should be the only place that carries out scanning."""

        target_dir_path = tkfiledialog.askdirectory()

        # If the dialog is closed with "Cancel", return.
        if target_dir_path == "":
            return

        # Get depth.
        input_depth_string = self.depth_entry_box.get()
        if not input_depth_string:  # Empty input
            self.set_depth( 1 )
        else:  # Non-empty input
            try:  # Integer input
                self.depth = int( input_depth_string )
                if self.depth < 1 or self.depth > self.MAXDEPTH:
                    tkmessagebox.showerror( "Error", "Depth can only be between 1 to 5. Resetting to 1." )
                    self.set_depth( 1 )
            except ValueError:  # Bad input
                tkmessagebox.showerror( "Error", "Scan depth isn't an integer. Depth is set to 1." )
                self.set_depth( 1 )

        target_entry_infos = self.get_dir_info( target_dir_path, 1 )

        self.set_current_scan_result( target_dir_path, self.depth, target_entry_infos )

        self.clear_displays()
        self.display( target_entry_infos )

    def on_sort_button_clicked( self, sorting_function ):

        if self.current_scan_result.root_path == "":
            tkmessagebox.showerror( "Error", "You haven't scanned any directory yet." )
            return

        self.clear_displays()

        target_entry_infos = sorting_function()

        self.display( target_entry_infos )

    def on_unit_selected( self, selected ):

        self.unit_divisor = 1024 ** self.unit_options.index( selected )

        self.clear_displays()
        self.display( self.current_scan_result.entry_infos )

    def display( self, entry_infos ):

        """ Fill the text boxes with specified contents.

        :param entry_infos: A list of EntryInfo
        """

        for entry_info in entry_infos:

            self.dir_info_tree_view.insert( "", tk.END, entry_info.path )
            self.dir_info_tree_view.set( entry_info.path, "content", entry_info.path )
            self.dir_info_tree_view.set( entry_info.path, "size", str( entry_info.size / self.unit_divisor ) +
                                         self.unit_option.get() )

    def clear_displays( self ):

        self.dir_info_tree_view.delete( *self.dir_info_tree_view.get_children() )

    def set_depth( self, target_depth ):
        self.depth = target_depth
        self.depth_entry_box.delete( 0, tk.END )
        self.depth_entry_box.insert( 0, target_depth )

    def save_result( self ):

        file = tkfiledialog.asksaveasfile( mode = 'w' )

        # If the dialog is closed with "Cancel"
        if file is None:
            return

        json.dump( self.current_scan_result.__dict__, file, default = lambda o: o.__dict__, indent = 4 )

        file.close()

    def load_and_compare( self ):

        file = tkfiledialog.askopenfile()

        # If the dialog is closed with "Cancel"
        if file is None:
            return

        # Load and validate.

        try:
            loaded_scan_result = json.load( file )
        except ValueError:
            tkmessagebox.showerror( "Error", "The file you opened is not of JSON format, thus it's not saved from this "
                                             "program." )
            return

        file.close()

        try:
            loaded_root_path = loaded_scan_result[ "root_path" ]
        except KeyError:
            self.report_unknown_json()
            return
        else:
            if loaded_root_path != self.current_scan_result.root_path:
                tkmessagebox.showerror( "Error", "The result you loaded isn't describing the same directory of what's"
                                                 "currently displayed." )
                return

        try:
            loaded_depth = loaded_scan_result[ "depth" ]
        except KeyError:
            self.report_unknown_json()
            return
        else:
            if loaded_depth != self.current_scan_result.depth:
                tkmessagebox.showerror( "Error", "The result you loaded is describing the same directory of"
                                                 "what's currently displayed, but the depth isn't the same."
                                                 "So it can't be compared." )
                return

        try:
            loaded_entry_infos = loaded_scan_result[ "entry_infos" ]
        except KeyError:
            tkmessagebox.showerror( "Error", "The file is corrupted." )
            return

        # Compare.

        entry_deltas = []  # TODO: Refactoring: Should it use a new class, despite having the same data types as fields?

        for entry_info in self.current_scan_result.entry_infos:

            entry_matches = False

            for loaded_entry_info in loaded_entry_infos:  # loadedEntryInfo is a dict.

                if entry_info.path == loaded_entry_info[ "path" ]:

                    entry_matches = True

                    if entry_info.size != loaded_entry_info[ "size" ]:

                        entry_deltas.append( EntryDelta( entry_info.path, entry_info.size -
                                                         loaded_entry_info[ "size" ] ) )

                    break

            # The entry is newly created.
            if not entry_matches:

                entry_deltas.append( EntryDelta( entry_info.path, entry_info.size ) )

        for loaded_entry_info in loaded_entry_infos:

            entry_deleted = True

            for entry_info in self.current_scan_result.entry_infos:

                if loaded_entry_info[ "path" ] == entry_info.path:

                    entry_deleted = False

                    break

            if entry_deleted:

                entry_deltas.append( EntryDelta( loaded_entry_info[ "path" ], -loaded_entry_info[ "size" ] ) )

        print( entry_deltas )

        report_window_widget = tk.Tk()
        report_window_widget.title( "Report" )
        report_window = ReportWindow( report_window_widget, entry_deltas )

        report_window_widget.mainloop()

    def get_dir_info( self, target_dir_path, operating_depth ):

        """ Get a directory's info from scratch.

        This is expensive because it calls getDirSize.

        :param target_dir_path: A full path name of current directory.
        :return entryNamesAndSizes: A list of pairs of entry name and size, automatically sorted lexically.
        """

        entry_infos = []

        for entry in os.scandir( target_dir_path ):

            # Init entry info.
            entry_info = EntryInfo( target_dir_path + "/" + entry.name, EntryType.Unset, 0, [] )

            if entry.is_file():

                entry_info.entry_type = EntryType.File
                entry_info.size = os.path.getsize( entry )

                entry_infos.append( entry_info )

                continue

            elif entry.is_dir():

                # If depth isn't exhausted, recursively get and append all sub-entries, but exclude itself.
                if operating_depth < self.depth:
                    for entry_info in self.get_dir_info( entry_info.path, operating_depth + 1 ):
                        entry_infos.append( entry_info )
                # If depth is exhausted, simply append itself.
                else:
                    entry_info.entry_type = EntryType.Dir
                    entry_info.size = self.get_dir_size( entry )
                    entry_infos.append( entry_info )

            else:
                tkmessagebox.showerror( "Error", entry_info.path + " is neither file nor directory? Aborted." )
                return

        return entry_infos

    def get_entry_infos_sorted_lexically( self ):

        return sorted( self.current_scan_result.entry_infos, key = lambda item: item.path.casefold() )

    def get_entry_infos_sorted_by_size( self ):

        return sorted( self.current_scan_result.entry_infos, key = lambda item: item.size )

    def get_dir_size( self, dir_path ):

        """ Calculate a directory's size.

        This is expensive.
        """

        dir_size = 0

        for sub_dir_path, sub_dir_names, file_names in os.walk( dir_path ):

            for fileName in file_names:

                file_path = os.path.join( sub_dir_path, fileName )

                if not os.path.islink( file_path ):
                    dir_size += os.path.getsize( file_path )

        return dir_size

    def set_current_scan_result( self, root_path, depth, entry_infos ):

        self.current_scan_result.root_path = root_path
        self.current_scan_result.depth = depth
        self.current_scan_result.entry_infos = entry_infos

    def report_unknown_json( self ):

        tkmessagebox.showerror( "Error", "Although the file you opened is of JSON format, it's not saved from this "
                                         "program." )


main_window_widget = tk.Tk()
main_window_widget.title( "Folder Size Monitor" )
main_window = MainWindow( main_window_widget )

main_window_widget.mainloop()
