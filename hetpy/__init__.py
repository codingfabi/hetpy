r'''
# HetPy?

HetPy is a python module that provides simplified handling of heterogeneous information networks by wrapping and utilizing popule python package iGraph.

# How to install HetPy?

HetPy is currently in Alpha version and can be install via [PyPi's test repository](https://test.pypi.org).

```python
pip install -i https://test.pypi.org/simple/ hetpy==0.1.1b0
```

You can then use the provided modules, classes and functions for your network science project.

# Introduction

'''



__version__ = '0.1.1b'
__author__ = 'Fabian Kneissl'
__credits__ = 'Database Systems Research Group | Heidelberg University'

from .models.node import Node
from .models.edge import Edge
from .models.hetGraph import HetGraph
from .models.hetPaths import HetPaths, NodeTypeTuple, EdgeTypeMapping
from .models.metaPath import MetaPath


from .graphUtils.graphCreationUtils import fromCSV