from typing import NamedTuple, List


class NodeTypeTuple(NamedTuple):
    """
    A named tuple of node types.
    """
    sourceType: str
    """The type of the first/source node."""

    targetType: str
    """The type of the second/target node."""

class EdgeTypeMapping(NamedTuple):
    """
    A mapping class of a tuple of node types to an edge type.
    """
    nodeTypes: NodeTypeTuple
    """A named tuple of node types."""

    edgeType: str
    """The type of the edge the node tuple maps to."""

class HetPaths(dict):
    """
    An extended dictionary that maps a tuple of of node types to an edge type.
    """
    def __init__(self, paths: List[EdgeTypeMapping] = []) -> None:
        """
        Maps a list of EdgeTypeMappings to a dictionary. The dicitonary contains NodeTypeTuples as keys and edge types as values.
        
        Parameters
        ----------
            paths : List[EdgeTypeMapping]
                The list of EdgeTypeMappings that should be mapped into a dictionary.
        """
        pathDict = {}
        for path in paths:
            self[path[0]] = path[1]

        super(HetPaths, self).__init__(pathDict)
