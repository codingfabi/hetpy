r'''

HetPy is a python module that provides simplified handling of heterogeneous information networks by wrapping and utilizing populare python package [iGraph](https://igraph.readthedocs.io/en/stable/).

# How to install HetPy?

HetPy is currently in Alpha version and can be install via [PyPi's test repository](https://test.pypi.org).

```python
pip install -i https://test.pypi.org/simple/ hetpy==0.2.0
```

You can then use the provided modules, classes and functions for your network science project.

# Introduction

.. include:: ../demo/hetPyDemo.md

'''



__version__ = '0.2.0b'
__author__ = 'Fabian Kneissl'
__credits__ = 'Database Systems Research Group | Heidelberg University'

# Classes
from .models.node import Node
from .models.edge import Edge
from .models.hetGraph import HetGraph
from .models.hetPaths import HetPaths, NodeTypeTuple, EdgeTypeMapping
from .models.metaPath import MetaPath

# Enums
from .enums.projectionEnums import CombineEdgeTypes

# Util Functions
from .graphUtils.graphCreationUtils import fromCSV, from_iGraph
from .graphUtils.metaProjections import create_meta_projection
