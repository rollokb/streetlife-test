#!/usr/local/bin/python3
import sys
import random
from pprint import pprint
from streetlife.tfl_graph import graph
from streetlife.utils import find_cats, generate_people


if __name__ == '__main__':
    # Default to 10 people and cats
    people_count = int(sys.argv[1]) if 1 < len(sys.argv) else 10
    print("%d cats and their owners will be spawned in the TFL network." \
          % people_count)

    people = generate_people(people_count)
    people_found_cats, people_lost_cats = find_cats(people)
    total_moves = sum([person.moves for person in people_found_cats])

    # Stats!
    print("Total Number of cats: %d" % people_count)
    print("Number of cats found: %d" % len(people_found_cats))
    print("Average number of movements required to find cat: %d"
          %  (total_moves / len(people_found_cats) ) )

    # Sort people who lost cats by their moves
    people_lost_cats_by_moves = sorted(people_lost_cats, key=lambda x: x.moves,
                                       reverse=True)

    # least lucky person is the one who moved the most
    # out of those who didn't find their cat
    least_lucky_person = people_lost_cats_by_moves[0]


    print("Least lucky owner was person %d who moved %d times *and* lost their cat" %
           (least_lucky_person.id, least_lucky_person.moves))
