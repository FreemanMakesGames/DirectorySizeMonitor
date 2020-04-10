class EntryUtils:

    @staticmethod
    def get_flat_entries( entries, target_depth ):

        return EntryUtils.__get_flat_entries( entries, target_depth, 1 )

    @staticmethod
    def __get_flat_entries( entries, target_depth, operating_depth ):

        if operating_depth == target_depth:

            return entries.copy()

        result = []

        for entry in entries:

            if len( entry.sub_entries ) >= 1:

                result += EntryUtils.__get_flat_entries( entry.sub_entries, target_depth, operating_depth + 1 )

            else:

                result.append( entry )

        return result
