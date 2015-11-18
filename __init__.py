import sys
import pdb
import random
from pprint import pprint
from network import graph, names, NoPathFoundException


class Cat(object):
    current_station = None
    trapped = False


    def __init__(self, initial_station):
        self.current_station = initial_station

    def go_to_next(self):
        connections = graph.get_connections(self.current_station)
        # get any element of the connections set
        try:
            self.current_station = random.sample(connections, 1)[0]
        except ValueError:
            # If there are no connections the cat is trapped!
            pass


class Person(object):
    current_station = None
    id = None
    trapped = False
    cat = None
    moves = 0
    previous_stations = []

    def __init__(self, initial_station, cat, id):
        self.current_station = initial_station
        self.cat = cat
        self.id = id

    def found_cat(self):
        return self.current_station == self.cat.current_station

    def path_to_cat(self):
        try:
            return graph.find_path(self.current_station,
                                   self.cat.current_station)
        except NoPathFoundException:
            pass

    def step_to_cat(self):
        """
        A person will avoid going to a station they have already
        visited unless there is no other option.
        """
        paths = self.path_to_cat()
        if paths is not None:
            try:
                self.previous_stations.append(self.current_station)
                self.current_station = paths[1]
            except IndexError:
                pass



def main(cats_and_owners):
    people = []
    # In the dataset provided, the keys are a continuous list
    # So I'm making the assumption that there will be an id for
    # each number within 1 ... count(name.keys())
    station_ids = names.keys()

    for i in range(0, cats_and_owners):
        # copy the station ids
        availiable_spawns = list(station_ids)
        # Make sure that cat and owner spawns are different
        cat_spawn_station_id = availiable_spawns[random.randrange(1, len(availiable_spawns))]
        # remove cat's owner from list of available spawns
        availiable_spawns.remove(cat_spawn_station_id)
        # we can now pick id from the available_spawns
        person_spawn_station_id = random.choice(availiable_spawns)
        # Construct a person missing his cat
        cat = Cat(cat_spawn_station_id)
        person = Person(person_spawn_station_id, cat, i+1)
        people.append(person)


    people_who_found_their_cat = []

    while len(people) > 0:
        # while we still have people in our array, step their locations
        # and their cats
        for person in people:
            # Because the movement of a person is dependant on the position of
            # the cat, I am making the assumption that a person follows a cat to
            # its next station.
            person.cat.go_to_next()
            person.step_to_cat()

            if person.found_cat():
                print("Person %d found cat %d - %s is now closed." %
                      (person.id, person.id, names[person.current_station]))
                graph.close_station(person.current_station)
                # When we close the station we also need to check if this
                # permanently separates an owner from the cat
                people.remove(person)
                people_who_found_their_cat.append(person)
                break

            if not person.path_to_cat():
                # the person is trapped or there is no path to their cat.
                people.remove(person)
                break


    # Calculate the stats
    print("Total Number of cats: %d" % cats_and_owners)
    print("Number of cats found: %d" % len(people_who_found_their_cat))
    total_moves = sum([person.moves for person in people_who_found_their_cat])
    print("Average number of movements required to find cat: %d"
          %  (total_moves / len(people_who_found_their_cat) ) )





if __name__ == '__main__':
    # Default to 10 cats
    cats_and_owners = int(sys.argv[1]) if 1 < len(sys.argv) else 10
    print("%d cats and owners have been spawned in the TFL network." \
          % cats_and_owners)
    main(cats_and_owners)
