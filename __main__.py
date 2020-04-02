from entryclasses import *
from scanresult import ScanResult
from entry_infos_display import EntryInfosDisplay
from unit import Unit

import os
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

        self.sort_lexically_button = tk.Button( input_frame, text = "Sort Lexically", command = lambda:
                                                self.on_sort_button_clicked( self.sort_entry_infos_lexically,
                                                                             self.sort_entry_deltas_lexically ) )
        self.sort_lexically_button.grid( row = 0, column = 1 )

        self.sort_by_size_button = tk.Button( input_frame, text = "Sort By Size", command = lambda:
                                              self.on_sort_button_clicked( self.sort_entry_infos_by_size,
                                                                           self.sort_entry_deltas_by_size ) )
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
        self.unit_option.set( self.unit_options[ 0 ] )
        self.unit = Unit( self.unit_divisor, self.unit_option.get() )
        self.unit_options_menu = tk.OptionMenu( input_frame, self.unit_option, *self.unit_options,
                                                command = lambda selected: self.on_unit_selected( selected ) )
        self.unit_options_menu.grid( row = 1, column = 1 )

        ## Depth input
        self.depth_label = tk.Label( input_frame, text = "Depth" )
        self.depth_label.grid( row = 1, column = 2 )
        self.depth_entry_box = tk.Entry( input_frame )
        self.depth_entry_box.grid( row = 1, column = 3 )
        self.depth = 1
        self.depth_entry_box.insert( 0, self.depth )

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

        # Display

        display_frame = tk.Frame( master_frame )
        display_frame.grid( row = 1, column = 0 )

        ## Entry infos display
        self.entry_infos_display_label = tk.Label( display_frame, text = "Scan Result" )
        self.entry_infos_display_label.grid( row = 0, column = 0, sticky = tk.W )
        entry_infos_display_treeview = ttk.Treeview( display_frame )
        # self.root_tree_view.config( show = ["headings"] )  # Hide the tree.
        entry_infos_display_treeview.config( columns = ("content", "size") )
        entry_infos_display_treeview.column( "#0", width = 100 )
        entry_infos_display_treeview.column( "content", width = 600 )
        entry_infos_display_treeview.column( "size", width = 200 )
        entry_infos_display_treeview.heading( "content", text = "Content" )
        entry_infos_display_treeview.heading( "size", text = "Size" )
        entry_infos_display_treeview.grid( row = 1, column = 0 )
        self.entry_infos_display = EntryInfosDisplay( entry_infos_display_treeview )

        ## Delta tree view
        self.delta_tree_view_label = tk.Label( display_frame, text = "Comparison" )
        self.delta_tree_view_label.grid( row = 2, column = 0, sticky = tk.W )
        self.delta_tree_view = ttk.Treeview( display_frame )
        self.delta_tree_view.config( show = [ "headings" ] )  # Hide the tree.
        self.delta_tree_view.config( columns = ( "entry", "delta" ) )
        self.delta_tree_view.column( "entry", width = 600 )
        self.delta_tree_view.column( "delta", width = 200 )
        self.delta_tree_view.heading( "entry", text = "Entry" )
        self.delta_tree_view.heading( "delta", text = "Delta" )
        self.delta_tree_view.grid( row = 3, column = 0 )

        """ Backend """

        self.current_scan_result = ScanResult( "", self.depth, [] )

        self.displayed_entry_infos = []

        self.current_entry_infos_sorting_function = self.sort_entry_infos_lexically

        self.current_entry_deltas = []

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

        # Display.
        if self.hierarchy_or_depth.get() == 1:
            self.display_entry_infos_by_hierarchy( self.current_scan_result.entry_infos )
        else:
            self.display_entry_infos_by_depth( self.current_scan_result.entry_infos )

    def on_sort_button_clicked( self, entry_infos_sorting_function, entry_deltas_sorting_function ):

        if self.current_scan_result.root_path == "":
            tkmessagebox.showerror( "Error", "You haven't scanned any directory yet." )
            return

        # Sort and display entry infos.
        self.display_entry_infos( self.displayed_entry_infos, entry_infos_sorting_function, self.unit )
        self.current_entry_infos_sorting_function = entry_infos_sorting_function

        # Sort and display entry deltas, if any.
        if len( self.current_entry_deltas ) > 0:
            self.current_entry_deltas = entry_deltas_sorting_function( self.current_entry_deltas )
            self.clear_tree_view( self.delta_tree_view )
            self.display_delta_tree_view()

    def on_unit_selected( self, selected ):

        self.unit.divisor = 1024 ** self.unit_options.index( selected )
        self.unit.postfix = self.unit_option.get()

        self.display_entry_infos( self.displayed_entry_infos, self.current_entry_infos_sorting_function, self.unit )

        self.display_delta_tree_view()

    def on_hierarchy_display_selected( self ):

        # Can't pass self.displayed_entry_infos here, because flattened sub entry infos can't be
        # Put back to their hierarchy.
        self.display_entry_infos_by_hierarchy( self.current_scan_result.entry_infos )

    def display_entry_infos_by_hierarchy( self, entry_infos ):

        self.display_entry_infos( entry_infos, self.current_entry_infos_sorting_function, self.unit )

    def on_depth_display_selected( self ):

        self.display_entry_infos_by_depth( self.current_scan_result.entry_infos )

    def display_entry_infos_by_depth( self, entry_infos ):

        entry_infos_to_display = []

        for entry_info in entry_infos:

            if len( entry_info.sub_entry_infos ) >= 1:

                entry_infos_to_display += entry_info.get_flat_sub_entry_infos( 5 )

            else:

                entry_infos_to_display.append( entry_info )

        self.display_entry_infos( entry_infos_to_display, self.current_entry_infos_sorting_function, self.unit )

    def display_entry_infos( self, entry_infos, sorting_function, unit ):

        self.entry_infos_display.display( entry_infos, sorting_function, self.unit )

        self.displayed_entry_infos = entry_infos

    def display_delta_tree_view( self ):

        for entry_delta in self.current_entry_deltas:

            self.delta_tree_view.insert( "", tk.END, entry_delta.path )
            self.delta_tree_view.set( entry_delta.path, "entry", entry_delta.path )
            self.delta_tree_view.set( entry_delta.path, "delta", str( entry_delta.delta / self.unit_divisor ) +
                                      self.unit_option.get() )

            # Assign tag based on delta type, for highlighting.
            if entry_delta.delta_type == DeltaType.NewEntry:
                self.delta_tree_view.item( entry_delta.path, tags = "new_entry" )
            elif entry_delta.delta_type == DeltaType.Deleted:
                self.delta_tree_view.item( entry_delta.path, tags = "deleted" )

        # Highlight rows based on their tag.
        self.delta_tree_view.tag_configure( "new_entry", background = "#81ed81" )  # Light green
        self.delta_tree_view.tag_configure( "deleted", background = "#ff9191" )  # Light red

    def clear_all_displays( self ):

        self.entry_infos_display.clear()
        self.clear_tree_view( self.delta_tree_view )

    def clear_tree_view( self, tree_view ):

        tree_view.delete( *tree_view.get_children() )

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
                                                         loaded_entry_info[ "size" ], DeltaType.SizeDiff ) )

                    break

            # The entry is newly created.
            if not entry_matches:

                entry_deltas.append( EntryDelta( entry_info.path, entry_info.size, DeltaType.NewEntry ) )

        for loaded_entry_info in loaded_entry_infos:

            entry_deleted = True

            for entry_info in self.current_scan_result.entry_infos:

                if loaded_entry_info[ "path" ] == entry_info.path:

                    entry_deleted = False

                    break

            if entry_deleted:

                entry_deltas.append( EntryDelta( loaded_entry_info[ "path" ], -loaded_entry_info[ "size" ],
                                                 DeltaType.Deleted ) )

        self.current_entry_deltas = entry_deltas

        # Display.
        self.clear_tree_view( self.delta_tree_view )
        self.display_delta_tree_view()

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
                entry_info.size = self.get_dir_size( entry )

                # If depth isn't exhausted, recursively get and append all sub-entries, but exclude itself.
                if operating_depth < self.depth:
                    for sub_entry_info in self.get_dir_info( entry_info.path, operating_depth + 1 ):
                        entry_info.sub_entry_infos.append( sub_entry_info )

                entry_infos.append( entry_info )

            else:
                tkmessagebox.showerror( "Error", entry_info.path + " is neither file nor directory? Aborted." )
                return

        return entry_infos

    def sort_entry_infos_lexically( self, entry_infos ):

        entry_infos = sorted( entry_infos, key = lambda item: item.path.casefold() )

        for entry_info in entry_infos:

            entry_info.sub_entry_infos = self.sort_entry_infos_lexically( entry_info.sub_entry_infos )

        return entry_infos

    def sort_entry_infos_by_size( self, entry_infos ):

        entry_infos = sorted( entry_infos, key = lambda item: item.size )

        for entry_info in entry_infos:

            entry_info.sub_entry_infos = self.sort_entry_infos_by_size( entry_info.sub_entry_infos )

        return entry_infos

    def sort_entry_deltas_lexically( self, entry_deltas ):

        return sorted( entry_deltas, key = lambda item: item.path.casefold() )

    def sort_entry_deltas_by_size( self, entry_deltas ):

        return sorted( entry_deltas, key = lambda item: item.delta )

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
