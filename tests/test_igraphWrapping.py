import unittest
import matplotlib.pyplot as plt

from hetpy import Node, Edge, HetGraph, HetPaths

def createSimpleMockHetGraph():
    nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
    edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
    hetGraphObject = HetGraph(nodes, edges)

    return hetGraphObject

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

        self.assertTrue("Some defined edge types do not match the defined paths" in str(context.exception))

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
        returned_nodes = hetGraphObject.getNodesOfType("MockType1")
        self.assertEqual(returned_nodes[0].attributes["Name"], "Node1")
        self.assertEqual(returned_nodes[1].attributes["Name"], "Node2")
    

    def test_nodeTypeSelectionError(self):
        nodes = [Node("MockType1", {"Name": "Node1"}),Node("MockType1", {"Name" : "Node2"}),Node("MockType2", {"Color": "Red"}),Node("MockType3", {"Name": "Node4"})]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)
        
        with self.assertRaises(Exception) as context:
            hetGraphObject.getNodesOfType("UndefinedMockType")
        
        self.assertTrue("Nodetype UndefinedMockType does not exist" in str(context.exception))

    def test_edgeTypeSelection(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1",{"Name": "Edge1"}), Edge(nodes[1], nodes[3],False,"MockEdgeType2",{"Name": "Edge2"})]
        hetGraphObject = HetGraph(nodes, edges)
        returned_edges = hetGraphObject.getEdgesOfType("MockEdgeType1")
        self.assertEqual(returned_edges[0].attributes["Name"], "Edge1")
    
    def test_edgeTypeSelection(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1",{"Name": "Edge1"}), Edge(nodes[1], nodes[3],False,"MockEdgeType2",{"Name": "Edge2"})]
        hetGraphObject = HetGraph(nodes, edges)
        
        with self.assertRaises(Exception) as context:
            hetGraphObject.getEdgesOfType("UndefinedEdgeType")
        
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

if __name__ == '__main__':
    unittest.main()