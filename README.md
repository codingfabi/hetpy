# HetPy

HetPy is a strongly typed python library for handling heterogeneous information networks.                   


![Coverage](coverage.svg)


## How to install

HetPy is installable via pip: 

```python
pip install -i hetpy
```

The package is available for Python versions 3.7 - 3.10.

HetPy is and will always be free to use. If you use this package frequently for reasearch or business purposes, feel free to contribute to the project by giving feedback, raising issues or enhancing the documentation. If used for a publication, feel free to use the citation provided in the sidebar.

## Quick Start

HetPy provides various strongly typed classes for typesafe handling of heterogeneous information networks (HINs).
HINs in general are graphs with at least two node or two edge types. Node and edge types are a requirement for a HIN to exist. 
HetPy supports these type definitions by asserting and requiring these types. Further, it enables the user to define types of paths and meta paths on the graph.

To get started, import the main class HetGraph from the package and create one using a set of nodes and a set of edges. 

```python
from hetpy import HetGraph, Node, Edge


node = Node("MockType",{"Name": "node1"})
node_two = Node("MockType2",{"Name": "node2"})
node_three = Node("MockType3",{"Name": "node3"})

edge = Edge(source=node, target=node_two, directed=True, type="EdgeType")
edge_two = Edge(source=node, target=node_three, directed=True, type="EdgeType2")

graph = HetGraph([node, node_two, node_three], [edge, edge_two])
```

It is further possible to define path types as a mapping of node type tuple to an edge type. A list of paths can then be defiend on the graph object in order to assert object type definitions.

```
edge_type_mappings = [(("MockType","MockType2"),"EdgeType"), (("MockType2", "MockType3"),"EdgeType2")]
path_definitions = HetPaths(edge_type_mappings)
```
As an extention to this path concept, we allow definitions of meta paths that guide the semantics of the underlying domain. Meta paths are defined as a concatenation of edge types and hence, concatenation of paths. Meta path objects are consequently defined by a path sequence and an abbreviation that works as a unique identifier. Further, they containa describtion. Both, paths and meta paths can be added to the graph either during creation or in hindsight.

```python
exemplaryMetaPath = MetaPath(path=["EdgeType","EdgeType2"], description="A meta path do demonstrate meta path functionality.", abbreviation="mockMetaPath")

hinGraphWithPaths = HetGraph(nodes=[node, node_two, node_three], edges=[edge, edge_two] path_list=path_definitions, meta_paths=[exemplaryMetaPath])
```

By specifying these semantic boundaries, the information network becomes easier to interpret w.r.t. its domain. 

## Meta Projection

To compress the information a heterogeneous graph contains and focus on a particular node type relation, it is possible to create a projection of the graph on basis of a meta path. Following along the concept of bipartite projections in a bipartite graph, this is called a "meta projection".

A meta projection connects to two nodes if there exists a path that is an instance of the meta path that the projection is based on. Consequently, the meta projection shows the relation between the node types of the source and the sink of the meta path. 

For example, we can compress the information the previous defined graph by the meta path that we defined earlier. 

```python
projection = create_meta_projection(graph=hinGraphWithPaths, meta_path=exemplaryMetaPath)
```

This results in a projeciton graph where `node1` connects to `node3` because they are connected by an instance of the meta path `exemplaryMetaPath`.


For more information, demos and detailed documentation see the [API-Documentation](https://codingfabi.github.io/hetpy/hetpy.html).

