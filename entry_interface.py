from enum import IntEnum


class EntryType( IntEnum ):

    Unset = 0
    File = 1
    Dir = 2


class IEntry:

    """ An "entry" is either a file or a directory.

    :var path: Full path name
    :var entry_type: An EntryType enum which can be either File or Dir.
    :var size: An entry's size, but for EntryDelta subclass, it's the delta of size..
    :var sub_entry_infos: If the entry is a dir, this will be an array of its sub-elements. Otherwise, it's empty.
    """

    def __init__( self, path, entry_type, size, sub_entries ):

        self.path = path
        self.entry_type = entry_type
        self.size = size
        self.sub_entries = sub_entries
