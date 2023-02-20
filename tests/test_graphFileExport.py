import unittest
import json

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
        graph.export_to_json("./mockGraphExport.json")

        with open('./mockGraphExport.json') as f:
            d = json.load(f)

            self.assertEqual(len(d["nodes"]),4)
            self.assertEqual(len(d["edges"]),2)


    def test_JSONDumpWithPaths(self):
        graph = createHetGraphWithPathDefinitions()

        graph.export_to_json("./mockGraphExportWithPaths.json")

        with open('./mockGraphExportWithPaths.json') as f:
            d = json.load(f)

            self.assertEqual(len(d["path_definitions"]),2)

    def test_JSONDumpWithMetapaths(self):
        graph = createHetGraphWithPathDefinitions()

        metapath = MetaPath(path=["EdgeType1","EdgeType2"], description="A mock meta path for testing export function.", abbreviation="mockAbbrv")
        
        graph.add_meta_path(metapath)

        graph.export_to_json('./mockGraphExportWithMetaPaths.json')

        with open('./mockGraphExportWithMetaPaths.json') as f:
            d = json.load(f)

            self.assertEqual(len(d["meta_path_definitions"]), 1)




if __name__ == '__main__':
    unittest.main()