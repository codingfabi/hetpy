from typing import List

from .hetPaths import HetPaths
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

    paths: HetPaths


    __nodeIdStore = {}
    __graphNodeStore = {}

    def __init__(self, nodes: List[Node], edges: List[Edge], pathList: HetPaths = {}) -> None:
        """
        TODO: Add docstrings
        """
        self.nodes = nodes
        self.edges = edges
        self.nodeTypes = set([node.type for node in nodes])
        self.edgeTypes = set([edge.type for edge in edges])

        self.paths = pathList
        
        # create igraph instance iteratively
        self.graph = ig.Graph()
        self.graph.add_vertices(len(nodes))
        for index, node in enumerate(nodes):
            self.__nodeIdStore[node.id] = index
            self.__graphNodeStore[index] = node.id
            self.graph.vs[index]["Type"] = node.type
        
        igraph_edges = [(self.__nodeIdStore[edge.nodes[0].id],self.__nodeIdStore[edge.nodes[1].id]) for edge in edges]
        igraph_edge_types = [edge.type for edge in edges]
        self.graph.add_edges(igraph_edges)
        self.graph.es["Type"]=igraph_edge_types


    def _mapNodeToIGraphVertex(self, node: Node):
        """
        TODO: Add docstrings
        """
        return self.graph.vs[self.__nodeIdStore[node.id]]

    def _mapEdgeToIGraphEdge(self, edge: Edge):
        """
        TODO: Add docstrings
        """
        for e in self.graph.es:
            if self.__graphNodeStore[e.source] == edge.nodes[0].id and self.__graphNodeStore[e.target] == edge.nodes[1].id and e["Type"] == edge.type:
                return e