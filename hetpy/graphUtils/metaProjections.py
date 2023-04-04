import igraph as ig
import itertools
from collections import Counter

from typing import List


from hetpy.enums.projectionEnums import CombineEdgeTypes

from hetpy.models import MetaPath, HetGraph, HetPaths
from hetpy.models.edge import Edge

from hetpy.exceptions.commonExceptions import GraphDefinitionException, NotDefinedException

# implement own pairwise function to please python 3.9
def __pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def __check_path_for_metapath(path: List, path_definitions: HetPaths, metapath: MetaPath) -> bool:
    """
    Performs a type by type string comparison of a list of nodes quals the list of node types that a meta path constructs.
    
    Properties:
    --------------
        path : list
            The sequence of vertices that needs to be checked.
        path_definitions: hetpy.HetPaths
            The list of node type to edge mappings that are defined on the graph.
        metapath : hetpy.MetaPath
            The metapath to which the actual path instance shall be compared
    """
    actual_edge_types = []
    for t in __pairwise(path):
        try:
            defined_edge_type = path_definitions[(t[0]["Type"],t[1]["Type"])]
            actual_edge_types.append(defined_edge_type)
        except KeyError:
            print("The edges of your graph contain an undefined path type. This can especially happen in undirected HetGraph objects. Please check your path definitions, you probably did not define the inverse of some path. Skipping this possible path...")
            continue
    return actual_edge_types == metapath.path

def __combine_multi_edges(edges: List[Edge], combine_edges: CombineEdgeTypes) -> List[Edge]:
    """
    Identifies and combines edges that connect the same nodes into a single one. Combination strategies are specified by CombineEdgeTypes enum. 
    Paramters:
    -----------
        edges : List[Edge]
            The edges of the projection that are supposed to be checked for multi-edges.
        combine_edges : CombineEdgeTypes
            The strategy for combining multi-edges.
    
    Returns:
    ----------
        combined_edges : List[Edge]
            A new list of edges with the combined edges.
    """
    node_tuples = [(edge.source,edge.target) for edge in edges]
    counter = Counter(node_tuples)

    edge_type = edges[0].type # edges should all be of type metapath abbreviation. Therefor just use first element in edges to determine type.

    combined_edges = []
    for node_tuple, count in counter.items():
        edge = Edge(node_tuple[0],node_tuple[1], type=edge_type, directed=any([edge.directed for edge in edges]))
        attributes = {}
        if combine_edges is CombineEdgeTypes.SUM.value:
                attributes['Weight'] = count
        edge.attributes = attributes
        combined_edges.append(edge)
    return combined_edges


    
def create_meta_projection(graph: HetGraph, metapath: MetaPath, directed: bool = False, combine_edges: CombineEdgeTypes = CombineEdgeTypes.NONE ) -> HetGraph:
    """
    Creates a graph projection based on a provided metapath.
    Parameters:
    -------------
        graph : hetpy.HetGraph
            The graph for which the projection should be created
        metapath : hetpy.MetaPath
            A list of node types that make up the metapath that the projection is based on. Order matters.
        directed : bool
            Specifies whether the projection graph should be a directed graph or not.
    Returns:
    --------------
        projection : hetpy.HetGraph
    """

    if metapath.path not in [metapath.path for metapath in graph.meta_paths]:
        raise NotDefinedException(f"The metapath {metapath.abbreviation} you are trying to use as a projection is not defined on the graph you are trying to compress.")

    starting_type = ''
    ending_type = ''
    for key, object in graph.paths.items():
        if object == metapath.path[0]:
            starting_type = key[0]
        if object == metapath.path[-1]:
            ending_type = key[1]
    
    starting_nodes = graph.get_nodes_of_type(starting_type)
    ending_nodes = graph.get_nodes_of_type(ending_type)

    undirected_graph_copy = graph.graph.as_undirected()
    igraph_starting_nodes = [graph._mapNodeToIGraphVertex(node) for node in starting_nodes]
    igraph_ending_nodes = [graph._mapNodeToIGraphVertex(node) for node in ending_nodes]
    all_paths = {}
    for node in igraph_starting_nodes:
        paths_for_node = undirected_graph_copy.get_all_simple_paths(node, igraph_ending_nodes, cutoff=len(metapath.path))
        all_paths[str(node.index)] = paths_for_node
    
    projection_edges = []
    for _, paths_of_node in all_paths.items():
        for path in paths_of_node:
            path_nodes = [undirected_graph_copy.vs[index] for index in path]
            if len(path_nodes) == (len(metapath.path)+1) and __check_path_for_metapath(path_nodes, graph.paths, metapath):
                projection_edges.append((path[0],path[-1]))
            else:
                continue

    if len(projection_edges) == 0:
        raise NotDefinedException(f"There were no path instances of the specified meta path {metapath.abbreviation}.")
    
    projection_igraph_nodes = undirected_graph_copy.vs[list(set(itertools.chain.from_iterable(projection_edges)))]
    projection_nodes_map = {str(vertex.index) : graph._mapIGraphVertexToNode(vertex) for vertex in projection_igraph_nodes}
    new_projection_edges = [Edge(source=projection_nodes_map[str(t[0])], target=projection_nodes_map[str(t[1])], directed=directed, type=metapath.abbreviation) for t in projection_edges]

    if combine_edges is not CombineEdgeTypes.NONE.value:
        new_projection_edges = __combine_multi_edges(new_projection_edges, combine_edges)


    projection_path = ((starting_type, ending_type),metapath.abbreviation)
    projection_graph = HetGraph(nodes = list(projection_nodes_map.values()), edges = new_projection_edges, path_list = HetPaths([projection_path]))
    return projection_graph