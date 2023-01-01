import unittest

from hetpy import Node, Edge

class TestClasses(unittest.TestCase):

    def test_node(self):
        node = Node("MockType")
        self.assertEqual(node.type, "MockType")

if __name__ == '__main__':
    unittest.main()