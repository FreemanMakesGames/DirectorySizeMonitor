from entry_interface import IEntry


class EntryInfoType:

    Unset = 0
    File = 1
    Dir = 2


class EntryInfo( IEntry ):

    """ An "entry" is either a file or a directory.

    :var path: Full path name
    :var entry_type: An EntryType enum which can be either File or Dir.
    :var sub_entry_infos: If the entry is a dir, this will be an array of its sub-elements. Otherwise, it's empty.
    """

    def __init__( self, path, entry_type, size, sub_entry_infos ):

        super().__init__( path, size, sub_entry_infos )

        self.entry_type = entry_type
