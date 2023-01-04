from hetpy.utils.utils import generateNodeId



class Node:
    """
    TODO: Add docstrings
    """

    id: str
    type: str

    def __init__(self, type) -> None:
        self.id = generateNodeId()
        self.type = type