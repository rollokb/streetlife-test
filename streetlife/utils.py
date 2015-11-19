import random
from .tfl_graph import graph
from .models import Cat, Person

def generate_people(number):
    "Generate n number of people in a random location different from their cat"
    people = []
    station_ids = graph.names.keys()
    for i in range(0, number):
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

    return people


def find_cats(people):
    people_found_cats = []
    people_lost_cats = []
    while people:
        # while we still have people in our array, tick the simulation
        for person in people:
            person.cat.go_to_next()
            person.step_to_cat()

            if person.found_cat():
                print("Person %d found cat %d - %s is now closed." %
                      (person.id, person.id, graph.names[person.current_station]))
                graph.close_station(person.current_station)
                # When we close the station we also need to check if this
                # permanently separates an owner from the cat
                people.remove(person)
                people_found_cats.append(person)
                break

            if not person.path_to_cat():
                # the person is trapped or there is no path to their cat.
                people.remove(person)
                people_lost_cats.append(person)
                break

            if person.is_out_of_moves():
                people.remove(person)
                people_lost_cats.append(person)
                break


    return people_found_cats, people_lost_cats

