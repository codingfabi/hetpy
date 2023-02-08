### Basic Graph Creation


```python
from hetpy import HetGraph, Node, Edge, HetPaths, MetaPath
from hetpy.graphUtils import create_meta_projection
import matplotlib.pyplot as plt
import igraph as ig
import pandas as pd
from copy import deepcopy
import itertools
```

#### Create a simple graph with two node types and one edge type

HetPy functions as a standard graph library which uses strongly typed node and edge objects. To create a basic, simple graph, we first create a standard set of two nodes and a single edge that connects those nodes.


```python
node = Node("MockType",{"Name": "node1"})
node_two = Node("MockType2",{"Name": "node2"})

edge = Edge(node, node_two, True, "EdgeType")
```

We can then easily create a heterogeneous graph $G=(V,E)$ defined by set of nodes $V$ and a set of edges $E$ 


```python
graph = HetGraph([node, node_two], [edge])
color_map = {
    "MockType": "yellow",
    "MockType2": "pink"
}
visual_style = {
    "vertex_label": [node.type for node in [node, node_two]],
    "vertex_label_size": 10
}
fig, ax = plt.subplots()
graph.plot(type_color_map=color_map, axis=ax, plot_args=visual_style)
```


    
![png](../demo/hetPyDemo_files/hetPyDemo_6_0.png)
    


While this graph is quite simple, we can also define edge types by specifying the node types they connect and add a list of these paths to the graph. These semantic paths then enable us to infer edge types while creating the graph. Furthermore, we can add attribtues to the nodes that are handeled just like normal attributes.


```python
# define paths
edge_type_mappings = [(("Player","Club"),"played_for"), (("Club", "Shirt"),"wears")]
paths = HetPaths(edge_type_mappings)
```


```python
# define nodes and edges
players = [Node("Player", {"Name": "Lionel Messi"}), Node("Player", {"Name": "Toni Kroos"}), Node("Player", {"Name": "Luis Figo"})]
clubs = [Node("Club", {"Name": "Real Madrid"}), Node("Club", {"Name": "FC Barcelona"})]
shirts = [Node("Shirt", {"shirt_color": "White"}), Node("Shirt", {"shirt_color": "Blue and Red"})]

nodes = list(itertools.chain(players, clubs, shirts))
edges = [
    Edge(players[0], clubs[1], False),
    Edge(players[1], clubs[0], False),
    Edge(players[2], clubs[1], False),
    Edge(players[2], clubs[0], False),
    Edge(clubs[0], shirts[0], False),
    Edge(clubs[1], shirts[1], False)
]


```

Then we can create a HetGraph out of the defined objects. You will notice that during creation, the graph constructor will report that some edges have a undefined type and that the type will be infered from the paths assigned to it. After creation, we can check if all edge types are correctly inferred.


```python
het_graph = HetGraph(nodes, edges, paths)
```

    Some edge types are undefined. Infering types from paths...


The HetGraph class asserts also automaticall asserts the defined edge types. If they do not match the specified paths, an error is raised during the object creation.


```python
# assign wrong type to edge
wrong_edges = deepcopy(edges)
wrong_edges[0].type = "wears"

HetGraph(nodes, wrong_edges, paths)
```


    ---------------------------------------------------------------------------

    TypeException                             Traceback (most recent call last)

    /Users/I542771/Documents/GitHub/hetpy/demo/hetPyDemo.ipynb Cell 20 in <cell line: 5>()
          <a href='vscode-notebook-cell:/Users/I542771/Documents/GitHub/hetpy/demo/hetPyDemo.ipynb#X25sZmlsZQ%3D%3D?line=1'>2</a> wrong_edges = deepcopy(edges)
          <a href='vscode-notebook-cell:/Users/I542771/Documents/GitHub/hetpy/demo/hetPyDemo.ipynb#X25sZmlsZQ%3D%3D?line=2'>3</a> wrong_edges[0].type = "wears"
    ----> <a href='vscode-notebook-cell:/Users/I542771/Documents/GitHub/hetpy/demo/hetPyDemo.ipynb#X25sZmlsZQ%3D%3D?line=4'>5</a> HetGraph(nodes, wrong_edges, paths)


    File /opt/homebrew/lib/python3.10/site-packages/hetpy/models/hetGraph.py:127, in HetGraph.__init__(self, nodes, edges, path_list, meta_paths)
        122     self.__inferEdgeTypes()
        125 if len(path_list.keys()) > 0:
        126     # perform assertions
    --> 127     self._performTypeAssertions()
        129 self.__setTypes()
        132 # create igraph instance iteratively


    File /opt/homebrew/lib/python3.10/site-packages/hetpy/models/hetGraph.py:90, in HetGraph._performTypeAssertions(self)
         86 def _performTypeAssertions(self) -> None:
         87     """
         88     A wrapper function that performs all type assertions during graph creation.
         89     """
    ---> 90     self.__assertEdgeTypes()


    File /opt/homebrew/lib/python3.10/site-packages/hetpy/models/hetGraph.py:62, in HetGraph.__assertEdgeTypes(self)
         60 defined_type = self.paths[edge.nodes[0].type, edge.nodes[1].type]
         61 if edge_type is not defined_type:
    ---> 62     raise TypeException(f"Some defined edge types do not match the defined paths: {edge_type} | {defined_type}! Abborting graph creation.")


    TypeException: A type error occured: Some defined edge types do not match the defined paths: wears | played_for! Abborting graph creation.


We can then again use the plotting approach to visualize our HetGraph.


```python
nodes = het_graph.nodes
vertex_labels = [node.attributes["Name"] for node in nodes[:-2]]
vertex_labels = vertex_labels + [node.attributes["shirt_color"] for node in nodes[-2:]]
color_map = {
    "Player": "orange",
    "Club": "pink",
    "Shirt": "white"
}
for edge in het_graph.edges:
    print(vars(edge))
visual_style = {
    "vertex_label": vertex_labels,
    "vertex_size": 0.3,
    "vertex_label_size": 8,
    "edge_label": [edge.type for edge in het_graph.edges],
    "edge_label_size": 8,
    "edge_align_label": True
}
layout = het_graph.graph.layout_kamada_kawai()
fig, ax = plt.subplots()
het_graph.plot(type_color_map=color_map, axis=ax, plot_args=visual_style, layout=layout)
```

    {'nodes': (<hetpy.models.node.Node object at 0x103725840>, <hetpy.models.node.Node object at 0x13d588550>), 'directed': False, 'type': 'played_for', 'attributes': {}}
    {'nodes': (<hetpy.models.node.Node object at 0x13d58b430>, <hetpy.models.node.Node object at 0x13d80e590>), 'directed': False, 'type': 'played_for', 'attributes': {}}
    {'nodes': (<hetpy.models.node.Node object at 0x13d58be20>, <hetpy.models.node.Node object at 0x13d588550>), 'directed': False, 'type': 'played_for', 'attributes': {}}
    {'nodes': (<hetpy.models.node.Node object at 0x13d58be20>, <hetpy.models.node.Node object at 0x13d80e590>), 'directed': False, 'type': 'played_for', 'attributes': {}}
    {'nodes': (<hetpy.models.node.Node object at 0x13d80e590>, <hetpy.models.node.Node object at 0x13d58b520>), 'directed': False, 'type': 'wears', 'attributes': {}}
    {'nodes': (<hetpy.models.node.Node object at 0x13d588550>, <hetpy.models.node.Node object at 0x13d58b6d0>), 'directed': False, 'type': 'wears', 'attributes': {}}



    
![png](../demo/hetPyDemo_files/hetPyDemo_15_1.png)
    


#### Meta Paths

In order to define rich semantics of the graphs domain on the object itself, the graph constructor also considers list of meta path objects and applies it on the graph. The MetaPath object takes a list of edge types, a description and a required abbreviation. The abbreviation functions as the unique identifier of the meta path. Here, we can reuse edge types defined on the path dictionary used before.


```python
edge_type_mappings = [(("Player","Club"),"played_for"), (("Club", "Shirt"),"wears")]
paths = HetPaths(edge_type_mappings)

print(paths)

hasPlayedInMetaPath = MetaPath(path=["played_for","wears"], description="The player has played in a certain shirt color", abbreviation="hasPlayedIn")
```

    {('Player', 'Club'): 'played_for', ('Club', 'Shirt'): 'wears'}



```python
# define nodes and edges
players = [Node("Player", {"Name": "Lionel Messi"}), Node("Player", {"Name": "Toni Kroos"}), Node("Player", {"Name": "Luis Figo"})]
clubs = [Node("Club", {"Name": "Real Madrid"}), Node("Club", {"Name": "FC Barcelona"})]
shirts = [Node("Shirt", {"shirt_color": "White"}), Node("Shirt", {"shirt_color": "Blue and Red"})]

nodes = list(itertools.chain(players, clubs, shirts))
edges = [
    Edge(players[0], clubs[1], False),
    Edge(players[1], clubs[0], False),
    Edge(players[2], clubs[1], False),
    Edge(players[2], clubs[0], False),
    Edge(clubs[0], shirts[0], False),
    Edge(clubs[1], shirts[1], False)
]
```


```python
hetGraphWithMetaPaths = HetGraph(nodes, edges, path_list=paths, meta_paths=[hasPlayedInMetaPath])
```

    Some edge types are undefined. Infering types from paths...


We can check whether the meta path was defined correctly on the graph.


```python
hetGraphWithMetaPaths.get_meta_paths()
```




    {'hasPlayedIn': ['played_for', 'wears']}



Also, we can add a meta path in hindsight.


```python
reverseMetaPath = MetaPath([paths[('Club','Shirt')], paths[('Player','Club')]], "The shirt color was worn by the player", "wasWornBy")
hetGraphWithMetaPaths.add_meta_path(reverseMetaPath)
```


```python
hetGraphWithMetaPaths.get_meta_paths()
```




    {'hasPlayedIn': ['played_for', 'wears'], 'wasWornBy': ['wears', 'played_for']}



#### Create a graph from a .csv file

HetPy provides a utility function to create a heterogeneous graph from a .csv file. For pracitcality reasons, we assume each row of the .csv file to be a node and create edges by specifying the row indices to which a node connects in a special column. 


```python
from hetpy import fromCSV
```

Consider the following column structure in our demo .csv file:


```python
data = pd.read_csv('./playClubData.csv', index_col="index")
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>name</th>
      <th>links_to</th>
    </tr>
    <tr>
      <th>index</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Player</td>
      <td>Lionel Messi</td>
      <td>[4]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Player</td>
      <td>Luis Figo</td>
      <td>[3, 4]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Player</td>
      <td>Sergio Ramos</td>
      <td>[3]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Club</td>
      <td>Real Madrid</td>
      <td>[5]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Club</td>
      <td>FC Barcelona</td>
      <td>[6]</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Stadium</td>
      <td>Bernabeu</td>
      <td>[3]</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Stadium</td>
      <td>Camp Nou</td>
      <td>[4]</td>
    </tr>
  </tbody>
</table>
</div>



We specify the type column and the foreign key column as function parameters and can then easily load the data into a csv file:


```python
column_attribute_map = {'Name': 'name'}
mock_graph = fromCSV('./playClubData.csv','type','links_to',consider_edge_directions=False, node_attribute_column_map=column_attribute_map)

mock_graph.node_types
```




    {'Club', 'Player', 'Stadium'}



The function also allows to pass arguments directly to the graphs initialization function as a dictionary. This way, we can also sepcify a network schema and a list of meta paths for the graph we want to create from a csv file.


```python
edge_type_mappings = [(("Player","Club"),"played_for"), (("Club", "Stadium"),"plays_in"), (('Stadium', 'Club'),"is_owned_by")]
paths = HetPaths(edge_type_mappings)

has_played_in_meta_path = MetaPath(path=["played_for","plays_in"], description="The player has played in a certain shirt color", abbreviation="hasPlayedIn")

graph_args = {
    'path_list': paths,
    'meta_paths': [has_played_in_meta_path]
}

loaded_graph = fromCSV('./playClubData.csv','type','links_to',consider_edge_directions=True, node_attribute_column_map=column_attribute_map, graphArgs=graph_args)

loaded_graph.paths
```

    Some edge types are undefined. Infering types from paths...





    {('Player', 'Club'): 'played_for',
     ('Club', 'Stadium'): 'plays_in',
     ('Stadium', 'Club'): 'is_owned_by'}




```python
type_color_map = {
    "Player": "orange",
    "Club": "pink",
    "Stadium": "blue"
}

layout = loaded_graph.graph.layout_kamada_kawai()

fig, ax = plt.subplots()

loaded_graph.plot(type_color_map=type_color_map, axis=ax, layout=layout)

```


    
![png](../demo/hetPyDemo_files/hetPyDemo_34_0.png)
    


#### Meta Projections

To compress the information a heterogeneous graph contains and focus on a particular node type relation, it is possible to create a projection of the graph on basis of a meta path. Following along the concept of bipartite projections in a bipartite graph, this is called a "meta projection".

A meta projection connects to two nodes if there exists a path that is an instance of the meta path that the projection is based on. Consequently, the meta projection show the relation between the node types of the source and the sink of the meta path. Consequently, if the source and the sink ahve the same type, the resulting projection graph only contains one node type. If the source and sink have different types, the resulting projection is a bipartite graph.

Take for example the following code to create a meta projection based on the already defined meta path "hasPlayedIn". It shows which player has already played in which shirt color.


```python
projection = create_meta_projection(loaded_graph, has_played_in_meta_path)

fig, ax = plt.subplots()
layout = projection.graph.layout_kamada_kawai()
projection.plot(type_color_map, axis=ax, layout=layout)
```


    
![png](../demo/hetPyDemo_files/hetPyDemo_36_0.png)
    


Projections can also be directed if specified.


```python
directed_projection = create_meta_projection(loaded_graph, has_played_in_meta_path, directed=True)

fig, ax = plt.subplots()
layout = directed_projection.graph.layout_kamada_kawai()
directed_projection.plot(type_color_map, axis=ax, layout=layout)
```


    
![png](../demo/hetPyDemo_files/hetPyDemo_38_0.png)
    



```python

```
