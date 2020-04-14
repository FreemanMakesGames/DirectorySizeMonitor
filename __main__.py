from entry_info import *
from entry_delta import *
from entry_interface import *
from scan_result import ScanResult
from entry_infos_display import EntryInfosDisplay
from entry_deltas_display import EntryDeltasDisplay
from entry_utils import *
from unit import Unit

import os
import platform
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import json


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

        self.sort_lexically_or_by_size = tk.IntVar()
        self.sort_lexically_or_by_size.set( 1 )
        self.sort_lexically_radio_button = tk.Radiobutton( input_frame, text = "Sort Lexically",
                                                      variable = self.sort_lexically_or_by_size,
                                                      value = 1, command = lambda:
                                                      self.on_sort_button_clicked( self.sort_entries_lexically ) )
        self.sort_lexically_radio_button.grid( row = 0, column = 1 )

        self.sort_by_size_radio_button = tk.Radiobutton( input_frame, text = "Sort By Size",
                                                    variable = self.sort_lexically_or_by_size,
                                                    value = 2, command = lambda:
                                                    self.on_sort_button_clicked( self.sort_entries_by_size ) )
        self.sort_by_size_radio_button.grid( row = 0, column = 2 )

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
        self.unit_option.set( self.unit_options[ 0 ] )
        self.unit = Unit( self.unit_divisor, self.unit_option.get() )
        self.unit_options_menu = tk.OptionMenu( input_frame, self.unit_option, *self.unit_options,
                                                command = lambda selected: self.on_unit_selected( selected ) )
        self.unit_options_menu.grid( row = 1, column = 1 )

        ## Depth input
        tk.Label( input_frame, text = "Scan Depth" ).grid( row = 1, column = 2 )
        self.scan_depth_entry_box = tk.Entry( input_frame )
        self.scan_depth_entry_box.grid( row = 1, column = 3 )
        self.scan_depth = 1
        self.scan_depth_entry_box.insert( 0, self.scan_depth )

        ## Hierarchical vs. depth display
        self.hierarchy_or_depth = tk.IntVar()
        self.hierarchy_or_depth.set( 1 )
        self.hierarchy_display_radio_button = tk.Radiobutton( input_frame, text = "Display by hierarchy",
                                                              variable = self.hierarchy_or_depth, value = 1,
                                                              command = self.on_hierarchy_display_selected )
        self.depth_display_radio_button = tk.Radiobutton( input_frame, text = "Display by depth",
                                                          variable = self.hierarchy_or_depth, value = 2,
                                                          command = self.on_depth_display_selected )
        self.hierarchy_display_radio_button.grid( row = 1, column = 4 )
        self.depth_display_radio_button.grid( row = 1, column = 5 )

        ## Display-by-depth options
        tk.Label( input_frame, text = "Display Depth" ).grid( row = 1, column = 6 )
        self.display_depth_options = [ 1, 2, 3, 4, 5 ]
        self.display_depth = tk.IntVar()
        self.display_depth.set( 1 )
        self.display_depth_menu = tk.OptionMenu( input_frame, self.display_depth, *self.display_depth_options,
                                                 command = self.on_display_depth_selected )
        self.display_depth_menu.config( state = tk.DISABLED )
        self.display_depth_menu.grid( row = 1, column = 7 )

        # Display

        display_frame = tk.Frame( master_frame )
        display_frame.grid( row = 1, column = 0 )

        ## Entry infos display
        entry_infos_display_label = tk.Label( display_frame, text = "Scan Result" )
        entry_infos_display_label.grid( row = 0, column = 0, sticky = tk.W )
        entry_infos_treeview = ttk.Treeview( display_frame )
        # self.root_tree_view.config( show = ["headings"] )  # Hide the tree.
        entry_infos_treeview.config( columns = ("content", "size") )
        entry_infos_treeview.column( "#0", width = 100 )
        entry_infos_treeview.column( "content", width = 600 )
        entry_infos_treeview.column( "size", width = 200 )
        entry_infos_treeview.heading( "content", text = "Content" )
        entry_infos_treeview.heading( "size", text = "Size" )
        entry_infos_treeview.grid( row = 1, column = 0 )
        ### Scrollbar
        entry_infos_display_scrollbar = ttk.Scrollbar( display_frame, orient = "vertical",
                                                       command = entry_infos_treeview.yview )
        entry_infos_treeview.config( yscrollcommand = entry_infos_display_scrollbar.set )
        entry_infos_display_scrollbar.grid( row = 1, column = 1, sticky = tk.NS )
        self.entry_infos_display = EntryInfosDisplay( entry_infos_treeview )

        ## Delta tree view
        delta_tree_view_label = tk.Label( display_frame, text = "Comparison" )
        delta_tree_view_label.grid( row = 2, column = 0, sticky = tk.W )
        entry_deltas_treeview = ttk.Treeview( display_frame )
        # entry_deltas_treeview.config( show = [ "headings" ] )  # Hide the tree.
        entry_deltas_treeview.config( columns = ( "entry", "delta" ) )
        entry_deltas_treeview.column( "#0", width = 100 )
        entry_deltas_treeview.column( "entry", width = 600 )
        entry_deltas_treeview.column( "delta", width = 200 )
        entry_deltas_treeview.heading( "entry", text = "Entry" )
        entry_deltas_treeview.heading( "delta", text = "Delta" )
        entry_deltas_treeview.grid( row = 3, column = 0 )
        ### Scrollbar
        entry_deltas_display_scrollbar = ttk.Scrollbar( display_frame, orient = "vertical",
                                                        command = entry_deltas_treeview.yview )
        entry_deltas_treeview.config( yscrollcommand = entry_deltas_display_scrollbar.set )
        entry_deltas_display_scrollbar.grid( row = 3, column = 1, sticky = tk.NS )
        self.entry_deltas_display = EntryDeltasDisplay( entry_deltas_treeview )

        """ Backend """

        self.current_scan_result = ScanResult( "", self.scan_depth, [] )
        self.current_entry_deltas = []

        self.displayed_entry_infos = []
        self.displayed_entry_deltas = []

        self.current_entries_sorting_function = self.sort_entries_lexically

        self.MAXDEPTH = 5

    def on_scan_button_clicked( self ):

        """This function should be the only place that carries out scanning."""

        target_dir_path = tkfiledialog.askdirectory()

        # If the dialog is closed with "Cancel", return.
        if target_dir_path == "":
            return

        # Get depth.
        input_depth_string = self.scan_depth_entry_box.get()
        if not input_depth_string:  # Empty input
            self.set_scan_depth( 1 )
        else:  # Non-empty input
            try:  # Integer input
                self.scan_depth = int( input_depth_string )
                if self.scan_depth < 1 or self.scan_depth > self.MAXDEPTH:
                    tkmessagebox.showerror( "Error", "Depth can only be between 1 to 5. Resetting to 1." )
                    self.set_scan_depth( 1 )
            except ValueError:  # Bad input
                tkmessagebox.showerror( "Error", "Scan depth isn't an integer. Depth is set to 1." )
                self.set_scan_depth( 1 )

        target_entry_infos = self.get_dir_info( target_dir_path, 1 )

        self.set_current_scan_result( target_dir_path, self.scan_depth, target_entry_infos )

        # Display.
        if self.hierarchy_or_depth.get() == 1:
            self.display_entries_by_hierarchy()
        else:
            self.display_entries_by_depth()

    def on_sort_button_clicked( self, entries_sorting_function ):

        if self.current_scan_result.root_path == "":
            tkmessagebox.showerror( "Error", "You haven't scanned any directory yet." )
            return

        self.current_entries_sorting_function = entries_sorting_function

        self.display_entry_infos( self.displayed_entry_infos )

        if len( self.displayed_entry_deltas ) > 0:
            self.display_entry_deltas( self.displayed_entry_deltas )

    def on_unit_selected( self, selected ):

        self.unit.divisor = 1024 ** self.unit_options.index( selected )
        self.unit.postfix = self.unit_option.get()

        self.display_entry_infos( self.displayed_entry_infos )
        self.display_entry_deltas( self.displayed_entry_deltas )

    def on_display_depth_selected( self, value ):

        self.display_entries_by_depth()

    def on_hierarchy_display_selected( self ):

        # Can't pass self.displayed_entry_infos here, because flattened sub entry infos can't be
        # Put back to their hierarchy.
        self.display_entries_by_hierarchy()

        self.display_depth_menu.config( state = tk.DISABLED )

    def display_entries_by_hierarchy( self ):

        self.display_entry_infos( self.current_scan_result.entry_infos )
        self.display_entry_deltas( self.current_entry_deltas )

    def on_depth_display_selected( self ):

        self.display_entries_by_depth()

        self.display_depth_menu.config( state = tk.NORMAL )

    def display_entries_by_depth( self ):

        self.display_entry_infos( EntryUtils.get_flat_entries( self.current_scan_result.entry_infos,
                                                               self.display_depth.get() ) )

        self.display_entry_deltas( EntryUtils.get_flat_entries( self.current_entry_deltas,
                                                                self.display_depth.get() ) )

    def display_entry_infos( self, entry_infos ):

        self.displayed_entry_infos = self.current_entries_sorting_function( entry_infos )

        self.entry_infos_display.display( self.displayed_entry_infos, self.unit )

    def display_entry_deltas( self, entry_deltas ):

        self.displayed_entry_deltas = self.current_entries_sorting_function( entry_deltas )

        self.entry_deltas_display.display( self.displayed_entry_deltas, self.unit )

    def clear_all_displays( self ):

        self.entry_infos_display.clear()
        self.entry_deltas_display.clear()

    def clear_tree_view( self, tree_view ):

        tree_view.delete( *tree_view.get_children() )

    def set_scan_depth( self, target_depth ):

        self.scan_depth = target_depth
        self.scan_depth_entry_box.delete( 0, tk.END )
        self.scan_depth_entry_box.insert( 0, target_depth )

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
        self.current_entry_deltas = self.get_entry_deltas( self.current_scan_result.entry_infos, loaded_entry_infos )

        # Display.
        self.display_entry_deltas( self.current_entry_deltas )

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

                entry_info.entry_type = EntryType.Dir

                # If depth isn't exhausted, recursively get and append all sub-entries,
                # And get this dir's size simply by summing up sub entries' sizes.
                if operating_depth < self.scan_depth:
                    for sub_entry_info in self.get_dir_info( entry_info.path, operating_depth + 1 ):
                        entry_info.sub_entries.append( sub_entry_info )
                        entry_info.size += sub_entry_info.size
                # If depth is exhausted, just get this dir's size the slow way, which involves os module calls.
                else:
                    entry_info.size = self.get_dir_size( entry )

                entry_infos.append( entry_info )

            else:
                tkmessagebox.showerror( "Error", entry_info.path + " is neither file nor directory? Aborted." )
                return

        return entry_infos

    def get_entry_deltas( self, current_entry_infos, loaded_entry_infos ):

        result = []

        for current_entry_info in current_entry_infos:

            entry_matches = False

            for loaded_entry_info in loaded_entry_infos:  # loaded_entry_infos is a dict read from JSON.

                if current_entry_info.path == loaded_entry_info[ "path" ]:

                    entry_matches = True

                    if current_entry_info.size != loaded_entry_info[ "size" ]:

                        entry_delta_to_append = EntryDelta\
                            ( current_entry_info.path, current_entry_info.entry_type,
                              current_entry_info.size - loaded_entry_info[ "size" ], EntryDeltaType.SizeDiff, [] )

                        entry_delta_to_append.sub_entries = self.get_entry_deltas( current_entry_info.sub_entries,
                                                                                   loaded_entry_info[ "sub_entries" ] )

                        result.append( entry_delta_to_append )

                    break

            # The entry is newly created.
            if not entry_matches:

                entry_delta_to_append = EntryDelta( current_entry_info.path, current_entry_info.entry_type,
                                                    current_entry_info.size, EntryDeltaType.NewEntry, [] )

                entry_delta_to_append.sub_entries = self.get_entry_deltas( current_entry_info.sub_entries, [] )

                result.append( entry_delta_to_append )

        for loaded_entry_info in loaded_entry_infos:

            entry_deleted = True

            for current_entry_info in current_entry_infos:

                if loaded_entry_info[ "path" ] == current_entry_info.path:

                    entry_deleted = False

                    break

            if entry_deleted:

                entry_delta_to_append = EntryDelta\
                    ( loaded_entry_info[ "path" ], EntryType( loaded_entry_info[ "entry_type" ] ),
                      -loaded_entry_info[ "size" ], EntryDeltaType.Deleted, [] )

                entry_delta_to_append.sub_entries = self.get_entry_deltas( [], loaded_entry_info[ "sub_entries" ] )

                result.append( entry_delta_to_append )

        return result

    def sort_entries_lexically( self, entries ):

        entries = sorted( entries, key = lambda item: item.path.casefold() )

        for entry in entries:

            entry.sub_entries = self.sort_entries_lexically( entry.sub_entries )

        return entries

    def sort_entries_by_size( self, entries ):

        entries = sorted( entries, key = lambda item: item.size )

        for entry in entries:

            entry.sub_entries = self.sort_entries_by_size( entry.sub_entries )

        return entries

    def get_dir_size( self, dir_path ):

        """ Calculate a directory's size.

        This is expensive.
        """

        dir_size = 0

        for sub_dir_path, sub_dir_names, file_names in os.walk( dir_path ):

            for fileName in file_names:

                file_path = os.path.join( sub_dir_path, fileName )

                # File path formatting for Windows
                if platform.system() == "Windows":
                    file_path = file_path.replace( "/", "\\" )
                    file_path = "\\\\?\\" + file_path  # A prefix \\?\ for path length over 260 characters

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
