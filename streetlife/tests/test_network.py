from pprint import pprint
from streetlife.tfl_graph import TFLNetworkGraph

def test_pathfinding_with_line():
    """
    A test of the most basic pathfinding of the TFLNetworkGraph
    The dataset represents a graph with a single branch.
    0-----1-----2

    The path from 0 to 1 should be 0,1,2
    """
    graph = TFLNetworkGraph(
        [
         (0,1),
         (1,2),
        ],
        {}
    )
    path = graph.find_path(0, 2)
    assert path == [0,1,2]

def test_pathfinding_with_tree():
    """
    A test of the pathfinding of the TFLNetworkGraph where there is a branch
    The dataset can visually be represented like so:

        1-----2
       /
      0
       \
        3-----4

    The path from 0 to 2 should be 0,1,2
    """
    graph = TFLNetworkGraph(
        [
         (0,1),
         (0,3),
         (1,2),
         (3,4)
        ],
        {}
    )
    # top branch
    path = graph.find_path(0, 2)
    assert path == [0,1,2]

    # bottom branch
    path = graph.find_path(0, 4)
    assert path == [0,3,4]

def test_pathfinding_with_cyclical_graph():
    """
    A test of the pathfinding of the TFLNetworkGraph.
    The dataset can visually be represented like so:

                   6----1-----2
                  /    /
                 5----0
                       \
                        3-----4

    """
    graph = TFLNetworkGraph(
        [
         (0,1),
         (0,3),
         (1,2),
         (3,4),
         (5,0),
         (5,6),
         (6,1)
        ],
        {}
    )
    # top branch
    path = graph.find_path(0, 2)
    assert path == [0,1,2]

    # bottom branch
    path = graph.find_path(0, 4)
    assert path == [0,3,4]

    path = graph.find_path(0, 6)
    assert path == [0,1,6] or path == [0,5,6]

def test_remove_node_then_attempt_pathfind():
    """
    The dataset represents a graph with a single branch.

    0-----1-----2

    We then remove node 1, and test if no path can be traced
    between 0 and 1
    """
    graph = TFLNetworkGraph(
        [
         (0,1),
         (1,2),
        ],
        {}
    )
    path = graph.find_path(0, 2)
    assert path == [0,1,2]

    graph.close_station(1)
    obstructed_path = graph.find_path(0, 2)
    assert obstructed_path == None
