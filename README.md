# Diagonal sudoku solver
AI agent that solver diagonal sudoku boards, by using Depth-First Search and propagation, iterating with elimination, only choice and naked twins strategies.

## Prerequisites / how to run
Pygame is used to visualize the AI agent progress while solving the puzzle.
Actually, this visualization is a reconstruction that introduces a delay for each step, because the agent should be able to solve the puzzle almost instantaneously.
You can execute this project from a virtual environment if you have installed python3, virtualenv and git:

```
git clone https://github.com/azarrias/sudoku-solver-diagonal.git
cd sudoku-solver-diagonal
virtualenv -p python3 env && env\Scripts\activate
python -m pip install -r requirements.txt
cd src && python solution.py
```

The sudoku grid to be solved is hard-coded in main:

```
diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
```

which is a single line string representation in row-major order.

So, it is possible to change the value for sudoku_grid, as long as the value represents a valid diagonal sudoku grid (otherwise it won't be possible for the agent to solve it).
