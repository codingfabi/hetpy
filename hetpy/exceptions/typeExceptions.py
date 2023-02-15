class TypeException(Exception):
    """
    An exception to throw when the type of some object is undefined or invalid.
    """
    def __init__(self, details):            
        # Call the base class constructor with the parameters it needs
        message = f"A type error occured: {details}"
        super().__init__(message)