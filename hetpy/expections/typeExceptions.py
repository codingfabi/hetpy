class TypeException(Exception):
    """
    TODO: Add docstrings
    """
    def __init__(self, details):            
        # Call the base class constructor with the parameters it needs
        message = f"A type error occured: {details}"
        super().__init__(message)