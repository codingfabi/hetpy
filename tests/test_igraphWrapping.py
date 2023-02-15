import unittest
import matplotlib.pyplot as plt

from hetpy import Node, Edge, HetGraph, HetPaths

def createSimpleMockHetGraph():
    nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
    edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
    hetGraphObject = HetGraph(nodes, edges)

    return hetGraphObject

def createHetGraphWithPathDefinitions():
    nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
    edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]
    edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2")]
    paths = HetPaths(edge_type_mappings)
    graph = HetGraph(nodes, edges, paths)
    
    return graph
class TestClasses(unittest.TestCase):

    def test_simpleIGraphWraping(self):
        hetGraphObject = createSimpleMockHetGraph()

        self.assertEqual(len(hetGraphObject.graph.vs), 4)
        self.assertEqual(len(hetGraphObject.graph.es), 2)
        self.assertEqual(hetGraphObject.graph.is_directed(), False)
        self.assertEqual(hetGraphObject.graph.degree(), [1,1,1,1])

        
    def test_simpleTypeWrapping(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)

        for node in nodes:
            self.assertEqual(hetGraphObject._mapNodeToIGraphVertex(node)['Type'], node.type)

        for edge in edges:
            igraphEdge = hetGraphObject._mapEdgeToIGraphEdge(edge)
            self.assertEqual(igraphEdge["Type"], edge.type)

    def test_castGraphToDirected(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],True,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)

        self.assertEqual(hetGraphObject.graph.is_directed(), True)
        self.assertEqual(hetGraphObject.graph.degree(mode="out"), [1,1,0,0])
        self.assertEqual(hetGraphObject.graph.degree(mode="in"), [0,0,1,1])

    def test_edgeTypeInfering(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2")]
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)

        self.assertEqual(graph.edges[1].type, "EdgeType2")

    def test_edgeTypeAssertions(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"InvalidEdgeType")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2")]
        paths = HetPaths(edge_type_mappings)

        with self.assertRaises(Exception) as context:
            graph = HetGraph(nodes, edges, paths)
            self.assertIsNone(graph)

        self.assertTrue("Some defined edge types do not match the defined paths" in str(context.exception))

    def test_shouldNotOverwriteEdgeTypes(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2")]
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)

        self.assertEqual(graph.edges[0].type,"EdgeType1")
        self.assertEqual(graph.edges[1].type,"EdgeType2")

        edges[0].type = "WrongEdgeType"

        self.assertEqual(graph.edges[0].type, "EdgeType1")


    def test_nodeAttributeWrapping(self):
        nodes = [Node("MockType1", {"Name": "Node1"}),Node("MockType1", {"Name" : "Node2"}),Node("MockType2", {"Color": "Red"}),Node("MockType3", {"Name": "Node4"})]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)

        self.assertEqual(len(hetGraphObject.graph.vs), 4)
        self.assertEqual(len(hetGraphObject.graph.es), 2)
        self.assertEqual(hetGraphObject.graph.is_directed(), False)
        self.assertEqual(hetGraphObject.graph.degree(), [1,1,1,1])

        self.assertEqual(hetGraphObject.graph.vs[0]["Name"], "Node1")
        self.assertEqual(hetGraphObject.graph.vs[1]["Name"], "Node2")
        self.assertEqual(hetGraphObject.graph.vs[2]["Color"], "Red")
        self.assertEqual(hetGraphObject.graph.vs[3]["Name"], "Node4")
            
        # undefined attributes should be None
        self.assertEqual(hetGraphObject.graph.vs[0]["Color"], None)
        self.assertEqual(hetGraphObject.graph.vs[2]["Name"], None)

    def test_edgeAttributeWrapping(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1",{"Weight": 20}), Edge(nodes[1], nodes[3],False,"MockEdgeType2", {"Color": "Red"})]
        hetGraphObject = HetGraph(nodes, edges)

        self.assertEqual(len(hetGraphObject.graph.vs), 4)
        self.assertEqual(len(hetGraphObject.graph.es), 2)
        self.assertEqual(hetGraphObject.graph.is_directed(), False)
        self.assertEqual(hetGraphObject.graph.degree(), [1,1,1,1])

        self.assertEqual(hetGraphObject.graph.es[0]["Weight"], 20)
        self.assertEqual(hetGraphObject.graph.es[1]["Color"], "Red")

        # undefined attributes should be None
        self.assertEqual(hetGraphObject.graph.es[1]["Weight"], None)
        self.assertEqual(hetGraphObject.graph.es[0]["Color"], None)

    def test_nodeTypeSelection(self):
        nodes = [Node("MockType1", {"Name": "Node1"}),Node("MockType1", {"Name" : "Node2"}),Node("MockType2", {"Color": "Red"}),Node("MockType3", {"Name": "Node4"})]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)
        returned_nodes = hetGraphObject.get_nodes_of_type("MockType1")
        self.assertEqual(returned_nodes[0].attributes["Name"], "Node1")
        self.assertEqual(returned_nodes[1].attributes["Name"], "Node2")
    

    def test_nodeTypeSelectionError(self):
        nodes = [Node("MockType1", {"Name": "Node1"}),Node("MockType1", {"Name" : "Node2"}),Node("MockType2", {"Color": "Red"}),Node("MockType3", {"Name": "Node4"})]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)
        
        with self.assertRaises(Exception) as context:
            hetGraphObject.get_nodes_of_type("UndefinedMockType")
        
        self.assertTrue("Nodetype UndefinedMockType does not exist" in str(context.exception))

    def test_edgeTypeSelection(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1",{"Name": "Edge1"}), Edge(nodes[1], nodes[3],False,"MockEdgeType2",{"Name": "Edge2"})]
        hetGraphObject = HetGraph(nodes, edges)
        returned_edges = hetGraphObject.get_edges_of_type("MockEdgeType1")
        self.assertEqual(returned_edges[0].attributes["Name"], "Edge1")
    
    def test_edgeTypeSelectionUndefinedType(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1",{"Name": "Edge1"}), Edge(nodes[1], nodes[3],False,"MockEdgeType2",{"Name": "Edge2"})]
        hetGraphObject = HetGraph(nodes, edges)
        
        with self.assertRaises(Exception) as context:
            hetGraphObject.get_edges_of_type("UndefinedEdgeType")
        
        self.assertTrue("Edgetype UndefinedEdgeType does not exist" in str(context.exception))

    def test_graphPlotting(self):
        graph = createSimpleMockHetGraph()

        color_dict = {
            "MockType1": "orange",
            "MockType2": "red",
            "MockType3": "pink"
        }
        fig, ax = plt.subplots()
        graph.plot(
            type_color_map=color_dict,
            axis = ax
        )
        fig.savefig('tests/test_data/mockPlot.png')

    def test_graphPlottingWithVisualOptions(self):
        nodes = [Node("MockType1", {"Name": "Node1"}),Node("MockType1", {"Name": "Node2"}),Node("MockType2", {"Name": "Node3"}),Node("MockType3", {"Name": "Node4"})]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1", {"Name": "Edge1"}), Edge(nodes[1], nodes[3],False,"MockEdgeType2", {"Name": "Edge2"})]
        graph = HetGraph(nodes, edges)

        color_dict = {
            "MockType1": "orange",
            "MockType2": "red",
            "MockType3": "pink"
        }

        visual_style = {}
        visual_style["vertex_size"] = 0.1
        visual_style["vertex_label"] = graph.graph.vs["Name"]
        visual_style["edge_width"] = 1
        visual_style["edge_label"] = graph.graph.es["Type"]
        visual_style["bbox"] = (800, 800)
        visual_style["margin"] = 20

        fig, ax = plt.subplots()
        graph.plot(type_color_map = color_dict, axis=ax, plot_args = visual_style)

        fig.savefig('tests/test_data/styledMockPlot.png')

    def test_directedGraphPlotting(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],True,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)
        color_dict = {
            "MockType1": "orange",
            "MockType2": "red",
            "MockType3": "pink"
        }
        fig, ax = plt.subplots()
        hetGraphObject.plot(
            type_color_map=color_dict,
            axis = ax
        )
        fig.savefig('tests/test_data/directedMockPlot.png')

    def test_addPathDefinition(self):
        hetGraph = createSimpleMockHetGraph()
        edge_type_mapping= (("MockType1","MockType2"),"NewEdgeType")

        self.assertEqual(len(hetGraph.paths.keys()), 0)

        hetGraph.add_path(edge_type_mapping)

        self.assertEqual(len(hetGraph.paths.keys()),1)

    def test_addExistingPathDefinition(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2")]
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)

        with self.assertRaises(Exception) as context:
            graph.add_path((("MockType1","MockType2"),"NewEdgeTye"))
        
        self.assertTrue(f"The graph already contains a path definition for the node types" in str(context.exception))

    def test_removePathDefinition(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2")]
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)

        self.assertEqual(len(graph.paths.keys()),2)

        graph.remove_path((("MockType1","MockType2"), "EdgeType1"))

        self.assertEqual(len(graph.paths.keys()),1)

        graph.remove_path((("MockType1","MockType3"), "EdgeType2"))

        self.assertEqual(len(graph.paths.keys()),0)

    def test_removeInvalidPathDefinition(self):
        graph = createHetGraphWithPathDefinitions()

        with self.assertRaises(Exception) as context:
            graph.remove_path((("MockType1","MockType2"),"InvalidPathDefinition"))
        
        self.assertTrue("The graph contains a different path definition for the nodes ('MockType1', 'MockType2'), namely: EdgeType1" in str(context.exception))

    def test_removeNonExistentPathDefinition(self):
        graph = createHetGraphWithPathDefinitions()

        with self.assertRaises(Exception) as context:
            graph.remove_path((("MockType2","MockType3"),"NonExistentPath"))
        
        self.assertTrue("There is no path definition for the nodes ('MockType2', 'MockType3')" in str(context.exception))


    def test_addEdgeWithTypeToGraph(self):
        hetGraph = createSimpleMockHetGraph()
        new_edge = Edge(hetGraph.nodes[0], hetGraph.nodes[3], False, "NewType")
        hetGraph.add_edge(new_edge)

        self.assertEqual(len(hetGraph.edges), 3)
        self.assertEqual(hetGraph.edge_types, {'NewType','MockEdgeType1','MockEdgeType2'})
        
    def test_addEdgeWithoutTypeToGraph(self):
        hetGraph = createSimpleMockHetGraph()
        edge_type_mapping= (("MockType1","MockType3"),"MockEdgeType")
        hetGraph.add_path(edge_type_mapping)
        new_edge = Edge(hetGraph.nodes[0], hetGraph.nodes[3], False)
        hetGraph.add_edge(new_edge)

        self.assertEqual(len(hetGraph.edges), 3)

    def test_addNonExistingEdgeToGraph(self):
        """Should cause exception"""
        hetGraph = createSimpleMockHetGraph()
        non_existing_node = Node("nonExistingType")
        new_edge = Edge(hetGraph.nodes[0], non_existing_node, False)

        with self.assertRaises(Exception) as context:
            hetGraph.add_edge(new_edge)

        self.assertTrue("One of the nodes you are trying to connect does not exist in the graph" in str(context.exception))

    def test_removeEdgeFromGraph(self):
        hetGraph = createSimpleMockHetGraph()
        hetGraph.delete_edge(hetGraph.edges[0])

        self.assertEqual(len(hetGraph.edges), 1)
        self.assertEqual(len(hetGraph.graph.es), 1)
        self.assertEqual(hetGraph.edge_types, {'MockEdgeType2'})

    def test_removeNonExistingEdgeFromGraph(self):
        hetGraph = createSimpleMockHetGraph()
        non_existing_edge = Edge(hetGraph.nodes[0],hetGraph.nodes[0], False)

        self.assertEqual(len(hetGraph.edges), 2)
        self.assertEqual(len(hetGraph.graph.es), 2)

        with self.assertRaises(Exception) as context:
            hetGraph.delete_edge(non_existing_edge)

        self.assertEqual(len(hetGraph.edges), 2)
        self.assertEqual(len(hetGraph.graph.es), 2)
        
        self.assertTrue("The edge you are trying to remove does not exist on the graph." in str(context.exception))
        
    def test_addNodeToGraph(self):
        hetGraph = createSimpleMockHetGraph()
        new_node = Node("NewNodeType", {"NewAttr": "NewVal"})
        hetGraph.add_node(new_node)

        self.assertEqual(len(hetGraph.nodes), 5)
        self.assertEqual(hetGraph.node_types, {'NewNodeType','MockType1','MockType2','MockType3'})

        igraph_node = hetGraph._mapNodeToIGraphVertex(new_node)
        self.assertEqual(igraph_node["NewAttr"], "NewVal")

    def test_findEdge(self):
        het_graph = createSimpleMockHetGraph()
        
        retrieved_edge = het_graph.find_edge(het_graph.nodes[0], het_graph.nodes[2])
        self.assertEqual(retrieved_edge, het_graph.edges[0])
    
    def test_findNonexistingEdge(self):
        """
        Should throw exception
        """
        het_graph = createSimpleMockHetGraph()

        retrieved_edge = het_graph.find_edge(het_graph.nodes[0],het_graph.nodes[1])
        
        self.assertIsNone(retrieved_edge)


    def test_deleteNodeFromGraph(self):
        hetGraph = createSimpleMockHetGraph()
        hetGraph.delete_node(hetGraph.nodes[0])

        self.assertEqual(len(hetGraph.nodes), 3)
        self.assertEqual(len(hetGraph.graph.vs), 3)
        # check that edge was deleted aswell
        self.assertEqual(len(hetGraph.graph.es), 1)

    def test_deleteNonExistentNodeFromGraph(self):
        hetGraph = createSimpleMockHetGraph()
        nonExistentNode = Node("MockType",{"mockAttr":42})
        
        self.assertEqual(len(hetGraph.nodes), 4)
        with self.assertRaises(Exception) as context:
            hetGraph.delete_node(nonExistentNode)

        self.assertEqual(len(hetGraph.nodes), 4)
        
        self.assertTrue(f"The node with id {nonExistentNode.id} your are trying to remove is not defined on the graph." in str(context.exception))

    def test_advancedDeleteNodeFromGraph(self):
        hetGraph = createSimpleMockHetGraph()
        new_node = Node("NewNodeType", {"MockAttr": "MockValue"})
        new_edge = Edge(new_node, hetGraph.nodes[0], False)

        hetGraph.add_node(new_node)
        hetGraph.add_edge(new_edge)

        self.assertEqual(len(hetGraph.nodes), 5)
        self.assertEqual(len(hetGraph.edges), 3)

        hetGraph.delete_node(hetGraph.nodes[0])

        self.assertEqual(len(hetGraph.nodes), 4)
        self.assertEqual(len(hetGraph.edges), 1)
    
    def test_networkSchemaPlottingTerminal(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType3","MockType4"),"EdgeType3"),(("MockType4","MockType2"),"EdgeType4"),(("MockType3","MockType5"),"EdgeType5")]
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)

        graph.print_network_schema()
    
    def test_networkSchemaPlottingImage(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType3","MockType4"),"EdgeType3"),(("MockType4","MockType2"),"EdgeType4"),(("MockType3","MockType5"),"EdgeType5")]
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)

        fig, ax = plt.subplots(figsize=(16,9))
        graph.print_network_schema(axis=ax)
        fig.savefig('tests/test_data/networkSchema.png')


if __name__ == '__main__':
    unittest.main()