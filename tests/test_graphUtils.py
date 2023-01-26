import unittest

from hetpy import fromCSV, from_iGraph
from hetpy.models.hetPaths import HetPaths
from hetpy.models.metaPath import MetaPath

import igraph as ig


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



        
