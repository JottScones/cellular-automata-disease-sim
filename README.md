# Cellular Automata for Disease Simulation

A disease spread simulator based on the [Kermack-McKendrick model](https://en.wikipedia.org/wiki/Kermack–McKendrick_theory) for disease spread throughout a population.

Steps to get up and running:
1. Pull this repo
2. Create a python venv and activate (`python -m env PATH/TO/REPO` & `source bin/activate`)
3. Download library dependencies using `pip install -r requirements.txt`
4. Run python app using `python disease_sim.py --infect-prob IP --recover-prob RP`
5. Watch how simulation progresses using cellular automata and animated line graph

<img width="1312" alt="image" src="https://user-images.githubusercontent.com/47277374/166073749-78a9c440-22a6-4114-aeea-ef076124d302.png">

Required arguments to use with simulator:
- `--infect-prob`: Probability that a diseased cell infects a neighbouring healthy cell (infection rate).
  - Value: [0,1]
- `--recover-prob`: Probability that a diseased cell recovers from infection.
  - Value: [0,1]

Optional arguments to use with simulator:
- `--recov-infect-prob`: Probability that a recovered cell becomes reinfected with the disease.
  - Value: [0,1]
  - default: 0
- `--infect-pop IPOP`: Percentage of population infected at the start.
  - Value: [0,1]
  - default: 0.1
- `--grid-size N`: Population size measured the number of cells along a side of the square grid.
  - Value: [1:]
  - default: 50
- `--grid-type N`: Dictates where the infected cells are initialised on the grid.
  - Value: ['random'|'central']
  - default: 'random'

The simulator logic makes use of Matplotlib and Numpy. Each cell is classified as either healthy, infected or recovered. At each timestep, 
a cell has a certain probability that it will change state (eg. infected -> recovered). This is simulated using random number generation.
