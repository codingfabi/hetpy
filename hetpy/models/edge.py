from typing import Union
from .node import Node

class Edge:
    """
    TODO: Add docstrings
    """


    nodes: Union[Node, Node]
    directed: bool
    type: str

    def __init__(self, source: Node, target: Node, directed: bool, type: str) -> None:
        self.nodes = (source, target)
        self.directed = directed
        self.type = type