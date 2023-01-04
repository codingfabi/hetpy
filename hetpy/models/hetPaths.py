from typing import NamedTuple, TypedDict, List


class NodeTypeTuple(NamedTuple):
    """
    TODO: Add Docstrings    
    """
    sourceType: str
    targetType: str

class EdgeTypeMapping(NamedTuple):
    """
    TODO: Add docstrings
    """
    nodeTypes: NodeTypeTuple
    edgeType: str

class HetPaths(dict):
    """
    TODO: Add docstrings
    """
    def __init__(self, paths: List[EdgeTypeMapping] = []) -> None:
        """
        TODO: Add docstrings
        """
        pathDict = {}
        for path in paths:
            self[path[0]] = path[1]

        super(HetPaths, self).__init__(pathDict)
