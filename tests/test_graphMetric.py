import unittest

from hetpy import Node, Edge, HetGraph, HetPaths

def createHetGraph():
    nodes_type_one = [
        Node("MockType1"),
        Node("MockType1"),
        Node("MockType1"),
        Node("MockType1"),
        Node("MockType1")
    ]
    nodes_type_two = [
        Node("MockType2"),
        Node("MockType2"),
        Node("MockType2")
    ]
    nodes_type_three = [
        Node("MockType3"),
        Node("MockType3"),
        Node("MockType3"),
        Node("MockType3")
    ]
    nodes_type_four = [
        Node("MockType4"),
        Node("MockType4"),
        Node("MockType4"),
        Node("MockType4"),
        Node("MockType4")
    ]
    nodes_type_five = [
        Node("MockType5"),
        Node("MockType5"),
        Node("MockType5"),
        Node("MockType5")
    ]
    type_mappings = [(("MockType1","MockType2"),"EdgeType1"), (("MockType2","MockType4"),"EdgeType2"),(("MockType3","MockType5"),"EdgeType3"),(("MockType4","MockType1"),"EdgeType4")]
    paths = HetPaths(type_mappings)
    edges_type_one = [Edge(nodes_type_one[0],nodes_type_two[0], False),Edge(nodes_type_one[1],nodes_type_two[1], False),Edge(nodes_type_one[2],nodes_type_two[2], False),Edge(nodes_type_one[3],nodes_type_two[1], False),Edge(nodes_type_one[4],nodes_type_two[0], False)]
    edges_type_two = [Edge(nodes_type_two[0],nodes_type_four[0], False),Edge(nodes_type_two[1],nodes_type_four[3], False),Edge(nodes_type_two[2],nodes_type_four[4], False)]
    edges_type_three = [Edge(nodes_type_three[0], nodes_type_five[0], False),Edge(nodes_type_three[1], nodes_type_five[0], False), Edge(nodes_type_three[2], nodes_type_five[3], False),Edge(nodes_type_three[1], nodes_type_five[2], False)]
    edges_type_four = [Edge(nodes_type_four[1],nodes_type_one[0], False),Edge(nodes_type_four[2],nodes_type_one[1], False),Edge(nodes_type_four[3],nodes_type_one[2], False),Edge(nodes_type_four[4],nodes_type_one[3], False)]
    nodes = nodes_type_one + nodes_type_two + nodes_type_three + nodes_type_four + nodes_type_five
    edges = edges_type_one + edges_type_two + edges_type_three + edges_type_four

    het_graph = HetGraph(nodes, edges, paths)
    return het_graph


class TestMetrics(unittest.TestCase):

    def test_nodeTypeDist(self):
        het_graph = createHetGraph()
        expected_dist = {
            "MockType1": 5,
            "MockType2": 3,
            "MockType3": 4,
            "MockType4": 5,
            "MockType5": 4
        }
        dist = het_graph.get_node_type_dist()
        self.assertEqual(expected_dist, dist)

    def test_nodeTypeDistPDF(self):
        het_graph = createHetGraph()
        expected_pdf = {
            "MockType1": 5/21,
            "MockType2": 3/21,
            "MockType3": 4/21,
            "MockType4": 5/21,
            "MockType5": 4/21
        }
        pdf = het_graph.get_node_type_dist(pdf=True)
        self.assertEqual(expected_pdf, pdf)

    def test_edgeTyeDist(self):
        het_graph = createHetGraph()
        expected_dist = {
            "EdgeType1": 5,
            "EdgeType2": 3,
            "EdgeType3": 4,
            "EdgeType4": 4
        }
        dist = het_graph.get_edge_type_dist()
        self.assertEqual(expected_dist, dist)

    def test_edgeTypeDistPDF(self):
        het_graph = createHetGraph()
        expected_pdf = {
            "EdgeType1": 5 / 16,
            "EdgeType2": 3 / 16,
            "EdgeType3": 4 / 16,
            "EdgeType4": 4 / 16
        }
        pdf = het_graph.get_edge_type_dist(pdf=True)
        self.assertEqual(expected_pdf, pdf)

if __name__ == '__main__':
    unittest.main()