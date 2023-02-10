import unittest

from hetpy import Node, Edge, HetGraph, HetPaths, MetaPath



class TestClasses(unittest.TestCase):

    def test_graphWithMetaPaths(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"), Edge(nodes[2], nodes[3], False, "EdgeType3")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        expected_dict = {
            "mck" : ["EdgeType1","EdgeType3"],
            "mck2": ["EdgeType2","EdgeType1"]
        }
        
        self.assertEqual(graph.get_meta_paths(), expected_dict)

    def test_addMetaPathRetrospectively(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"), Edge(nodes[2], nodes[3], False, "EdgeType3")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths)
        self.assertEqual(graph.get_meta_paths(), {})
        self.assertEqual(graph.meta_paths, [])

        expected_dict = {
            "mck" : ["EdgeType1","EdgeType3"],
        }

        graph.add_meta_path(mockMetaPath)
        self.assertEqual(graph.get_meta_paths(), expected_dict)

    def test_redundantMetapathDefinition(self):
        """
        Should throw an exception if a graph contains two meta paths with the same abbreviation.
        """
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"), Edge(nodes[2], nodes[3], False, "EdgeType3")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        expected_dict = {
            "mck" : ["EdgeType1","EdgeType3"],
            "mck2": ["EdgeType2","EdgeType1"]
        }
        
        self.assertEqual(graph.get_meta_paths(), expected_dict)

        duplicateMetaPath = MetaPath(["EdgeType2","EdgeType3"], "A redundant meta path", "mck2")
        with self.assertRaises(Exception) as context:
            graph.add_meta_path(duplicateMetaPath)

        self.assertTrue("A metapath with the abbreviaton mck2" in str(context.exception))

    def test_metapathRemoval(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"), Edge(nodes[2], nodes[3], False, "EdgeType3")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        graph.remove_meta_path("mck")

        expected_dict = {
            "mck2": ["EdgeType2","EdgeType1"]
        }

        self.assertEqual(graph.get_meta_paths(), expected_dict)

    def test_nonExistingMetapathRemoval(self):
        """
        Should throw an exception if a meta path is removed that does not exist on a graph.
        """
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"), Edge(nodes[2], nodes[3], False, "EdgeType3")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        with self.assertRaises(Exception) as context:
            graph.remove_meta_path('mck3')

        self.assertTrue("Metapath mck3" in str(context.exception))

if __name__ == '__main__':
    unittest.main()