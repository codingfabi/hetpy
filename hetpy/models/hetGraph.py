from typing import List


from .hetPaths import HetPaths
from .node import Node
from .edge import Edge
from .metaPath import MetaPath

# exceptions
from hetpy.exceptions.typeExceptions import TypeException
from hetpy.exceptions.commonExceptions import AlreadyDefinedException, NotDefinedException

import igraph as ig


class HetGraph:
    """
    An heterogeneous graph with multiple node and edge types.
    """

    nodes: List[Node]
    """The set of nodes that make up the network."""

    edges: List[Edge]
    """The set of edges that connect the nodes in the network."""

    nodeTypes: List[str]
    """A set of all node types that exist in the graph."""

    edgeTypes: List[str]
    """A set of all edge types that exist in the graph."""

    graph: ig.Graph
    """The graph instance itself."""

    paths: HetPaths
    """A list of paths that exist in the graph. Maps a tuple of node types to an edge type."""

    metaPaths: List[MetaPath]
    """A list of meta paths that exist in the graph."""


    __nodeIdStore = {}
    __graphNodeStore = {}

    def __inferEdgeTypes(self) -> None:
        """
        Infers the types of untyped edges from the graphs path definitions.
        """
        for edge in self.edges:
                if edge.type == '':
                    edge.type = self.paths[(edge.nodes[0].type, edge.nodes[1].type)]
    
    def __assertEdgeTypes(self) -> None:
        """
        Asserts if all defined edge types match with the defined path definitions.
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
        Maps parameters and attributes during object creation. Also creates a igraph.Graph instance from defined nodes and edges.

        Parameters
        ----------
            nodes : List[Node]
                List of nodes of the graph.
            edges : List[Edge]
                List of edges of the graph.
            pathList : HetPaths
                A dictionary of simple path definitions.
            metaPaths : List[MetaPath]
                A list of semantic meta path definitions on the graph.
        """
        self.nodes = nodes
        self.edges = edges

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
        
        self.nodeTypes = set([node.type for node in nodes])
        self.edgeTypes = set([edge.type for edge in edges])
        
        
        # create igraph instance iteratively
        self.graph = ig.Graph(directed=any([edge.directed for edge in self.edges]))
        self.graph.add_vertices(len(nodes))
        for index, node in enumerate(nodes):
            self.__nodeIdStore[node.id] = index
            self.__graphNodeStore[index] = node.id
            self.graph.vs[index]["Type"] = node.type
            for key, value in node.attributes.items():
                self.graph.vs[index][key] = value
        
        igraph_edges = [(self.__nodeIdStore[edge.nodes[0].id],self.__nodeIdStore[edge.nodes[1].id]) for edge in self.edges]
        igraph_edge_types = [edge.type for edge in self.edges]
        self.graph.add_edges(igraph_edges)
        
        # add edge attributes to igraph edges
        self.graph.es["Type"] = igraph_edge_types
        for index, edge in enumerate(self.graph.es):
            for key, value in edges[index].attributes.items():
                edge[key] = value


    def _mapNodeToIGraphVertex(self, node: Node):
        """
        Maps a node object to the coresponding igraph vertex.
        """
        return self.graph.vs[self.__nodeIdStore[node.id]]

    def _mapEdgeToIGraphEdge(self, edge: Edge):
        """
        Maps an edge to the corresponding igraph edge.
        """
        for e in self.graph.es:
            if self.__graphNodeStore[e.source] == edge.nodes[0].id and self.__graphNodeStore[e.target] == edge.nodes[1].id and e["Type"] == edge.type:
                return e

    def getDefinedMetaPaths(self) -> dict:
        """
        Function that returns the meta paths defined on the HetGraph as a dictionary

        Returns
        ------------
            metapath_dict : dict
                The meta paths defined on the HetGraph in a dictionary.
                Uses the abbreviation as key and the edge type sequence as values.
        """
        graph_dict = {}
        for metapath in self.metaPaths:
            graph_dict[metapath.abbreviation] = metapath.path
        return graph_dict

    def addMetaPath(self, metapath: MetaPath) -> None: 
        """
        Function that adds a meta path to the already existing heterogeneous graph.

        Parameters:
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
        
        Parameters:
        -----------------
            metapath_abbreviation : str
                The abbreviation by which the meta path that is supposed to be removed is defined.
        """
        if metapath_abbreviation in self.getDefinedMetaPaths().keys():
            remove_index = [metapath.abbreviation for metapath in self.metaPaths].index(metapath_abbreviation)
            del self.metaPaths[remove_index]
        else:
            raise NotDefinedException(f"Metapath {metapath_abbreviation}")

    # utility functions

    def getNodesOfType(self, type : str) -> List[Node]:
        """
        Returns all nodes of the specified type in the graph. 
        Parameters:
        ------------------
            type : str
                The type of which nodes should be selected.

        Returns:
        ------------------
            selected_nodes : List[Nodes]
                The selected nodes of the specified type.
        """
        if type in self.nodeTypes:
            selected_nodes = [node for node in self.nodes if node.type == type]
            return selected_nodes
        else:
            raise NotDefinedException(f"Nodetype {type} does not exist in the graph")

    def getEdgesOfType(self, type : str) -> List[Edge]:
        """
        Returns all edges of the specified type in the graph. 

        Parameters:
        ------------------
            type : str
                The type of which edges should be selected.
        
        Returns:
        ------------------
            selected_edges : List[Edge]
                The selected edges of the specified type.
        """
        if type in self.edgeTypes:
            selected_edges = [edge for edge in self.edges if edge.type == type]
        else:
            raise NotDefinedException(f"Edgetype {type} does not exist in the graph")
        return selected_edges

    def plot(self, type_color_map: dict, layout = "random", axis = None, plot_args: dict = {}) -> None:
        """
        Plots the graph onto the specified matplotlib axis. Works as a wrapper for igraph.plot.

        Parameters:
        ----------------
            type_color_map : dict
                A dictionary that maps a node type to a color. 
            layout : string | igraph.layout
                The layout in which the graph shall be plotted. Defaults to random layout.
            axis : matplotlib.pyplot.axis
                The matplotlib axis on which the graph shall eb plotted.
            plot_args : dict
                A dicitonary of additional plotting arguments that get passed to the igraph.plot function.
        """

        vertex_colors = []
        if len(type_color_map.keys()) > 0:
            vertex_colors = [type_color_map[type] for type in self.graph.vs["Type"]]
        
        ig.plot(
            self.graph,
            layout=layout,
            vertex_color=vertex_colors,
            target=axis,
            **plot_args
        )

