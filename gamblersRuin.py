"""
This is the code document dedicated to the modeling of gamblers ruin through code
"""
import numpy as np

def playGame(i, p, N): # here i is our initial balance, p is our probability of winning any given round, N is our desired winnings at which we can stop the game.
    if p == .5:
        return i/N
    return round((1-((1-p)/p)**i)/(1 - ((1-p)/p)**N), 2) # The formula for this is derived in the gamblers ruin walkthrough on my substack
    
def eX(i,p,N): # This function will calculate the expected number of attempts it will take to reach N if we start at i. We will use first step anaylsis in order to do so.
    equals = [1] * (N + 1) # ok so now the equals are all set up. I now need to set up the other side of the equation which will be a list of lists.
    equals[0] = 0
    equals[-1] = 0
    notEquals = [[0] * (N + 1) for _ in range(N + 1)] 
    for j in range(1, N):
        notEquals[j][j-1] = -(1-p)
        notEquals[j][j] = 1
        notEquals[j][j+1] = -p
    notEquals[0][0] = 1
    notEquals[N][N] = 1
    a = np.array(notEquals)
    b = np.array(equals)
    solution = np.linalg.solve(a, b)
    return solution[i]

    




def main():
    print(playGame(5, .5, 10))
    print(eX(5, .5, 10))

if __name__ == "__main__":
    main()