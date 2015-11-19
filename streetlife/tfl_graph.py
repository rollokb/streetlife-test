import pdb
from collections import defaultdict
from pprint import pprint


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
        "Add connections (list of tuples)"
        for station1, station2 in connections:
            self.add_connection(station1, station2)

    def add_connection(self, station1, station2):
        "Create a *bidirectional* connection between the two stations"
        self._graph[station1].add(station2)
        self._graph[station2].add(station1)

    def get_connections(self, station):
        return self._graph[station]

    def find_path(self, station1, station2):
        """
        find_path works using a BDF algorithm to search for the
        destination (if a path exists). I set the node's parent
        (for this context), and then work backwards to find the
        actual path.
        """
        parents = self._get_parent_chain(station1, station2)

        if len(parents) > 0:
            path = [station2]
            while path[-1] != station1:
                try:
                    path.append(parents[path[-1]])
                except KeyError:
                    return None

            path.reverse()
            return path
        else:
            return None

    def _get_parent_chain(self, station1, station2):
        visited = dict.fromkeys(self._graph.keys(), False)
        queue = []
        parent = {}
        visited[station1] = True
        queue.append(station1)

        while len(queue) > 0:
            station = queue.pop(0)
            if station == station2: # Reached our destination
                return parent

            for adjacent in self.get_connections(station):
                if not visited[adjacent]:
                    visited[adjacent] = True;
                    parent[adjacent] = station
                    queue.append(adjacent)

        return parent



    def close_station(self, station):
        "Remove the station and all refs to it"
        for n, cxns in self._graph.items():
            try:
                cxns.remove(station)
            except KeyError:
                pass

        try:
            del self._graph[station]
        except KeyError:
            pass


def create_tfl_grapth():
    names = {}
    connections = []

    # load the names
    with open('tfl_stations.csv') as f:
        for line in f:
            data = line.split(',')
            id = int(data[0]) # cast id to an int
            name = data[1][:-1] # truncate new line char
            names[id] = name

    # load the connections (edges)
    with open('tfl_connections.csv') as f:
        for line in f:
            data = line.split(',')
            station1 = int(data[0]) # cast to int
            station2 = int(data[1])
            connections.append((station1, station2)) # Append a tuple of the connection

    return TFLNetworkGraph(connections, names)


# Load the data!
graph = create_tfl_grapth()
