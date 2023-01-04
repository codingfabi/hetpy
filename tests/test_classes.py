import unittest

from hetpy import Node, Edge, HetGraph, HetPaths

class TestClasses(unittest.TestCase):

    def test_node(self):
        node = Node("MockType")
        self.assertEqual(node.type, "MockType")
    
    def test_edge(self):
        mockSourceNode = Node("MockType1")
        mockTargetNode = Node("MockType2")
        edge = Edge(mockSourceNode, mockTargetNode, False, "MockEdgeType")
        self.assertEqual(edge.type, "MockEdgeType")

    def test_hetGraph(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)

        self.assertEqual(hetGraphObject.nodeTypes, {"MockType1","MockType2","MockType3"})
        self.assertEqual(hetGraphObject.edgeTypes, {"MockEdgeType1","MockEdgeType2"})
        self.assertEqual(len(hetGraphObject.nodes), 4)
        self.assertEqual(len(hetGraphObject.edges), 2)

    def test_hetPaths(self):
        node_types = [(("MockNodeType1","MockNodeType2"), "EdgeType1"),(("MockNodeType1","MockNodeType3"), "EdgeType2")]
        paths = HetPaths(node_types)
        self.assertEqual(paths["MockNodeType1","MockNodeType2"], "EdgeType1")
        self.assertEqual(paths["MockNodeType1","MockNodeType3"], "EdgeType2")

    def test_hetPathsEmptyArguments(self):
        paths = HetPaths()
        self.assertEqual(paths, {})



if __name__ == '__main__':
    unittest.main()