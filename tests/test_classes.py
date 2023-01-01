import unittest

from hetpy import Node, Edge

class TestClasses(unittest.TestCase):

    def test_node(self):
        node = Node("MockType")
        self.assertEqual(node.type, "MockType")

    def test_failing(self):
        node = Node("MockType")
        self.assertEqual(node.type, "asdfasfas")



if __name__ == '__main__':
    unittest.main()