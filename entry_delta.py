from entry_interface import IEntry


class EntryDeltaType:

    Unset = 0
    NoDiff = 1
    SizeDiff = 2
    NewEntry = 3
    Deleted = 4


class EntryDelta( IEntry ):

    """ How much has the size of an entry at a certain path changed"""

    def __init__( self, path, delta, delta_type ):

        self.path = path
        self.delta = delta
        self.delta_type = delta_type

    def get_path( self ):

        return self.path

    def get_size( self ):

        return self.delta
