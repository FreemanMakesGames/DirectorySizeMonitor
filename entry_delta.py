from entry_interface import IEntry


class EntryDeltaType:

    Unset = 0
    NoDiff = 1
    SizeDiff = 2
    NewEntry = 3
    Deleted = 4


class EntryDelta( IEntry ):

    """ How much has the size of an entry at a certain path changed"""

    def __init__( self, path, entry_type, delta, delta_type, sub_entries ):

        super().__init__( path, entry_type, delta, sub_entries )

        self.delta_type = delta_type
