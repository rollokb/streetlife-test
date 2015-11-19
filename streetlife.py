#!/usr/local/bin/python3
import sys
import random
from pprint import pprint
from lib.tfl_graph import graph
from lib.utils import find_cats, generate_people


if __name__ == '__main__':
    # Default to 10 people and cats
    people_count = int(sys.argv[1]) if 1 < len(sys.argv) else 10
    print("%d cats and their owners will be spawned in the TFL network." \
          % people_count)

    people = generate_people(people_count)
    people_found_cats, people_lost_cats = find_cats(people)
    total_moves = sum([person.moves for person in people_found_cats])
    print([len(person.previous_stations) for person in people_found_cats])

    pprint(people_found_cats[0].previous_stations)

    print("moves %d" % people_found_cats[0].moves)
    # Stats!
    print("Total Number of cats: %d" % people_count)
    print("Number of cats found: %d" % len(people_found_cats))
    print("Average number of movements required to find cat: %d"
          %  (total_moves / len(people_found_cats) ) )
