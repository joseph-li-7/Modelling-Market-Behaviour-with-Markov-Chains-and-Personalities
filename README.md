# Modelling Market Behaviour with Markov Chains and Personalities

This project applies mathematics and programming to simulate and explore market
trends influenced by personality-driven investor behaviours. It uses Markov chains and
probabilistic modelling to visualize and analyze how different types of investors react to
changing market conditions.

The primary goal of this project is to simulate an oversimplified version of the stock
market and model how people with different risk tolerances (e.g., cautious, greedy, average,
risk-taking) make decisions in uncertain market conditions. The simulation aims to represent not
just complete randomness, but also some human psychology under uncertainty, making it a mix
of behavioural economics and mathematics.
At the core of this simulation is the Markov chain, a mathematical system that transitions
from one state to another according to certain probabilities. In our case, the “states” represent
the market's condition: up, down, flat, boom, and crash. A Markov chain assumes that the next
state depends only on the current state (not the full history), which is ideal for modelling market
fluctuations over time.
Each market state has its own set of transition probabilities defined in a Markov
transition matrix, which reflects the likelihood of the market moving from one state to another.
We modify these probabilities dynamically based on investor activity, adding a feedback loop
that connects participation to market behaviour - a simple version of supply and demand
psychology.
Additionally, every investor is programmed with a personality that affects whether they
choose to stay in or exit the market. These decisions are probabilistic and vary depending on
the current market state.
