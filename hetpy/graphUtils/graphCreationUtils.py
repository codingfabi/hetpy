from hetpy.models import Node, Edge, HetGraph

import pandas as pd
from ast import literal_eval

def fromCSV(filepath: str,type_column: str, connection_column: str, consider_edge_directions = False,  index_column: str = "index", node_attribute_column_map: dict = {}) -> HetGraph:
    """
    Returns a heterogeneous graph object mapped from a csv file. Consideres every row to be a node.
    Attributes: 
    -------------------
    filepath : str
        The path to the csv file.
    type_column : str
        The column in the csv file that specifies the type.
    connection_column : str
        The column that specifies to which nodes other nodes connects
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

    hetGraph = HetGraph(nodes, edges)

    return hetGraph

     
