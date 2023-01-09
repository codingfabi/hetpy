from hetpy.models import Node, Edge, HetGraph

import pandas as pd

def fromCSV(filepath: str, type_column: str, connection_column: str, consider_edge_directions = False) -> HetGraph:
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
    data  = pd.read_csv(filepath)
    nodes = []
    edges = []

    index_to_nodeid_map = {}

    # preliminary create all nodes. Needed to create correct edge objects.
    for row in data.to_dict("records"):
        node = Node(row["type_column"])
        index_to_nodeid_map[row["index"]] = node.id
        nodes.append(node)
    
    for row in data.to_dict("records"):
        for entry in row[connection_column]:
            source = nodes[[node.id for node in nodes].index(index_to_nodeid_map[row["index"]])]
            target = index_to_nodeid_map[str(entry)]
            edge = Edge(source, target, directed=consider_edge_directions)
            edges.append(edge)

    hetGraph = HetGraph(nodes, edges)

    return hetGraph

     
