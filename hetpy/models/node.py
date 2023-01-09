from ..utils.utils import generateNodeId



class Node:
    """
    TODO: Add docstrings
    """

    id: str
    type: str

    attributes: dict

    def __init__(self, type: str, attributes: dict = {}) -> None:
        self.id = generateNodeId()
        self.type = type

        self.attributes = attributes