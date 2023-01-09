import unittest

from hetpy import fromCSV


class TestUtils(unittest.TestCase):

    def test_createGraphFromCsv(self):
        column_attribute_map = {"Name": "name"}
        mockGraph = fromCSV('tests/test_data/simple_csv_test.csv','type','links_to',consider_edge_directions=False, node_attribute_column_map=column_attribute_map)
        
        self.assertEqual(mockGraph.nodeTypes, {'Player','Club','Stadium'})
        self.assertEqual(mockGraph.nodes[0].attributes["Name"], "Lionel Messi")
        self.assertEqual(mockGraph.nodes[-1].type, "Stadium")
        self.assertEqual(mockGraph.nodes[-1].attributes["Name"], "Camp Nou")

        self.assertEqual(mockGraph.graph.is_directed(), False)

        self.assertEqual(mockGraph.graph.degree(), [1,2,1,4,4,2,2])
    
    def test_createDirectedGraphFromCsv(self):
        column_attribute_map = {"Name": "name"}
        mockGraph = fromCSV('tests/test_data/simple_csv_test.csv','type','links_to',consider_edge_directions=True, node_attribute_column_map=column_attribute_map)
        
        self.assertEqual(mockGraph.nodeTypes, {'Player','Club','Stadium'})
        self.assertEqual(mockGraph.nodes[0].attributes["Name"], "Lionel Messi")
        self.assertEqual(mockGraph.nodes[-1].type, "Stadium")
        self.assertEqual(mockGraph.nodes[-1].attributes["Name"], "Camp Nou")

        self.assertEqual(mockGraph.graph.is_directed(), True)

        self.assertEqual(mockGraph.graph.degree(mode="in"), [0,0,0,3,3,1,1])
        self.assertEqual(mockGraph.graph.degree(mode="out"), [1,2,1,1,1,1,1])