from typing import List
from hetpy.exceptions.commonExceptions import NotDefinedException

from hetpy.models import Node, Edge, HetGraph, HetPaths, MetaPath

import pandas as pd
import igraph as ig
from ast import literal_eval
import json

def fromCSV(filepath: str,type_column: str, connection_column: str, consider_edge_directions = False,  index_column: str = "index", node_attribute_column_map: dict = {}, graphArgs: dict = {} ) -> HetGraph:
    """
    Returns a heterogeneous graph object mapped from a csv file. Consideres every row to be a node.

    Parameters
    -----------
        filepath : str
            The path to the csv file.
        type_column : str
            The column in the csv file that specifies the type.
        connection_column : str
            The column that specifies to which nodes other nodes connects

    Returns
    ----------
        hetGraph : hetpy.models.hetGraph.HetGraph
            The created heterogenous graph.
    """
    data = pd.read_csv(filepath)
    nodes = []
    edges = []

    index_to_nodeid_map = {}

    # preliminary create all nodes. Needed to create correct edge objects.
    for row in data.to_dict("records"):
        node_attributes = {}
        for key, value in node_attribute_column_map.items():
            node_attributes[key] = row[value]
        node = Node(row[type_column], node_attributes)
        index_to_nodeid_map[str(row[index_column])] = node.id
        nodes.append(node)
    
    for row in data.to_dict("records"):
        for entry in literal_eval(row[connection_column]):
            source = nodes[[node.id for node in nodes].index(index_to_nodeid_map[str(row[index_column])])]
            target = nodes[[node.id for node in nodes].index(index_to_nodeid_map[str(entry)])]
            edge = Edge(source, target, directed=consider_edge_directions)
            edges.append(edge)

    hetGraph = HetGraph(nodes, edges, **graphArgs)

    return hetGraph

def from_iGraph(graph: ig.Graph, type_attribute: str = "Type", path_list: HetPaths = {}, meta_paths: List[MetaPath] = [] ) -> HetGraph:
    """
    Transforms a common igraph object into a heterogeneous graph. The index of the original graph vertices and edges get appended
    to the new object types as attributes.

    Parameters
    ----------
        graph : igraph.Graph
            The igraph object that is supposed to be converted.
        type_attribute : str
            The type attribute in the igraph object that specifies node and edge types.
        path_list : HetPaths
            A dictionary of simple path definitions.
        meta_paths : List[MetaPath]
            A list of semantic meta path definitions on the graph.

    Returns
    --------
        het_graph : HetGraph
            The transformed heterogeneous graph object.

    Raises
    ---------
        NotDefinedException
            Raised when the specified type_attribute is undefined in the nodes or edges of the iGraph object.
    """
    nodes = []
    edges = []
    for vertex in graph.vs:
        attribute_names = vertex.attribute_names()
        if type_attribute not in attribute_names:
           raise NotDefinedException(f"type_attribute {type_attribute} in iGraph node attributes")
        values = [vertex[name] for name in attribute_names]

        attributes = zip(attribute_names, values)
        attribute_dict = {tuple[0] : tuple[1] for tuple in attributes}
        attribute_dict["iGraphIndex"] = vertex.index
        nodes.append(Node(vertex[type_attribute], attributes=attribute_dict))
    
    nodes_by_original_index = [node.attributes["iGraphIndex"] for node in nodes]
    for edge in graph.es:
        attribute_names = edge.attribute_names()
        edge_type = ''
        if type_attribute in attribute_names:
            edge_type = edge[type_attribute]
        values = [edge[name] for name in attribute_names]

        attributes = zip(attribute_names, values)
        attribute_dict = {tuple[0] : tuple[1] for tuple in attributes}
        attribute_dict["iGraphIndex"] = edge.index
        source_node = nodes[nodes_by_original_index.index(edge.source)]
        target_node = nodes[nodes_by_original_index.index(edge.target)]
        edge = Edge(source_node, target_node, directed=graph.is_directed(), type=edge_type, attributes=attribute_dict)
        edges.append(edge)
    
    het_graph = HetGraph(nodes, edges, path_list, meta_paths)
    return het_graph


def from_json(filepath: str) -> HetGraph:
    """
    Creates a graph from existing json structure. Ideally use this with files created via the to_json() function of HetGraph objects.

    Parameters:
    ------------
        filepath: str
            The path to the .json file that is supposed to be loaded.
    """
    data = {}
    with open(filepath) as file:
        data = json.load(file)

    nodes = []
    for defined_node in data["nodes"]:
        node_object = Node(type=defined_node["type"], attributes=defined_node["attributes"])
        if "id" in defined_node.keys():
            node_object.id  = defined_node["id"] #overwrite id to preserve defined one
        nodes.append(node_object)

    edges = []
    for defined_edge in data["edges"]:
        source_node = nodes[[node.id for node in nodes].index(defined_edge["source"])]
        target_node = nodes[[node.id for node in nodes].index(defined_edge["target"])]
        edge = Edge(source = source_node, target = target_node, directed = defined_edge["directed"], type = defined_edge["type"], attributes = defined_edge["attributes"])
        edges.append(edge)
    
    node_type_mappings = []
    for path_definition in data["path_definitions"]:
        node_tuple = (path_definition["node_types"][0],path_definition["node_types"][1])
        node_type_mappings.append((node_tuple, path_definition["edge_type"]))
    
    paths = HetPaths(node_type_mappings)

    meta_paths = []
    for meta_path_definition in data["meta_path_definitions"]:
        meta_paths.append(MetaPath(path=meta_path_definition["path"], description=meta_path_definition["description"], abbreviation=meta_path_definition["abbreviation"]))

    return HetGraph(nodes=nodes, edges=edges, path_list = paths, meta_paths=meta_paths)



