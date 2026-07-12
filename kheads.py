"""
Here we will simulate the time it takes for a use to
flip k consecutive heads
"""
from enum import Enum
import numpy as np


def expectedk(k, oddsHeads):
    print(f"we will find the expected number of flips for {k} consecutive heads for a fair coin")
    information = [("heads", oddsHeads), ("tails", 1 - oddsHeads), ("cost of a flip", 1)]
    for i in range(3):
        print(f"{information[i]}")
    print(f"we can find the coin in {k + 1} different states")
    print(f"the states are...")
    for i in range(k+1):
        print(f"{i} consecutive heads")


    vectors = [[0] * (k) for i in range(k)]
    vectors[0][0] = 1 - (1 - oddsHeads)
    vectors[0][1] = -oddsHeads

    for i in range(1, len(vectors)-1):
        vectors[i][0] = -(1 - oddsHeads)
        vectors[i][i] = 1
        vectors[i][i+1] = -oddsHeads
    vectors[k-1][0] = -(1-oddsHeads)
    vectors[k-1][k-1] = 1
    A = np.array(vectors)
    b = np.array([1] * k)
    solution = np.linalg.solve(A, b)
    solution = solution[0]
    print(solution)
    
def main():
    expectedk(3, .6)

    



if __name__ == "__main__":
    main()

