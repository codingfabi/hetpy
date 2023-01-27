import igraph as ig
import itertools

from hetpy.models import MetaPath, HetGraph, HetPaths
from hetpy.models.edge import Edge


def __check_path_for_metapath(path: list, path_definitions: HetPaths, metapath: MetaPath) -> bool:
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
    for t in itertools.pairwise(path):
        defined_edge_type = path_definitions[(t[0]["Type"],t[1]["Type"])]
        actual_edge_types.append(defined_edge_type)

    return actual_edge_types == metapath.path
    
def create_meta_projection(graph: HetGraph, metapath: MetaPath, directed: bool = False) -> HetGraph:
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

    starting_type = ''
    ending_type = ''
    for key, object in graph.paths.items():
        if object == metapath.path[0]:
            starting_type = key[0]
        if object == metapath.path[-1]:
            ending_type = key[1]
    
    starting_nodes = graph.get_nodes_of_type(starting_type)
    ending_nodes = graph.get_nodes_of_type(ending_type)
    igraph_starting_nodes = [graph._mapNodeToIGraphVertex(node) for node in starting_nodes]
    igraph_ending_nodes = [graph._mapNodeToIGraphVertex(node) for node in ending_nodes]
    all_paths = {}
    for node in igraph_starting_nodes:
        paths_for_node = graph.graph.get_all_simple_paths(node, igraph_ending_nodes)
        all_paths[str(node.index)] = paths_for_node
    
    projection_edges = []
    for _, paths_of_node in all_paths.items():
        for path in paths_of_node:
            path_nodes = [graph.graph.vs[index] for index in path]
            if __check_path_for_metapath(path_nodes, graph.paths, metapath):
                projection_edges.append((path[0],path[-1]))
            else:
                continue
    
    projection_igraph_nodes = graph.graph.vs[list(set(itertools.chain.from_iterable(projection_edges)))]
    projection_nodes_map = {str(vertex.index) : graph._mapIGraphVertexToNode(vertex) for vertex in projection_igraph_nodes}
    new_projection_edges = [Edge(source=projection_nodes_map[str(t[0])], target=projection_nodes_map[str(t[1])], directed=directed, type=metapath.abbreviation) for t in projection_edges]
    projection_path = ((starting_type, ending_type),metapath.abbreviation)
    projection_graph = HetGraph(nodes = list(projection_nodes_map.values()), edges = new_projection_edges, path_list = HetPaths([projection_path]))
    return projection_graph