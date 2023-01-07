import unittest

from hetpy import Node, Edge, HetGraph, HetPaths

class TestClasses(unittest.TestCase):

    def test_simpleIGraphWraping(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)

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



if __name__ == '__main__':
    unittest.main()