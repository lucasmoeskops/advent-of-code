import unittest
from .main import parse_grid, NodeGrid, Node


class ParseGridTestCase(unittest.TestCase):
    def test(self):
        data = 'root@ebhq-gridcenter# df -h\n'\
               'Filesystem              Size  Used  Avail  Use%\n'\
               '/dev/grid/node-x3-y7     85T   72T    13T   84%'
        grid = parse_grid(data.split('\n'))
        self.assertEqual(1, len(grid.nodes))
        self.assertEqual(complex(3, 7), next(iter(grid.nodes.keys())))
        node = next(iter(grid.nodes.values()))
        self.assertEqual(85, node.space_total)
        self.assertEqual(13, node.space_available)
        self.assertEqual(72, node.space_used)


class NodeGridTestCase(unittest.TestCase):
    def test(self):
        node_grid = NodeGrid()
        node_grid.add_node(0, 0, Node(20, 10))
        node_grid.add_node(0, 1, Node(30, 10))
        node_grid.add_node(0, 2, Node(30, 0))
        self.assertEqual(1, node_grid.viable_pairs())


if __name__ == '__main__':
    unittest.main()

