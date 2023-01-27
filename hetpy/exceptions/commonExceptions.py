class AlreadyDefinedException(Exception):
    """
    An exception to throw when some property is already defined.
    """
    def __init__(self, details):            
        # Call the base class constructor with the parameters it needs
        message = f"ERROR! The attribute you are trying to define is already defined: {details}"
        super().__init__(message)

class NotDefinedException(Exception):
    """
    An exception to throw when some property is not defined. 
    """
    def __init__(self, details):            
        # Call the base class constructor with the parameters it needs
        message = f"ERROR! The attribute you are trying to access is not defined: {details}"
        super().__init__(message)

class GraphDefinitionException(Exception):
    """
    An exception to throw on common, arbitrary cases.
    """
    def __init__(self, details):
        # Call the base class constructor with the parameters it needs.
        message =f"ERROR! There was a common error in your graph definition: {details}"