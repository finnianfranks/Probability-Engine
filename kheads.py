"""
This file goes into different probabilistic metrics for flipping a coin and getting k heads in a row. Subsequently this is also flipping a coin and getting k tails in a row because 
of the symetry between heads and tails on a fair. Diverging from that though, we allow the user to parameterize the coin such it does not necessarily have to be fair and can instead
favor one side more than the other. For example, a coin that lands heads 70% of the time while only landing tails 30% of the time. 

Within this file we use NumPy to perform systems of equations calculations. The logic is explained within the respective code.
"""
from enum import Enum # the Enum class has not been used yet
import numpy as np


def expectedk(k, oddsHeads = .5):
    """
    The function will serve as the function which will numerically calculate the expected number of flips required to get k heads in a row.
    We also allow the user to parameterize the fairness of the coin.
    """
    print(f"we will find the expected number of flips for {k} consecutive heads for a fair coin")
    information = [("heads", oddsHeads), ("tails", 1 - oddsHeads), ("cost of a flip", 1)] # a list of tuples (for no particular reason) which lists the relevant information to perform such calculations
    for i in range(3):
        print(f"{information[i]}")
    print(f"we can find the experiment to be in {k + 1} different states") # this is true when our states are the number of consecutive heads we have landed. Elaboration below:
    """
    Let the state of the sequence be denoted E_i, where i is the number of consecutive heads we have thus far. Then, we start in the state E_0 because before we have
    flipped the coin we have 0 heads in a row. There are k+1 different states because we start at E_0 and go up through E_k. E_k is the state in which we have completed the goal
    and have obtained k heads in a row.
    """
    print(f"the states are...")
    for i in range(k+1):
        print(f"{i} consecutive heads")


    
    # in order to calculate the expected number of flips we have to use recurrence relations which means we will need an equation for each different state
    
    vectors = [[0] * (k) for i in range(k)] # here we are intializing our systems of equations. This list, vectors, will be intialized to contain k sublists, 
    # one for each state of the experiment excluding the final state which results in completion of the experiment. Within each of the sublists it will be necessary to keep track of all other 
    # states (the variables), hence each sublist is initialized with k 0's, one for each state. In order to understand this you have to understand solving the question using reccurence relations.
    vectors[0][0] = 1 - (1 - oddsHeads) # we manually enter the values for the beggining state which deviates from the predictable pattern of the other k-1 states in our vectors list.
    vectors[0][1] = -oddsHeads

    for i in range(1, len(vectors)-1): # now we are able to fill in the remaining sublists with a predictable pattern.
        vectors[i][0] = -(1 - oddsHeads) # because we have to balance each equation such that it's equal to a constant (in this case 1) the coefficients of our variables will 
        # appear to be negative. For this line, the probability of returning back to 0 heads is always the probability of tails, or '1 - oddsHeads' (negated because of above mentioned)
        vectors[i][i] = 1 # this is the state we are currently in
        vectors[i][i+1] = -oddsHeads # This is the probability of advancing to the next state. For example, going from 2 consecutive heads, to 3.
    vectors[k-1][0] = -(1-oddsHeads) # similar to how we had to manually enter the first values, we must also manually enter the last values which also deviate from a normal pattern.
    vectors[k-1][k-1] = 1
    A = np.array(vectors) # now using NumPy we set up the systems of equations
    b = np.array([1] * k) # because of the nature of the problem each sublist equation is actually equal to 1. remember how we had to balance it earlier in order to achieve this result?
    solution = np.linalg.solve(A, b)
    solution = solution[0] # we are only interested in the solution to E_0 since this is the expected value we are calculating
    solution = round(solution, 2)
    print(f"The expected number of flips required to achieve {k} consecutive heads is {solution}")
    
def main():
    expectedk(4, .5)

    



if __name__ == "__main__":
    main()

