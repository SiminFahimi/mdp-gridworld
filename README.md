# MDP GridWorld

A simple GridWorld environment solved with **Value Iteration** and **Policy Iteration** on a Markov Decision Process (MDP), visualized using Pygame and compared using Matplotlib.

## Features

- Random walls, one terminal negative state (reward -1) named hell and one terminal positive state (reward +1) named heaven
- MDP model with stochastic transitions (intended action + sideways noise)
- Value Iteration and Policy Iteration implementations
- Time comparison between algorithms for different grid sizes and wall densities

## Installation

```
git clone https://github.com/siminfahimi/mdp-gridworld.git
cd mdp-gridworld
pip install -r requirements.txt
```

## Usage

Run the Pygame visualization:

```
python -m src.main
```

Run the time comparison plots:

```
python -m src.visualization
```

## Configuration

Key parameters (grid size, cell size, wall density, discount factor, noise) are defined in `src/config.py` and can be changed for experiments.

## Motivation

This project was implemented to gain a deeper understanding of Markov Decision Processes (MDPs)
and classical planning algorithms in Reinforcement Learning, including Value Iteration and Policy Iteration.
The focus was on understanding convergence behavior, stochastic transitions, and the effect of environment
complexity on algorithm performance.

## Results

Experiments show that Policy Iteration converges in fewer iterations,
while Value Iteration scales better for larger grid sizes.
Higher wall density increases convergence time for both methods.
