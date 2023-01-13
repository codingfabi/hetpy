import uuid

def generateNodeId():
    """
    Generates a random uuid using uuid package.
    """
    return str(uuid.uuid4())