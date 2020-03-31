class EntryType:
    Unset = 0
    File = 1
    Dir = 2


class DeltaType:
    Unset = 0
    NoDiff = 1
    SizeDiff = 2
    NewEntry = 3
    Deleted = 4

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

    def __init__( self, path, delta, delta_type ):
        self.path = path
        self.delta = delta
        self.delta_type = delta_type
