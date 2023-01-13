from typing import List


class MetaPath:
    """
    A semantic path on the heterogeneous information network. 
    """
    path: List[str]
    """A list of edge types that compose the meta path."""
    description: str
    """A short, optional description."""
    abbreviation: str
    """The abbreviation of the meta path. Functions as a identifier."""

    length: int
    """The length of the meta path."""

    def __init__(self, path: List[str], description: str = "", abbreviation: str = ""):
        """
        Maps parameters and attributes on object creation.

        Parameters
        ----------
            path : List[str]
                A list of edge types that compose the meta path.
            description : str
                A short, optional description.
            abbreviation : str
                The abbreviation of the meta path. Functions as a identifier.
        """
        self.path = path
        self.description = description
        self.abbreviation = abbreviation

        self.length = len(path)