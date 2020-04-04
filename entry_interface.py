class IEntry:

    def __init__( self, path, size, sub_entries ):

        self.path = path
        self.size = size
        self.sub_entries = sub_entries

    def get_flat_sub_entries( self, required_depth ):

        return self.__get_flat_sub_entries( self.sub_entries, required_depth, 1 )

    def __get_flat_sub_entries( self, sub_entries, required_depth, operating_depth ):

        """ Flatten given list of ( sub ) entries.

        The result list will have references to the entry infos from the original list,
        But no entry info from the original list will actually change.
        """

        result = []

        if operating_depth == required_depth:

            return sub_entries

        for sub_entry in sub_entries:

            if len( sub_entry.sub_entries ) >= 1:

                result += self.__get_flat_sub_entries( sub_entry.sub_entries, required_depth, operating_depth + 1 )

            else:

                result.append( sub_entry )

        return result
