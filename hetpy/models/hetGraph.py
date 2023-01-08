from typing import List
from hetpy.expections.commonExceptions import AlreadyDefinedException, NotDefinedException

from hetpy.models.metaPath import MetaPath

from .hetPaths import HetPaths
from .node import Node
from .edge import Edge

# exceptions
from hetpy.expections.typeExceptions import TypeException

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
    metaPaths: List[MetaPath]


    __nodeIdStore = {}
    __graphNodeStore = {}

    def __inferEdgeTypes(self) -> None:
        """
        TODO: Add docstrings
        """
        for edge in self.edges:
                if edge.type == '':
                    edge.type = self.paths[(edge.nodes[0].type, edge.nodes[1].type)]
    
    def __assertEdgeTypes(self) -> None:
        """
        TODO: Add docstrings
        """
        for edge in self.edges:
            edge_type = edge.type
            defined_type = self.paths[edge.nodes[0].type, edge.nodes[1].type]
            if edge_type is not defined_type:
                raise TypeException(f"Some defined edge types do not match the defined paths: {edge_type} | {defined_type}! Abborting graph creation.")

    def _performTypeAssertions(self) -> None:
        """
        A wrapper function that performs all type assertions during graph creation.
        """
        self.__assertEdgeTypes()


    def __init__(self, nodes: List[Node], edges: List[Edge], pathList: HetPaths = {}, metaPaths: List[MetaPath] = []) -> None:
        """
        TODO: Add docstrings
        """
        self.nodes = nodes
        self.edges = edges
        self.nodeTypes = set([node.type for node in nodes])
        self.edgeTypes = set([edge.type for edge in edges])

        self.paths = pathList
        self.metaPaths = metaPaths

        # infer edge types if some are not defined
        undefined_edge_types = [edge.type == '' for edge in self.edges]
        if any(undefined_edge_types) and len(pathList.keys()) > 0:
            print("Some edge types are undefined. Infering types from paths...")
            self.__inferEdgeTypes()
        

        if len(pathList.keys()) > 0:
            # perform assertions
            self._performTypeAssertions()
        
        
        # create igraph instance iteratively
        self.graph = ig.Graph()
        self.graph.add_vertices(len(nodes))
        for index, node in enumerate(nodes):
            self.__nodeIdStore[node.id] = index
            self.__graphNodeStore[index] = node.id
            self.graph.vs[index]["Type"] = node.type
        
        igraph_edges = [(self.__nodeIdStore[edge.nodes[0].id],self.__nodeIdStore[edge.nodes[1].id]) for edge in self.edges]
        igraph_edge_types = [edge.type for edge in self.edges]
        self.graph.add_edges(igraph_edges)
        self.graph.es["Type"]=igraph_edge_types

        if any([edge.directed for edge in self.edges]):
            self.graph.to_directed()


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

    def getDefinedMetaPaths(self) -> dict:
        """
        Function that returns the meta paths defined on the HetGraph as a dictionary
        Returns:
        ------------
        metapath_dict : dit
            The meta paths defined on the HetGraph in a dictionary. Uses the abbreviation as key and the edge type sequence as values.
        """
        graph_dict = {}
        for metapath in self.metaPaths:
            graph_dict[metapath.abbreviation] = metapath.path
        return graph_dict

    def addMetaPath(self, metapath: MetaPath) -> None: 
        """
        Function that adds a meta path to the already existing heterogeneous graph. 
        Attributes:
        --------------
        metapath : MetPath
            The meta path that is supposed to be added to the graph.
        """
        if metapath.abbreviation not in self.getDefinedMetaPaths().keys():
            self.metaPaths.append(metapath)
        else:
            raise AlreadyDefinedException(f"A metapath with the abbreviaton {metapath.abbreviation}")

    def removeMetaPath(self, metapath_abbreviation: str) -> None: 
        """
        Removes the specified metapath from the graph definition. 
        Attributes:
        -----------------
        metapath_abbreviation : str
            The abbreviation by which the meta path that is supposed to be removed is defined.
        """
        if metapath_abbreviation in self.getDefinedMetaPaths().keys():
            remove_index = [metapath.abbreviation for metapath in self.metaPaths].index(metapath_abbreviation)
            del self.metaPaths[remove_index]
        else:
            raise NotDefinedException(f"Metapath {metapath_abbreviation}")