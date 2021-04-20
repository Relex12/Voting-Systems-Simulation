from random import random
from math import sqrt, pow, fsum, fabs
import matplotlib.pyplot as plt

from voting import *

#############
# FUNCTIONS #
#############

def distance(pointA, pointB):
    return sqrt(fsum([pow(fabs(pointA[i]-pointB[i]), 2) for i in range (0, len(pointA))]))

def iniate_dict(number, dimension):
    dict = {}
    for i in range(0, number):
        element = []
        for j in range(0, dimension):
            element.append(random())
        dict[i] = element
    return (dict)

def plot_grid(voters, candidates):
    fig, ax = plt.subplots()

    ax.scatter([voters[v][0] for v in voters], [voters[v][1] for v in voters],
    s=10, c="black")
    for c in candidates:
        ax.scatter(candidates[c][0], candidates[c][1])
        ax.annotate(str(c), (candidates[c][0], candidates[c][1]))
    ax.grid(True)
    fig.suptitle("Voter and candidate positions")
    plt.savefig("positions.png")


###########
# GLOBALS #
###########

space_dimension = 2
number_of_voters = 50
number_of_candidates = 10

########
# MAIN #
########

def main():
    voters = iniate_dict(number_of_voters, space_dimension)
    candidates = iniate_dict(number_of_candidates, space_dimension)

    plot_grid(voters, candidates)

    distances = {voter: { candidate: distance(voters[voter], candidates[candidate]) for candidate in candidates} for voter in voters }

    ranked_preferences = {voter: [candidate for candidate, distance in sorted(distances[voter].items(), key=lambda item: item[1])] for voter in voters}

    copy = ranked_preferences
    print("plurality:\t", N_rounds(copy, 1))
    copy = ranked_preferences
    print("two round:\t", N_rounds(copy, 2))
    copy = ranked_preferences
    print("instant runoff:\t", N_rounds(copy, number_of_candidates-1))
    copy = ranked_preferences
    print("condorcet:\t", condorcet(copy))
    copy = ranked_preferences
    print("borda:\t\t", borda(copy))

def test():
    j = 0
    max = 10000
    for i in range (1, max+1):
        voters = iniate_dict(number_of_voters, space_dimension)
        candidates = iniate_dict(number_of_candidates, space_dimension)
        distances = {voter: { candidate: distance(voters[voter], candidates[candidate]) for candidate in candidates} for voter in voters }
        ranked_preferences = {voter: [candidate for candidate, distance in sorted(distances[voter].items(), key=lambda item: item[1])] for voter in voters}
        copy = ranked_preferences
        if (condorcet(copy) == None):
            j+=1
            print (j*100/i)
    print (j*100/i)

if __name__ == '__main__':
    main()
    # test()
