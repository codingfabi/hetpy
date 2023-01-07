import unittest

from hetpy import Node, Edge, HetGraph, HetPaths, MetaPath



class TestClasses(unittest.TestCase):

    def test_graphWithMetaPaths(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False), Edge(nodes[2], nodes[3], False)]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        expected_dict = {
            "mck" : ["EdgeType1","EdgeType3"],
            "mck2": ["EdgeType2","EdgeType1"]
        }
        
        self.assertEqual(graph.getDefinedMetaPaths(), expected_dict)