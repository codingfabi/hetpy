import unittest

from hetpy import Node, Edge, HetGraph, HetPaths, MetaPath

class TestClasses(unittest.TestCase):

    def test_node(self):
        node = Node("MockType")
        self.assertEqual(node.type, "MockType")

    def test_nodeAttributes(self):
        mockNodeAttributes = {
            "name": "AMockNode",
            "color": "green"
        }
        node = Node("MockType", mockNodeAttributes)
        self.assertEqual(node.type, "MockType")
        self.assertEqual(node.attributes, mockNodeAttributes)
    
    def test_edge(self):
        mockSourceNode = Node("MockType1")
        mockTargetNode = Node("MockType2")
        edge = Edge(mockSourceNode, mockTargetNode, False, "MockEdgeType")
        self.assertEqual(edge.type, "MockEdgeType")

    def test_directedEdge(self):
        mockSourceNode = Node("MockType1")
        mockTargetNode = Node("MockType2")
        edge = Edge(mockSourceNode, mockTargetNode, True, "MockEdgeType")
        self.assertEqual(edge.type, "MockEdgeType")
        self.assertEqual(edge.directed, True)

    def test_edgeAttributes(self):
        mockSourceNode = Node("MockType1")
        mockTargetNode = Node("MockType2")
        edgeAttributes = {
            "weight": 2,
            "color":  "red"
        }
        edge = Edge(mockSourceNode, mockTargetNode, False, "MockEdgeType", edgeAttributes)
        self.assertEqual(edge.type, "MockEdgeType")
        self.assertEqual(edge.attributes, edgeAttributes)

    def test_edgeDefaultType(self):
        mockSourceNode = Node("MockType1")
        mockTargetNode = Node("MockType2")
        edge = Edge(mockSourceNode, mockTargetNode, False)
        self.assertEqual(edge.type, "")

    def test_hetGraph(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
        hetGraphObject = HetGraph(nodes, edges)

        self.assertEqual(hetGraphObject.node_types, {"MockType1","MockType2","MockType3"})
        self.assertEqual(hetGraphObject.edge_types, {"MockEdgeType1","MockEdgeType2"})
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

    def test_metaPaths(self):
        metaPath = MetaPath(["EdgeType1","EdgeType2","EdgeType3"], "A Mock Metapath", "123")
        self.assertEqual(metaPath.path, ["EdgeType1","EdgeType2","EdgeType3"])
        self.assertEqual(metaPath.description, "A Mock Metapath")
        self.assertEqual(metaPath.abbreviation, "123")
        self.assertEqual(metaPath.length, 3)




if __name__ == '__main__':
    unittest.main()