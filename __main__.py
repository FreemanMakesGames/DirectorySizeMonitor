# Copyright 2020 FreemanMakesGames https://www.freemanmakesgames.pro

# This file is part of DirectorySizeMonitor.
# 
# DirectorySizeMonitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# DirectorySizeMonitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with DirectorySizeMonitor. If not, see <https://www.gnu.org/licenses/>.


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
                                                 command = lambda selected: self.redisplay_all() )
        self.display_depth_menu.config( state = tk.DISABLED )
        self.display_depth_menu.grid( row = 1, column = 7 )

        # Display

        display_frame = tk.Frame( master_frame )
        display_frame.grid( row = 1, column = 0 )

        # Display of root path of current scan
        self.scanned_root = ""
        self.scanned_root_label_title = "Root of current scan: "
        self.scanned_root_label = tk.Label( display_frame, text = self.scanned_root_label_title )
        self.scanned_root_label.grid( row = 0, column = 0, sticky = tk.W )

        ## Entry infos display
        entry_infos_display_label = tk.Label( display_frame, text = "Scan Result" )
        entry_infos_display_label.grid( row = 1, column = 0, sticky = tk.W )
        entry_infos_treeview = ttk.Treeview( display_frame )
        # self.root_tree_view.config( show = ["headings"] )  # Hide the tree.
        entry_infos_treeview.config( columns = ("content", "size") )
        entry_infos_treeview.column( "#0", width = 100 )
        entry_infos_treeview.column( "content", width = 600 )
        entry_infos_treeview.column( "size", width = 200 )
        entry_infos_treeview.heading( "content", text = "Content" )
        entry_infos_treeview.heading( "size", text = "Size" )
        entry_infos_treeview.grid( row = 2, column = 0 )
        ### Scrollbar
        entry_infos_display_scrollbar = ttk.Scrollbar( display_frame, orient = "vertical",
                                                       command = entry_infos_treeview.yview )
        entry_infos_treeview.config( yscrollcommand = entry_infos_display_scrollbar.set )
        entry_infos_display_scrollbar.grid( row = 2, column = 1, sticky = tk.NS )
        self.entry_infos_display = EntryInfosDisplay( entry_infos_treeview )

        ## Delta tree view
        delta_treeview_label = tk.Label( display_frame, text = "Comparison" )
        delta_treeview_label.grid( row = 3, column = 0, sticky = tk.W )
        entry_deltas_treeview = ttk.Treeview( display_frame )
        # entry_deltas_treeview.config( show = [ "headings" ] )  # Hide the tree.
        entry_deltas_treeview.config( columns = ( "entry", "delta" ) )
        entry_deltas_treeview.column( "#0", width = 100 )
        entry_deltas_treeview.column( "entry", width = 600 )
        entry_deltas_treeview.column( "delta", width = 200 )
        entry_deltas_treeview.heading( "entry", text = "Entry" )
        entry_deltas_treeview.heading( "delta", text = "Delta" )
        entry_deltas_treeview.grid( row = 4, column = 0 )
        ### Scrollbar
        entry_deltas_display_scrollbar = ttk.Scrollbar( display_frame, orient = "vertical",
                                                        command = entry_deltas_treeview.yview )
        entry_deltas_treeview.config( yscrollcommand = entry_deltas_display_scrollbar.set )
        entry_deltas_display_scrollbar.grid( row = 4, column = 1, sticky = tk.NS )
        self.entry_deltas_display = EntryDeltasDisplay( entry_deltas_treeview )

        ## Errors tree view
        errors_treeview_label = tk.Label( display_frame, text = "These files or directories couldn't be accessed:" )
        errors_treeview_label.grid( row = 5, column = 0, sticky = tk.W )
        self.errors_treeview = ttk.Treeview( display_frame )
        self.errors_treeview.config( show = [ "headings" ] )  # Hide the tree.
        self.errors_treeview.config( columns = ( "entry", "error" ) )
        self.errors_treeview.column( "entry", width = 600 )
        self.errors_treeview.column( "error", width = 300 )
        self.errors_treeview.heading( "entry", text = "Entry" )
        self.errors_treeview.heading( "error", text = "Error" )
        self.errors_treeview.grid( row = 6, column = 0 )
        ### Scrollbar
        errors_treeview_scrollbar = ttk.Scrollbar( display_frame, orient = "vertical",
                                                   command = self.errors_treeview.yview )
        self.errors_treeview.config( yscrollcommand = errors_treeview_scrollbar.set )
        errors_treeview_scrollbar.grid( row = 6, column = 1, sticky = tk.NS )

        # Status label
        self.status_label = tk.Label( display_frame )
        self.status_label.grid( row = 7, column = 0, sticky = tk.W )

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

        # Clear errors treeview first, because errors are inserted on the go during the scan.
        # Not doing so will result in conflicting entries in the treeview.
        self.errors_treeview.delete( *self.errors_treeview.get_children() )

        self.scanned_root = target_dir_path

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

        # Display scanning status before the slow scanning, i.e. get_dir_info.
        # TODO: This doesn't work. Probably because displaying and scanning happen in the same frame?
        self.status_label.config( text = "Scanning is in progress, please wait..." )

        target_entry_infos = self.get_dir_info( self.scanned_root, 1 )

        self.set_current_scan_result( self.scanned_root, self.scan_depth, target_entry_infos )

        # Display.

        self.status_label.config( text = "" )

        self.current_entry_deltas.clear()

        self.redisplay_all()

        self.scanned_root_label.config( text = self.scanned_root_label_title + self.scanned_root + '/' )

    def on_sort_button_clicked( self, entries_sorting_function ):

        if self.current_scan_result.root_path == "":
            tkmessagebox.showerror( "Error", "You haven't scanned any directory yet." )
            return

        if self.current_entries_sorting_function == entries_sorting_function:
            return

        self.current_entries_sorting_function = entries_sorting_function

        self.redisplay_all()

    def on_unit_selected( self, selected ):

        self.unit.divisor = 1024 ** self.unit_options.index( selected )
        self.unit.postfix = self.unit_option.get()

        self.redisplay_all()

    def on_hierarchy_display_selected( self ):

        self.redisplay_all()

        self.display_depth_menu.config( state = tk.DISABLED )

    def on_depth_display_selected( self ):

        self.redisplay_all()

        self.display_depth_menu.config( state = tk.NORMAL )

    def get_what_to_display( self, entries ):

        to_display = entries

        if self.hierarchy_or_depth.get() == 2:
            to_display = EntryUtils.get_flat_entries( to_display, self.display_depth.get() )

        to_display = self.current_entries_sorting_function( to_display )

        return to_display

    def display_entry_infos( self, entry_infos ):

        self.displayed_entry_infos = self.get_what_to_display( entry_infos )

        self.entry_infos_display.display( self.displayed_entry_infos, self.unit, self.scanned_root )

    def display_entry_deltas( self, entry_deltas ):

        self.displayed_entry_deltas = self.get_what_to_display( entry_deltas )

        self.entry_deltas_display.display( self.displayed_entry_deltas, self.unit, self.scanned_root )

    def redisplay_all( self ):

        self.display_entry_infos( self.current_scan_result.entry_infos )
        self.display_entry_deltas( self.current_entry_deltas )

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
                tkmessagebox.showerror( "Error", "The result you loaded isn't describing the same directory of what's "
                                                 "currently displayed." )
                return

        try:
            loaded_depth = loaded_scan_result[ "depth" ]
        except KeyError:
            self.report_unknown_json()
            return
        else:
            if loaded_depth != self.current_scan_result.depth:
                tkmessagebox.showerror( "Error", "The result you loaded is describing the same directory of "
                                                 "what's currently displayed, but the depth isn't the same. "
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

        :param target_dir_path: A full path name of current directory.
        :return entryNamesAndSizes: A list of pairs of entry name and size, automatically sorted lexically.
        """

        if target_dir_path == "C:/$Recycle.Bin":
            self.log_error( target_dir_path, "Scanning recycle bin is currently not supported." )
            return []

        # On Windows, target_dir_path will have / at the end if it's the entire drive like C:/
        # But no / at the end if it's anything below.
        if target_dir_path[ -1 : ] != '/':
            target_dir_path += '/'

        try:

            entry_infos = []

            for entry in os.scandir( target_dir_path ):

                # Init entry info.
                entry_path = target_dir_path + entry.name
                entry_info = EntryInfo( entry_path, EntryType.Unset, 0, [] )

                if entry.is_file():

                    entry_info.entry_type = EntryType.File

                    try:
                        entry_info.size = os.path.getsize( entry )
                    except OSError as e:
                        self.log_error( entry_info.path, e )

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

        # Catching exception from os.scandir
        except PermissionError as e:
            self.log_error( target_dir_path, e )
            return []

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

        entries = sorted( entries, key = lambda item: item.size, reverse = True )

        for entry in entries:

            entry.sub_entries = self.sort_entries_by_size( entry.sub_entries )

        return entries

    def get_dir_size( self, dir_path ):

        """ Calculate a directory's size.

        This should only be called to get the size of a dir at max depth.
        This is expensive.
        """

        dir_size = 0

        for sub_dir_path, sub_dir_names, file_names in os.walk( dir_path ):

            # file_names is an exhaustive list of all files under dir_path.
            for file_name in file_names:

                # Before formatting, On Windows, sub_dir_path part has /, file_name has \
                # On Unix, it's all /
                file_path = self.format_path( os.path.join( sub_dir_path, file_name ) )

                if not os.path.islink( file_path ):
                    try:
                        dir_size += os.path.getsize( file_path )
                    except OSError as e:
                        self.log_error( file_path, e )

        return dir_size

    def format_path( self, raw_path ):

        # On non-Windows system, it shouldn't need any formatting.
        if platform.system() != "Windows":
            return raw_path

        result = raw_path
        result = result.replace( "/", "\\" )
        # A prefix \\?\ for path length over 260 characters
        result = "\\\\?\\" + result

        return result

    def unformat_path( self, formatted_path ):

        # On non-Windows system, there shouldn't be any formatting.
        if platform.system() != "Windows":
            return formatted_path

        result = formatted_path
        result = result.replace( "\\\\?\\", "" )
        result = result.replace( "\\", "/" )

        return result

    def set_current_scan_result( self, root_path, depth, entry_infos ):

        self.current_scan_result.root_path = root_path
        self.current_scan_result.depth = depth
        self.current_scan_result.entry_infos = entry_infos

    def report_unknown_json( self ):

        tkmessagebox.showerror( "Error", "Although the file you opened is of JSON format, it's not saved from this "
                                         "program." )

    # This method won't be needed if entry_display is refactored.
    def log_error( self, path, error ):
        raw_path = self.unformat_path( path )
        self.errors_treeview.insert( "", tk.END, raw_path )
        self.errors_treeview.set( raw_path, "entry", raw_path )
        self.errors_treeview.set( raw_path, "error", error )


main_window_widget = tk.Tk()
main_window_widget.title( "Directory Size Monitor" )
main_window_widget.resizable( 0, 0 )
main_window = MainWindow( main_window_widget )

main_window_widget.mainloop()
