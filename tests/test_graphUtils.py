import unittest

from hetpy import fromCSV, from_iGraph, create_meta_projection
from hetpy.models.hetPaths import HetPaths
from hetpy.models.metaPath import MetaPath
from hetpy.models import Node, Edge, HetGraph

from hetpy.enums import CombineEdgeTypes

import igraph as ig

def createSimpleMockHetGraph():
    nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
    edges = [Edge(nodes[0],nodes[2],False,"MockEdgeType1"), Edge(nodes[1], nodes[3],False,"MockEdgeType2")]
    hetGraphObject = HetGraph(nodes, edges)

    return hetGraphObject

class TestUtils(unittest.TestCase):

    def test_createGraphFromCsv(self):
        column_attribute_map = {"Name": "name"}
        mockGraph = fromCSV('tests/test_data/simple_csv_test.csv','type','links_to',consider_edge_directions=False, node_attribute_column_map=column_attribute_map)
        
        self.assertEqual(mockGraph.node_types, {'Player','Club','Stadium'})
        self.assertEqual(mockGraph.nodes[0].attributes["Name"], "Lionel Messi")
        self.assertEqual(mockGraph.nodes[-1].type, "Stadium")
        self.assertEqual(mockGraph.nodes[-1].attributes["Name"], "Camp Nou")

        self.assertEqual(mockGraph.graph.is_directed(), False)

        self.assertEqual(mockGraph.graph.degree(), [1,2,1,4,4,2,2])
    
    def test_createDirectedGraphFromCsv(self):
        column_attribute_map = {"Name": "name"}
        mockGraph = fromCSV('tests/test_data/simple_csv_test.csv','type','links_to',consider_edge_directions=True, node_attribute_column_map=column_attribute_map)
        
        self.assertEqual(mockGraph.node_types, {'Player','Club','Stadium'})
        self.assertEqual(mockGraph.nodes[0].attributes["Name"], "Lionel Messi")
        self.assertEqual(mockGraph.nodes[-1].type, "Stadium")
        self.assertEqual(mockGraph.nodes[-1].attributes["Name"], "Camp Nou")

        self.assertEqual(mockGraph.graph.is_directed(), True)

        self.assertEqual(mockGraph.graph.degree(mode="in"), [0,0,0,3,3,1,1])
        self.assertEqual(mockGraph.graph.degree(mode="out"), [1,2,1,1,1,1,1])

    def test_createGraphWithPathsFromCSV(self):
        column_attribute_map = {"Name": "name"}
        edge_type_mappings = [(("Player","Club"), "played for"),(("Club","Stadium"),"owns"),(("Stadium","Club"),"belongs to")]
        meta_paths = [MetaPath(["Player", "Club", "Stadium"], "played in", "PI")]
        paths = HetPaths(edge_type_mappings)
        mockGraph = fromCSV('tests/test_data/simple_csv_test.csv','type','links_to',consider_edge_directions=True, node_attribute_column_map=column_attribute_map, graphArgs={"path_list": paths, "meta_paths": meta_paths})

        self.assertEqual(mockGraph.edge_types, {'played for', 'owns', 'belongs to'})
        self.assertEqual(mockGraph.paths, {("Player","Club"): "played for", ("Club","Stadium"): "owns", ("Stadium","Club"): "belongs to"})
        self.assertEqual(mockGraph.get_meta_paths(), {"PI": ["Player","Club","Stadium"]})

    def test_graphFromIGraph(self):
        graph = ig.Graph()
        graph.add_vertices(10)
        graph.vs["Type"] = ["TypeA","TypeA","TypeA","TypeB","TypeB","TypeB","TypeC","TypeC","TypeC","TypeC"]
        graph.vs["Color"] = ["Red", "Red", "Red","Blue","Blue","Blue","Blue","Yellow","Yellow","Yellow"]

        edges = [(0,3),(1,3),(1,4),(2,5),(3,7),(4,8),(5,8),(0,8)]
        graph.add_edges(edges)
        graph.es["Type"] = ["EdgeType1","EdgeType1","EdgeType1","EdgeType1","EdgeType2","EdgeType2","EdgeType2","EdgeType3"]
        graph.es["Size"] = [1,1,1,4,4,3,2,5]

        paths = HetPaths([(("TypeA","TypeB"),"EdgeType1"),(("TypeA","TypeC"),"EdgeType3"),(("TypeB","TypeC"),"EdgeType2")])

        het_graph = from_iGraph(graph, path_list = paths)

        self.assertEqual(het_graph.node_types, {"TypeA","TypeB","TypeC"})
        self.assertEqual(het_graph.edge_types, {"EdgeType1","EdgeType2","EdgeType3"})

        self.assertEqual(het_graph.nodes[0].attributes["iGraphIndex"],0)
        self.assertEqual(het_graph.nodes[0].attributes["Color"],"Red")
        self.assertEqual(het_graph.edges[0].attributes["iGraphIndex"],0)
        self.assertEqual(het_graph.edges[0].attributes["Size"],1)

    def test_graphFromIGraphWrongTypeAttribute(self):
        graph = ig.Graph()
        graph.add_vertices(10)
        graph.vs["VertexType"] = ["TypeA","TypeA","TypeA","TypeB","TypeB","TypeB","TypeC","TypeC","TypeC","TypeC"]
        graph.vs["Color"] = ["Red", "Red", "Red","Blue","Blue","Blue","Blue","Yellow","Yellow","Yellow"]

        edges = [(0,3),(1,3),(1,4),(2,5),(3,7),(4,8),(5,8),(0,8)]
        graph.add_edges(edges)
        graph.es["EdgeType"] = ["EdgeType1","EdgeType1","EdgeType1","EdgeType1","EdgeType2","EdgeType2","EdgeType2","EdgeType3"]
        graph.es["Size"] = [1,1,1,4,4,3,2,5]

        paths = HetPaths([(("TypeA","TypeB"),"EdgeType1"),(("TypeA","TypeC"),"EdgeType3"),(("TypeB","TypeC"),"EdgeType2")])

        with self.assertRaises(Exception) as context:
            het_graph = from_iGraph(graph, path_list = paths)
        
        self.assertTrue('type_attribute Type in iGraph node attributes' in str(context.exception))
    
    def test_graphFromIGraphAdjustedTypeAttribute(self):
        graph = ig.Graph()
        graph.add_vertices(10)
        graph.vs["type"] = ["TypeA","TypeA","TypeA","TypeB","TypeB","TypeB","TypeC","TypeC","TypeC","TypeC"]
        graph.vs["Color"] = ["Red", "Red", "Red","Blue","Blue","Blue","Blue","Yellow","Yellow","Yellow"]

        edges = [(0,3),(1,3),(1,4),(2,5),(3,7),(4,8),(5,8),(0,8)]
        graph.add_edges(edges)
        graph.es["type"] = ["EdgeType1","EdgeType1","EdgeType1","EdgeType1","EdgeType2","EdgeType2","EdgeType2","EdgeType3"]
        graph.es["Size"] = [1,1,1,4,4,3,2,5]

        paths = HetPaths([(("TypeA","TypeB"),"EdgeType1"),(("TypeA","TypeC"),"EdgeType3"),(("TypeB","TypeC"),"EdgeType2")])

        het_graph = from_iGraph(graph, type_attribute = "type", path_list = paths)

        self.assertEqual(het_graph.node_types, {"TypeA","TypeB","TypeC"})
        self.assertEqual(het_graph.edge_types, {"EdgeType1","EdgeType2","EdgeType3"})

        self.assertEqual(het_graph.nodes[0].attributes["iGraphIndex"],0)
        self.assertEqual(het_graph.nodes[0].attributes["Color"],"Red")
        self.assertEqual(het_graph.nodes[0].type,"TypeA")
        self.assertEqual(het_graph.edges[0].attributes["iGraphIndex"],0)
        self.assertEqual(het_graph.edges[0].type, "EdgeType1")
        self.assertEqual(het_graph.edges[0].attributes["Size"],1)

    def test_metaProjection(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],True,"EdgeType1"), Edge(nodes[1], nodes[3],True,"EdgeType2"),
                Edge(nodes[2], nodes[3], True, "EdgeType3"),Edge(nodes[5], nodes[3], True, "EdgeType3"),
                Edge(nodes[4], nodes[5], True, "EdgeType1"),Edge(nodes[5], nodes[6], True, "EdgeType3"),
                Edge(nodes[4], nodes[6], True, "EdgeType2")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        het_graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        projection = create_meta_projection(het_graph, mockMetaPath, True)

        self.assertTrue(projection.find_edge(nodes[0], nodes[3]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[0], nodes[3]).directed is True) # check if projection creation function respects direction argument
        self.assertTrue(projection.find_edge(nodes[4], nodes[3]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[4], nodes[6]) is not None) # check if edge is defined in projection

        self.assertTrue(projection.find_edge(nodes[1], nodes[3]) is None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[1], nodes[6]) is None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[0], nodes[2]) is None) # check if edge is defined in projection

    def test_metaProjectionShouldFailForUndefinedPaths(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"),
                Edge(nodes[2], nodes[3], False, "EdgeType3"),Edge(nodes[5], nodes[3], False, "EdgeType3"),
                Edge(nodes[4], nodes[5], False, "EdgeType1"),Edge(nodes[5], nodes[6], False, "EdgeType3"),
                Edge(nodes[4], nodes[6], False, "EdgeType2")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        het_graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        with self.assertRaises(Exception) as context:
            projection = create_meta_projection(het_graph, mockMetaPath, False)

        self.assertTrue('The edges of your graph contain an undefined path type.' in str(context.exception))

    def test_undirectedMetaProjection(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],False,"EdgeType1"), Edge(nodes[1], nodes[3],False,"EdgeType2"),
                Edge(nodes[2], nodes[3], False, "EdgeType3"),Edge(nodes[5], nodes[3], False, "EdgeType3"),
                Edge(nodes[4], nodes[5], False, "EdgeType1"),Edge(nodes[5], nodes[6], False, "EdgeType3"),
                Edge(nodes[4], nodes[6], False, "EdgeType2")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3"),(("MockType2","MockType1"),"EdgeType4"),(("MockType3","MockType2"),"EdgeType5")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        het_graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        projection = create_meta_projection(het_graph, mockMetaPath, False)

        self.assertTrue(projection.find_edge(nodes[0], nodes[3]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[0], nodes[3]).directed is False) # check if projection creation function respects direction argument
        self.assertTrue(projection.find_edge(nodes[4], nodes[3]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[4], nodes[3]).directed is False) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[4], nodes[6]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[4], nodes[6]).directed is False) # check if edge is defined in projection

    def test_multigraphMetaProjection(self):
        nodes = [Node("MockType1"),Node("MockType1"),Node("MockType2"),Node("MockType3"),Node("MockType1"),Node("MockType2"),Node("MockType3")]
        edges = [Edge(nodes[0],nodes[2],True,"EdgeType1"), Edge(nodes[1], nodes[3],True,"EdgeType2"),
                Edge(nodes[2], nodes[3], True, "EdgeType3"),Edge(nodes[5], nodes[3], True, "EdgeType3"),
                Edge(nodes[4], nodes[5], True, "EdgeType1"),Edge(nodes[5], nodes[6], True, "EdgeType3"),
                Edge(nodes[4], nodes[6], True, "EdgeType2"), Edge(nodes[4], nodes[2], True, "EdgeType1")]

        edge_type_mappings = [(("MockType1","MockType2"), "EdgeType1"),(("MockType1","MockType3"), "EdgeType2"),(("MockType2","MockType3"), "EdgeType3")]
        mockMetaPath = MetaPath(["EdgeType1", "EdgeType3"], "A mock meta path", "mck")
        secondMockMetaPath = MetaPath(["EdgeType2","EdgeType1"], "Another, non existend mock meta path", "mck2")
        paths = HetPaths(edge_type_mappings)

        het_graph = HetGraph(nodes, edges, paths, [mockMetaPath, secondMockMetaPath])

        projection = create_meta_projection(het_graph, mockMetaPath, True, combine_edges=CombineEdgeTypes.SUM)

        self.assertTrue(projection.find_edge(nodes[0], nodes[3]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[0], nodes[3]).directed is True) # check if projection creation function respects direction argument
        self.assertTrue(projection.find_edge(nodes[4], nodes[3]) is not None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[4], nodes[6]) is not None) # check if edge is defined in projection

        self.assertTrue(projection.find_edge(nodes[1], nodes[3]) is None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[1], nodes[6]) is None) # check if edge is defined in projection
        self.assertTrue(projection.find_edge(nodes[0], nodes[2]) is None) # check if edge is defined in projection

        self.assertTrue(projection.find_edge(nodes[4], nodes[3]).attributes["Weight"] is 2) # check weights on edges when edge combining is specified
        self.assertTrue(projection.find_edge(nodes[0], nodes[3]).attributes["Weight"] is 1) # check weights on edges when edge combining is specified
        self.assertTrue(projection.find_edge(nodes[4], nodes[6]).attributes["Weight"] is 1) # check weights on edges when edge combining is specified

        
