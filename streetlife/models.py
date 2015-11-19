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
    previous_stations = set()
    # The cat does not need to count it's moves. Because it moves each time it's
    # owner does.
    moves = 0

    def __init__(self, initial_station, cat, id):
        self.current_station = initial_station
        self.cat = cat
        self.id = id

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
        try:
            self.previous_stations.add(self.current_station)
            # Avoid stations already visited
            prefered_stations = [s for s in paths if s not in self.previous_stations]
            if prefered_stations:
                next_station = prefered_stations[0]
            else:
                next_station = paths[1]

            self.current_station = next_station
            self.moves = self.moves + 1
        except IndexError:
            pass

    def step_to_cat(self):
        "Get the paths the person can take and choose the station"
        paths = graph.find_path(self.current_station,
                            self.cat.current_station)
        # If there are paths available, get the next station
        if paths is not None:
            self.choose_station(paths)

