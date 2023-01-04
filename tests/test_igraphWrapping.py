import unittest

from hetpy import Node, Edge, HetGraph

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

if __name__ == '__main__':
    unittest.main()