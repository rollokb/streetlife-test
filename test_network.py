from pprint import pprint
from .network import TFLNetworkGraph

def test_traversal():
    graph = TFLNetworkGraph(
        [(0,1),
         (0,2),
         (4, 5),
         (1,2),
         (2,3),
         (3,3)],
        {}
    )

    backtrace = graph.find_path(2, 5)
    pprint(backtrace)

