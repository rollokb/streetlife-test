import random
from .tfl_graph import graph

MAX_MOVES = 100000

class Cat(object):
    def __init__(self, initial_station):
        self.current_station = initial_station

    def go_to_next(self):
        connections = graph.get_connections(self.current_station)
        try:
            # randomly pick from connections set
            self.current_station = random.sample(connections, 1)[0]
        except ValueError:
            # If there are no connections the cat is trapped!
            pass


class Person(object):

    def __init__(self, initial_station, cat, id):
        self.current_station = initial_station
        self.cat = cat
        self.id = id
        self.previous_stations = set()
        # The cat does not need to count it's moves. Because it moves each time it's
        # owner does.
        self.moves = 0

    def found_cat(self):
        "If person and cat are at the same station, the cat has been found"
        return self.current_station == self.cat.current_station

    def path_to_cat(self):
        "Returns the *current* path to the cat"
        return graph.find_path(self.current_station,
                                self.cat.current_station)

    def is_out_of_moves(self):
        return True if self.moves > MAX_MOVES else False

    def choose_station(self, paths):
        """
        choose_station checks if there are any connections that have not already
        been visited.
        """
        self.previous_stations.add(self.current_station)
        available_stations = graph.get_connections(self.current_station)
        prefered_stations = available_stations - self.previous_stations # sets arithmetic

        optimal_station = paths[1] # Next station in pathfinding route

        # if there are any prefered stations
        if len(prefered_stations) > 0:
            if optimal_station in prefered_stations:
                # if the optiminal station is in prefered_stations
                return optimal_station
            else:
                # if the optimal station is not in prefered_stations but there
                # are other stations to choose from, just choose any.
                return list(prefered_stations)[0] # any element
        else:
            # if it is not possible to move to a prefered station
            return optimal_station


    def step_to_cat(self):
        "Get the paths the person can take and choose the station"
        paths = graph.find_path(self.current_station,
                            self.cat.current_station)
        # If there are paths available, get the next station
        if paths is not None:
            self.current_station = self.choose_station(paths)
            self.moves = self.moves + 1

