from entry_interface import IEntry


class EntryInfo( IEntry ):

    def __init__( self, path, entry_type, size, sub_entry_infos ):

        super().__init__( path, entry_type, size, sub_entry_infos )
