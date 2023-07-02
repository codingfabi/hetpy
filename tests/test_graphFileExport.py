import unittest
import json
import datetime

from hetpy import Node, Edge, HetGraph, HetPaths, MetaPath



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


    def test_simpleJSONDump(self):
        graph = createSimpleMockHetGraph()
        graph.export_to_json("./tests/test_data/mockGraphExport.json")

        with open('./tests/test_data/mockGraphExport.json') as f:
            d = json.load(f)

            self.assertEqual(len(d["nodes"]),4)
            self.assertEqual(len(d["edges"]),2)


    def test_JSONDumpWithPaths(self):
        graph = createHetGraphWithPathDefinitions()

        graph.export_to_json("./tests/test_data/mockGraphExportWithPaths.json")

        with open('./tests/test_data/mockGraphExportWithPaths.json') as f:
            d = json.load(f)

            self.assertEqual(len(d["path_definitions"]),2)

    def test_JSONDumpWithMetapaths(self):
        graph = createHetGraphWithPathDefinitions()

        metapath = MetaPath(path=["EdgeType1","EdgeType2"], description="A mock meta path for testing export function.", abbreviation="mockAbbrv")
        
        graph.nodes[0].attributes = {"MockAttribute": "mockValue"}
        
        graph.add_meta_path(metapath)

        graph.export_to_json('./tests/test_data/mockGraphExportWithMetaPaths.json')

        with open('./tests/test_data/mockGraphExportWithMetaPaths.json') as f:
            d = json.load(f)

            self.assertEqual(len(d["meta_path_definitions"]), 1)
    
    def test_JSONDumpWithDates(self):
        graph = createHetGraphWithPathDefinitions()
        graph.add_path((("MockType2","MockType3"),"EdgeTypeWithTimestamp"))
        edge_with_timestamp = Edge(graph.get_nodes_of_type("MockType2")[0],graph.get_nodes_of_type("MockType3")[0], True, "EdgeTypeWithTimestamp",{"time": datetime.datetime.now()})
        node_with_timestamp = Node("MockType4", {"timestamp": datetime.datetime.now()})
        graph.add_node(node_with_timestamp)
        graph.add_edge(edge_with_timestamp)
        
        graph.export_to_json('./tests/test_data/mockGraphExportWithDates.json')
        




if __name__ == '__main__':
    unittest.main()