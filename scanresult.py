class ScanResult:

    """ Scan result

    :var entry_infos: An array of every entry scanned. This isn't necessarily just the root's sub-entries.
                      If the depth is more than 1, this excludes root's sub-entries, and includes
                      the sub-entries below that.
    """

    def __init__( self, root_path, depth, entry_infos ):
        self.root_path = root_path
        self.depth = depth
        self.entry_infos = entry_infos
