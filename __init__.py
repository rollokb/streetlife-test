import sys
import pdb
from pprint import pprint
from collections import defaultdict

class TFLNetworkGraph(object):
    """
    To make sense of the data provided, we can
    consider stations to be nodes, and connections
    to be edges.

    It is probably best to create a Graph object to
    manange the data.
    """
    names = {} # Just a dict to look up the name for id

    def __init__(self, connections, names):
        self._graph = defaultdict(set)
        self.names = names
        self.add_many_connections(connections)

    def add_many_connections(self, connections):
        "Add connetions (list of tuples)"
        for station1, station2 in connections:
            self.add_connection(station1, station2)

    def add_connection(self, station1, station2):
        "Create a connection between the two stations"
        self._graph[station1].add(station2)
        self._graph[station2].add(station1)


def main(cats_and_owners):
    names = {}
    connections = []

    # load the names
    with open('tfl_stations.csv') as f:
        for line in f:
            data = line.split(',')
            id = int(data[0]) # cast id to an int
            name = data[1][:-1] # truncate new line char
            names[id] = name

    with open('tfl_connections.csv') as f:
        for line in f:
            data = line.split(',')
            station1 = int(data[0])
            station2 = int(data[1])
            connections.append((station1, station2))


    graph = TFLNetworkGraph(connections, names)

    pdb.set_trace()




if __name__ == '__main__':
    # Default to 10 cats
    cats_and_owners = sys.argv[1] if 1 < len(sys.argv) else 10
    print("%d cats and owners have been spawned in the TFL network." \
          % cats_and_owners)

    main(cats_and_owners)
