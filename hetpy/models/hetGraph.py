from typing import List
from copy import deepcopy


from .hetPaths import EdgeTypeMapping, HetPaths
from .node import Node
from .edge import Edge
from .metaPath import MetaPath

# exceptions
from hetpy.exceptions.typeExceptions import TypeException
from hetpy.exceptions.commonExceptions import AlreadyDefinedException, NotDefinedException

import igraph as ig
import json


class HetGraph:
    """
    An heterogeneous graph with multiple node and edge types.
    """

    nodes: List[Node]
    """The set of nodes that make up the network."""

    edges: List[Edge]
    """The set of edges that connect the nodes in the network."""

    node_types: List[str]
    """A set of all node types that exist in the graph."""

    edge_types: List[str]
    """A set of all edge types that exist in the graph."""

    graph: ig.Graph
    """The graph instance itself."""

    paths: HetPaths
    """A list of paths that exist in the graph. Maps a tuple of node types to an edge type."""

    meta_paths: List[MetaPath]
    """A list of meta paths that exist in the graph."""


    __nodeIdStore: dict
    __graphNodeStore: dict

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
        flag = True
        for edge in self.edges:
            edge_type = edge.type
            defined_type = self.paths[edge.nodes[0].type, edge.nodes[1].type]
            if edge_type is not defined_type:
                flag = False
                raise TypeException(f"Some defined edge types do not match the defined paths: {edge_type} | {defined_type}! Abborting graph creation.")
                break
        return flag

    def __assertNodeExistence(self, node: Node) -> False:
        """
        Asserts if a given node exists on the graph.

        Parameters:
        ------------
            node : Node
                The node for which the function shall check if it is defined on the graph.
        """
        if node.id not in [node.id for node in self.nodes]:
            return False
        else:
            return True

    
    def __setTypes(self) -> None:
        """
        A setter function that updates node types and edge types after a node or an edge has been added.
        """
        self.node_types = set([node.type for node in self.nodes])
        self.edge_types = set([edge.type for edge in self.edges])

    def _performTypeAssertions(self) -> None:
        """
        A wrapper function that performs all type assertions during graph creation.
        """
        return self.__assertEdgeTypes()


    def __init__(self, nodes: List[Node], edges: List[Edge], path_list: HetPaths = {}, meta_paths: List[MetaPath] = []) -> None:
        """
        Maps parameters and attributes during object creation. Also creates a igraph.Graph instance from defined nodes and edges.

        Parameters
        ----------
            nodes : List[Node]
                List of nodes of the graph.
            edges : List[Edge]
                List of edges of the graph.
            path_list : HetPaths
                A dictionary of simple path definitions.
            meta_paths : List[MetaPath]
                A list of semantic meta path definitions on the graph.
        """
        # initialize instance variables
        self.__nodeIdStore = {}
        self.__graphNodeStore = {}

        self.nodes = deepcopy(nodes)
        self.edges = deepcopy(edges)

        self.paths = deepcopy(path_list)
        self.meta_paths = deepcopy(meta_paths)

        # infer edge types if some are not defined
        undefined_edge_types = [edge.type == '' for edge in self.edges]
        if any(undefined_edge_types) and len(path_list.keys()) > 0:
            print("Some edge types are undefined. Infering types from paths...")
            self.__inferEdgeTypes()
        

        if len(path_list.keys()) > 0:
            # perform assertions
            if not self._performTypeAssertions():
                return None
        
        self.__setTypes()
        
        
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

    def _mapIGraphVertexToNode(self, vertex: ig.Vertex):
        return self.nodes[[node.id for node in self.nodes].index(self.__graphNodeStore[vertex.index])]

    def _mapEdgeToIGraphEdge(self, edge: Edge):
        """
        Maps an edge to the corresponding igraph edge.
        """
        for e in self.graph.es:
            if self.__graphNodeStore[e.source] == edge.nodes[0].id and self.__graphNodeStore[e.target] == edge.nodes[1].id and e["Type"] == edge.type:
                return e

    def get_meta_paths(self) -> dict:
        """
        Function that returns the meta paths defined on the HetGraph as a dictionary

        Returns
        ------------
            metapath_dict : dict
                The meta paths defined on the HetGraph in a dictionary.
                Uses the abbreviation as key and the edge type sequence as values.
        """
        graph_dict = {}
        for metapath in self.meta_paths:
            graph_dict[metapath.abbreviation] = metapath.path
        return graph_dict

    # crud functions

    def add_path(self, path: EdgeTypeMapping) -> None:
        """
        Adds a path definition to graph.
        
        Parameters:
        ------------
            path : EdgeTypeMapping
                The path definition that is supposed to be added. Consists of a node type tuple and an edge type definition.

        Raises:
        -----------
            AlreadyDefinedException: Raised when there is already a path definition for the node types.
        """
        if path[0] in self.paths.keys():
            raise AlreadyDefinedException(f"The graph already contains a path definition for the node types {path[0]}")
        self.paths[path[0]] = path[1]

    def remove_path(self, path: EdgeTypeMapping) -> None:
        """
        Removes a path definitino from the network schema.
        
        Parameters:
            path : EdgeTypeMapping
                The path definition that is supposed to be removed. Consists of a node type tuple and an edge type definition.

        Raises:
            NotDefinedException: Raised when there is no path for the specified node types that can be removed.

            AlreadyDefinedException: Raised when the edge type that is defined for the path to be removed does not match the path definition in the paramters.
        """
        try:
            path_definition = self.paths[path[0]]
            if path_definition == path[1]:
                del self.paths[path[0]]
            else:
                raise AlreadyDefinedException(f"The graph contains a different path definition for the nodes {path[0]}, namely: {path_definition}")
        except KeyError as e:
            raise NotDefinedException(f"There is no path definition for the nodes {path[0]}")


    def add_meta_path(self, metapath: MetaPath) -> None: 
        """
        Function that adds a meta path to the already existing heterogeneous graph.

        Parameters:
        --------------
            metapath : MetPath
                The meta path that is supposed to be added to the graph.
        """
        if metapath.abbreviation not in self.get_meta_paths().keys():
            self.meta_paths.append(metapath)
        else:
            raise AlreadyDefinedException(f"A metapath with the abbreviaton {metapath.abbreviation}")

    def remove_meta_path(self, metapath_abbreviation: str) -> None: 
        """
        Removes the specified metapath from the graph definition. 
        
        Parameters:
        -----------------
            metapath_abbreviation : str
                The abbreviation by which the meta path that is supposed to be removed is defined.
        """
        if metapath_abbreviation in self.get_meta_paths().keys():
            remove_index = [metapath.abbreviation for metapath in self.meta_paths].index(metapath_abbreviation)
            del self.meta_paths[remove_index]
        else:
            raise NotDefinedException(f"Metapath {metapath_abbreviation}")

    def find_edge(self, source: Node, target: Node):
        """
        Finds an edge between two nodes in the graph. If there is no edge, returns none.
        
        Parameters:
        -----------
            source : hetpy.Node
                The source node of the particular edge.
            target : hetpy.Node
                The target node of the particular edge.
        """
        source_target_tuples = [(edge.source.id, edge.target.id) for edge in self.edges]
        try:
            index = source_target_tuples.index((source.id, target.id))
            return self.edges[index]
        except ValueError:
            return None

    def add_edge(self, edge: Edge) -> None:
        """
        Adds the specified edge from the graph definition.

        Parameters:
        -------------
            edge : Edge
                The edge that is supposed to be added.
        """
        for node in edge.nodes:
            if not self.__assertNodeExistence(node):
                raise NotDefinedException(f"One of the nodes you are trying to connect does not exist in the graph.")
        self.edges.append(edge)
        if edge.type == '' and len(self.paths.keys()) > 0:
            print('Edge does not have a specified type. Infering from path definitions.')
            self.__inferEdgeTypes()
        self.__setTypes()
        igraph_node_pair = (self._mapNodeToIGraphVertex(edge.nodes[0]),self._mapNodeToIGraphVertex(edge.nodes[1]))
        self.graph.add_edge(*igraph_node_pair)

    def delete_edge(self, edge: Edge) -> None:
        """
        Removes the specified edge from the graph.

        Parameters:
        ----------
            edge : Edge
                The edge that is supposed to be removed.
        """
        try:
            self.edges.remove(edge)
            self.graph.delete_edges(self._mapEdgeToIGraphEdge(edge))
            self.__setTypes()
        except ValueError:
            raise NotDefinedException(f"The edge you are trying to remove does not exist on the graph.")

    def add_node(self, node: Node) -> None:
        """
        Adds the specified node to the graph.

        Parameters:
        -----------
            node : Node
                The node which is supposed to be added.
        """
        self.nodes.append(node)
        self.__setTypes()
        node.attributes["Type"] = node.type
        new_igraph_vertex = self.graph.add_vertex(**node.attributes)
        self.__nodeIdStore[node.id] = new_igraph_vertex.index
        self.__graphNodeStore[new_igraph_vertex.index] = node.id

    def delete_node(self, node: Node) -> None:
        """
        Deletes a node from the graph.

        Parameters:
        -----------
            node : Node
                The node that is supposed to be removed.
        """
        if self.__assertNodeExistence(node):
            # remove all edges that feature the node first.
            edges_to_remove = [edge for edge in self.edges if edge.nodes[0].id == node.id or edge.nodes[1].id == node.id]
            for edge in edges_to_remove:
                self.delete_edge(edge)
            self.nodes.remove(node)
            igraph_vertex = self._mapNodeToIGraphVertex(node)
            self.graph.delete_vertices(igraph_vertex.index)
            del self.__nodeIdStore[node.id]
            del self.__graphNodeStore[igraph_vertex.index]
            self.__setTypes()
        else:
            raise NotDefinedException(f"The node with id {node.id} your are trying to remove is not defined on the graph.")

    # graph metric functions

    def get_node_type_dist(self, pdf=False) -> dict:
        """
        Calculates the distribution of node types on the graph.

        Parameters:
        -----------
            pdf : boolean
                Specifies whether to return the distribution as absolute values or as a probability density function.
        """
        distribution = {}
        for type in self.node_types:
            distribution[type] = 0
        for node in self.nodes:
            distribution[node.type] += 1
        if pdf is True:
            distribution = {k: v / len(self.nodes) for k, v in distribution.items()}
        
        return distribution

    def get_edge_type_dist(self, pdf=False) -> dict:
        """
        Calculates the distribution of edge types on the graph.

        Parameters:
        -----------
            pdf : boolean
                Specifies whether to return the distribution as absolute values or as a probability density function.
        """
        distribution = {}
        for type in self.edge_types:
            distribution[type] = 0
        for edge in self.edges:
            distribution[edge.type] += 1
        if pdf is True:
            distribution = {k: v / len(self.edges) for k, v in distribution.items()}
        return distribution


    # utility functions

    def get_nodes_of_type(self, type : str) -> List[Node]:
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
        if type in self.node_types:
            selected_nodes = [node for node in self.nodes if node.type == type]
            return selected_nodes
        else:
            raise NotDefinedException(f"Nodetype {type} does not exist in the graph")

    def get_edges_of_type(self, type : str) -> List[Edge]:
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
        if type in self.edge_types:
            selected_edges = [edge for edge in self.edges if edge.type == type]
        else:
            raise NotDefinedException(f"Edgetype {type} does not exist in the graph")
        return selected_edges


    # util function for graph file storage
    def export_to_json(self, filepath: str):
        """
        Exports the graph to a json file to share or expose.

        Parameters:
        --------------
            filepath : str
                The filepath where the resulting json data shall be stored.
        """ 
        edges_json = []
        for edge in self.edges:
            edge_dict = {e: getattr(edge, e) for e in dir(edge) if not e.startswith('__') and e != "nodes"}
            edge_dict["source"] = edge.source.id
            edge_dict["target"] = edge.target.id
            edges_json.append(edge_dict)

        nodes_json = []
        for node in self.nodes:
            node_dict = {n: getattr(node, n) for n in dir(node) if not n.startswith('__')}
            nodes_json.append(node_dict)

        path_definitions = []
        for nodes, path in self.paths.items():
            path_dict = {
                "node_types": nodes,
                "edge_type": path
            }
            path_definitions.append(path_dict)

        meta_path_definitions = []
        for meta_path in self.meta_paths:
            meta_path_dict = {
                'path': meta_path.path,
                'description': meta_path.description,
                'abbreviation': meta_path.abbreviation
            }
            meta_path_definitions.append(meta_path_dict)

        dump_data = {
            "nodes": nodes_json,
            "edges": edges_json,
            "path_definitions": path_definitions,
            "meta_path_definitions": meta_path_definitions
        }

        with open(filepath, "w") as f:
            json.dump(dump_data, f)

    # util functions for plotting

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

    def print_network_schema(self, axis = None) -> None:
        """
        Prints the network schema to the specified axis. The network schema itself is a graph instance. If no axis is provided, the function prints the specified paths on the graph to the terminal

        Parameters:
        -------------
            axis : matplotlib.pyplot.axis
                The axis on which the schema shall be printed. If no axis is provided, the functions prints the specified paths on the graph to the terminal.
        """
        schema_graph_nodes = list(set(list(sum([t for t in self.paths], ())))) # hacky, find other solution
        schema_graph = ig.Graph(directed=True)
        schema_graph.add_vertices(len(schema_graph_nodes))
        for index, v in enumerate(schema_graph.vs):
            v["Name"] = schema_graph_nodes[index]
        
        edges = []
        edge_types = []
        for path, edgetype in self.paths.items():
            source_node = schema_graph.vs.select(Name_eq=path[0])[0].index
            target_node = schema_graph.vs.select(Name_eq=path[1])[0].index
            edges.append((source_node, target_node))
            edge_types.append(edgetype)
        schema_graph.add_edges(edges)
        schema_graph.es["Name"] = edge_types

        layout = schema_graph.layout_fruchterman_reingold()

        if axis is None:
            for edge in schema_graph.es:
                source_node = schema_graph.vs[edge.source]
                target_node = schema_graph.vs[edge.target]
                print(f'{source_node["Name"]} ---{edge["Name"]}---> {target_node["Name"]}')
        else:
            ig.plot(
                schema_graph,
                autocurve=True,
                vertex_color = 'white',
                vertex_size=0.4,
                vertex_label= schema_graph.vs["Name"],
                edge_label=schema_graph.es["Name"],
                layout=layout,
                edge_align_label=True,
                vertex_label_size=8,
                target=axis    
            )

