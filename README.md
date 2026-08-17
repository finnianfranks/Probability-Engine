# Probability-Engine
A python project dedicated to the simulation of different probabilistic scenarios that allows for the application of probability theory and analysis. This includes and is not limited to calculating expected value mathematically, deriving expected value through simulation such as monte-carlo, and determining the probability of an event that is completely parametized. In the future I would like to apply deeper probability theory concepts such as markov-chains and code some of the project files in C++. \
\
For more information on some of the problems solved here visit the corrosponding substack with article proofs and walkthroughs attache below: \
[Substack](https://substack.com/@finnianfranks)




# kHeads.py:
In this file we begin by taking a coin and mathematically finding the average number of flips it would take to see k heads in a row. We do this using NumPy and utilizing the linear algebra portion of the library to set up the reccurence relation in order to find such an expected value. This offers insight in converting the math which can feel intuitive, to code that has to work for every case and therefore must follow some sort of pattern/predictable sequence. We then extend the project further by allowing the coin to be unfair--so weighting the probability of heads different from tails. After this we then derive the expected value through simulation to see if our mathematical and simulated answer corrospond. We find that they do and following this we print a graph of the simulation in order to see the visualization of our experiment.
Next steps...
Next I look to calculate the probability that it takes X number of flips in order to get K heads in a row. For example, "the probability that it takes 5 flips to get 3 heads in a row on coin that favors heads 2/3's of the time". Stay tuned with the project to see updates about this.

# gamblersRuin.py:
In this file we look at an important problem of probability known as the gamblers ruin problem. The problem has a complicated solution which requires a longer proof and is provided on the substack. In the file to calculate the probability that we beat the game, starting at i, we use the final formula derived from the proof. After that we take a look at the average amount of rounds the game must be played in order to be completed--that is the player reaches 0 or reaches N. We do this using the same type of first step analysis and linalg as in kheads.py. After that we calculate the probability that the game ends in t rounds which sort of extends what we were examining with the expected value calculation before hand. after this we run our experiment under a montecarlo simulation to verify our expected value calculation. We then extend the project further by essentially eliminating the possibility of losing the game and examining the new game under that constraint. In order to do this we use a decent amount of conditional probability and condition away the games in which we lose which allows us to practice some more abstract thinking and manipulation of the base equations. Finally we do Monte-Carlo for this calculation as well. This concludes the gamblers ruin coding analysis unless another interesting route to take the question pops into mind.

# amoeba.py:
Next I will examine the famous amoeba question since it appears to be recursive like. We will see if that actually comes through then in the implementation.

# Conclusion
I am marking the conclusion of this project at 5 worthwhile probability questions. After that I will re-evaluate wether it is worth doing more in this framework.