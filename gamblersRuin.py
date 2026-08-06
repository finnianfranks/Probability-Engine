"""
This is the code document dedicated to the modeling of gamblers ruin through code
Next I need to design the simulation.

"""
import numpy as np
import random as rd

def playGame(i, p, N): # here i is our initial balance, p is our probability of winning any given round, N is our desired winnings at which we can stop the game.
    if p == .5:
        return i/N
    return round((1-((1-p)/p)**i)/(1 - ((1-p)/p)**N), 2) # The formula for this is derived in the gamblers ruin walkthrough on my substack
    
def eX(i,p,N): # This function will calculate the expected number of attempts it will take to reach a conclusion of the game (0 or N) if we start at i. We will use first step anaylsis in order to do so.
    equals = [1] * (N + 1) # ok so now the equals are all set up. I now need to set up the other side of the equation which will be a list of lists.
    equals[0] = 0
    equals[-1] = 0 # we intialize equals[0] and equals[-1] to be 0 because at this stage the game is concluded
    notEquals = [[0] * (N + 1) for _ in range(N + 1)]  # we create an array of arrays to store our systems of equations
    for j in range(1, N): # setting up our systems of equations with a recursive approach. because of the nature of first step analysis this approach makes sense. A proof may or may not be provided on the website
        notEquals[j][j-1] = -(1-p)
        notEquals[j][j] = 1
        notEquals[j][j+1] = -p
    notEquals[0][0] = 1 # for these a value of 1 must be placed since at this point the game is concluded anyway.
    notEquals[N][N] = 1
    a = np.array(notEquals) # using numpy to set up the linalg equations
    b = np.array(equals)
    solution = np.linalg.solve(a, b)
    return solution[i] # this is the state we were interested in at the beggining of the function

def gameEndsInTRounds(i, p, N, t): # this is the function which defines the probability that the game would end in t rounds, it defines the event P(T=t)
    state = [0] * (N + 1)
    state[i] = 1 # this is the state that we are in right now
    count = 0 # to end our while loop. In retrospect could have just used a for loop.
    while count < t:
        newState = [0] * (N + 1) # using dymanic programming. Create a new array to hold the updated values
        for j in range(1, N): # go through the original and tweak
            if state[j] != 0: # if probability here is not 0 then we know it's neighbors must be changed
                try: # accounting for index out of bounds error. RETROSPECT: pointless
                    newState[j-1] += (1-p) * state[j]
                except IndexError:
                    pass
                try:
                    newState[j+1] += (p) * state[j]
                except IndexError:
                    pass
        state = newState
        count += 1
    return state[0] + state[N] # the beggining and end combined is the probability that the game ends in this amount of moves
                                # if we wanted to take it further we could have just looked at state[N] to see the probability the game is 'won' in t moves.

def simEX(trials, i, p, N): # this is the pretty general monte-carlo simulation
    """
    it's my opinion that this code doesn't need a whole lot of explaining. I will sum it up though. We define a function 'isSuccess' within the overarching function. It is essentially
    just a bernoulli trial of winning or not winning a specific round of the game. I use the random library for this. We then run a loop 'trials' amount of times. Each run of the loop
    plays the game and records the number of attempts that had to be made in order to finish the game. Then those attempts are added to an array, 'res', and averaged.
    """
    res = []
    def isSuccess(k):
        return rd.random() < k
    for _ in range(trials):
        at = i
        count = 0
        while at != 0 and at != N:
            count += 1
            result = isSuccess(p)
            if result:
                at += 1
            else:
                at -= 1
        res.append(count)
    return sum(res)/trials



            
        
        

def main():
    print(playGame(5, .5, 10))
    print(eX(5, .4, 10))
    print(gameEndsInTRounds(2, .6, 6, 2))
    print(simEX(500, 2, .6, 6))

if __name__ == "__main__":
    main()