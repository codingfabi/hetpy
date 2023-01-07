from typing import List


class MetaPath:
    """
    TODO: Add docstrings
    """
    path: List[str]
    description: str
    abbreviation: list

    def __init__(self, path: List[str], description: str = "", abbreviation: str = ""):
        """
        TODO: Add docstring
        """
        self.path = path
        self.description = description
        self.abbreviation = abbreviation