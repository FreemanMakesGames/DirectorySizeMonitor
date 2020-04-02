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

    def get_flat_sub_entry_infos( self, required_depth ):

        return self.__get_flat_sub_entry_infos( self.sub_entry_infos, required_depth, 1 )

    def __get_flat_sub_entry_infos( self, sub_entry_infos, required_depth, operating_depth ):

        """ The result list will have references to the entry infos from the original list,
        But no entry info from the original list will actually change."""

        result = []

        if operating_depth == required_depth:

            return sub_entry_infos

        for sub_entry_info in sub_entry_infos:

            if len( sub_entry_info.sub_entry_infos ) >= 1:

                result += self.__get_flat_sub_entry_infos( sub_entry_info.sub_entry_infos,
                                                           required_depth, operating_depth + 1 )

            else:

                result.append( sub_entry_info )

        return result


class DeltaType:

    Unset = 0
    NoDiff = 1
    SizeDiff = 2
    NewEntry = 3
    Deleted = 4


class EntryDelta:

    """ How much has the size of an entry at a certain path changed"""

    def __init__( self, path, delta, delta_type ):
        self.path = path
        self.delta = delta
        self.delta_type = delta_type
