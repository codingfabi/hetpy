from .node import Node

class Edge:
    """
    Calss that represents an edge in a heterogeneous information network.
    """


    nodes: tuple[Node, Node]
    """An ordered tuple of nodes. First element is the source node and second element the target node."""
    directed: bool
    """Flag whether the edge should be considered as directed or undirected."""
    type: str
    """The type of the edge. Is not required."""

    attributes: dict
    """Dictionary of edge attributes with the attributes identifiers as keys."""

    def __init__(self, source: Node, target: Node, directed: bool, type: str = '', attributes: dict = {}) -> None:
        """
        Maps edge attributes on object construction.
        
        Parameters
        ----------
            source : Node
                The source node of the edge.
            target : Node
                The sink node of the edge.
            directed : bool
                A flag whetehr the edge should be considered as directed.
            type : str
                The type of the edge. Optional.
            attributes : dict
                A dictionary of edge attributes with the attribute identifiers as keys.
        """
        self.nodes = (source, target)
        self.directed = directed
        self.type = type

        self.attributes = attributes

    @property
    def source(self):
        return self.nodes[0]
    
    @property
    def target(self):
        return self.nodes[1]