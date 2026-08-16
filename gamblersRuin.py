"""
This is the code document dedicated to the modeling of gamblers ruin through code
Next I need to design the simulation. Simulation has been designed.

The next step I can take in the gamblers ruin file is to calculate the expected number of trials it takes to win. That is equivalent to the expected number of trials 
it takes to reach N given that we do not reach 0 first. This question is a matter of conditional expectation and as such will require a new sort of calculation that I am not completely 
familiar with.
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
                                # if we wanted to take it further we could have just looked at state[N] to see the probability the game is 'won' in t moves. That's essentially what the function below is for

def gameEndsInTRoundsArray(i, p, N, t): # the only difference between this and the above function is that this return's the whole array such that I can use it to access any index I want
    state = [0] * (N + 1)
    state[i] = 1 
    count = 0 
    while count < t:
        newState = [0] * (N + 1)
        for j in range(1, N): 
            if state[j] != 0: 
                try: 
                    newState[j-1] += (1-p) * state[j]
                except IndexError:
                    pass
                try:
                    newState[j+1] += (p) * state[j]
                except IndexError:
                    pass
        state = newState
        count += 1
    return state 

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

"""
so the next step will be to calculate conditional expectation. We want to find the expected number of trials it takes to finish the game given we reach N. In order to do this I will 
have to find the probability that we finish the game in t steps given that we reach N. Isn't this the same as the probability that we win the game in t steps though? Ok yes let's think
about how I would find this now. 
"""
def probNoLoss(i, p, N, t):
    # so we are looking for the probability that the game ends in t rounds given that we win the game and do not lose the game
    # let t be the event that the game ends in t rounds and W be the event that we win the game. In that case we are looking for P(t|W)
    # This is equal to = P(W|t)P(t) / P(W). Luckily we already have the solutions to all these problems and can call on our other functions in order to solve the problem
    # Lets start with the top part
    wGivenT = gameEndsInTRoundsArray(i, p, N, t)
    numerator = wGivenT[-1]
    pW = playGame(i, p, N)
    return (numerator) / pW

def eXNoLoss(i, p, N): # of course I will now have to use more linalg and numpy in order to solve this problem
    """
    This function is a bit strange. and I assume it will be harder to implement but it will be a good excersise.
    So first what I need to do is to find the probability I win a round given I win the entire game. Let's call this P(U|W).
    this is equal to = P(W|U)P(U) / P(W). We can can call P(W|U) u_i+1 and that's the origal probability of winning when we are at i+1. That is over our original probability or u_i.
    All together this becomes (p*u_i+1)/u_i. Subsequently for the loss of a round this becomes (q*u_i-1)/u_i. The 'fun' part about this implementation is that the probability changes at every single state.
    We will of course use linalg for this approach and our handy dandy numPy.
    """
    equals = [1] * (N+1)
    equals[0] = 0
    equals[-1] = 0
    equations = [([0] * (N+1)) for _ in range(N+1)]
    for j in range(1, N):
        equations[j][j] = 1
        newProb = (playGame(j+1, p, N) * p) / playGame(j, p, N)
        newQ = (playGame(j-1, p, N) * (1-p)) / playGame(j, p, N)
        equations[j][j-1] = -(newQ)
        equations[j][j+1] = -(newProb)
    equations[0][0] = 1
    equations[N][N] = 1
    a = np.array(equations)
    b = np.array(equals)
    solution = np.linalg.solve(a, b)
    return solution[i]

def simExNoLoss(i, p, N, t):
    # we will no montecarlo simulate the expected number of trials it takes to complete the game by a win
    # I find the code to be generally straight forward and not require comments.
    res = []
    def winOrLoss(probability):
        return rd.random() < probability
    for j in range(t):
        at = i
        count = 0
        while at < N:
            if at == 0:
                count = -1
                break
            outcome = winOrLoss(p)
            if outcome:
                at += 1
            else:
                at -= 1
            count += 1
            
        if count == -1:
            continue
        else:
            res.append(count)
    return sum(res)/len(res)

        


        

def main():
    print(playGame(5, .5, 10))
    print(eX(5, .4, 10))
    print(gameEndsInTRounds(2, .6, 6, 2))
    print(simEX(500, 2, .6, 6))
    print(eXNoLoss(5, .4, 10))
    print(simExNoLoss(5, .4, 10, 10000))


if __name__ == "__main__":
    main()