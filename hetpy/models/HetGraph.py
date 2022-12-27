from typing import List
from .node import Node
from .edge import Edge

import igraph as ig


class HetGraph:
    """
    TODO: Add docstrings
    """

    nodes: List[Node]
    edges: List[Edge]

    nodeTypes: List[str]
    edgeTypes: List[str]

    graph: ig.Graph


    __nodeIdMap = {}

    def __init__(self, nodes: List[Node], edges: List[Edge]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.nodeType = set([node.type for node in nodes])
        self.edgeTypes: set([edge.type for edge in edges])
        
        self.graph = ig.Graph()
        self.graph.add_vertices(len(nodes))
        self.graph.add_edges([()])