# Candy Crush Replica

A grid-based match-three puzzle game implemented in Python. This project replicates core Candy Crush mechanics, including tile matching, cascading effects, random tile generation, and continuous game-state validation. It is designed as a clean, modular, and extensible codebase that can support future enhancements such as special candies, scoring systems, animations, or AI players.

## Features

### Core Gameplay

* **Grid-based Board**
  The game board is implemented as a 2D grid containing colored tiles represented by shapes.

* **Match-Three Detection**
  Horizontal and vertical matching logic identifies sequences of three or more identical tiles.

* **Cascading Effects**
  After matches are cleared, tiles above fall to fill empty spaces and new tiles are generated at the top. Cascades may chain together automatically.

* **Random Tile Generation**
  The algorithm ensures newly created tiles maintain randomness while avoiding impossible board states.

* **Game State Validation**
  After each move and cascade, the board is re-checked to ensure stability and to detect any new matches that should be resolved.

### Code Architecture

* **Modular Design**
  Functions are separated into logical modules responsible for board generation, matching logic, tile clearing, gravity simulation, and board refilling.

* **Deterministic Testing Support**
  The structure allows controlled test scenarios for debugging match logic and cascading behaviour.

* **No External Dependencies**
  The entire project is implemented using standard Python, making it portable and easy to run anywhere.


## How It Works

1. **Initialize Board**
   A new board is generated with random tiles while ensuring no immediate matches.

2. **Player Move**
   The user chooses a tile swap. (In a CLI version, this may be coordinate-based.)

3. **Check for Matches**
   The system detects horizontal and vertical sequences of length ≥ 3.

4. **Clear Matches**
   Matched tiles are removed and marked as empty.

5. **Apply Gravity**
   Tiles fall downward until all empty spaces are filled.

6. **Refill Board**
   New random tiles are generated at the top.

7. **Repeat Cascades**
   The game continues resolving cascades automatically until the board stabilizes.

## Installation and Usage

### Requirements

* Python 3.8 or above
* No additional libraries required

### Running the Game

```bash
python candy_crush_replica.py
```

## Example Gameplay (CLI)

```
Initial board:
A B C C A
B A A C B
C C B B A
...

Enter swap (row1 col1 row2 col2):
```

Matches and cascades automatically occur after each move.

## Future Enhancements

* Special candies (striped, wrapped, color bomb)
* Move counter and scoring system
* GUI implementation (Pygame)
* Save/load functionality
* AI solver for optimal move prediction

## Learning Objectives

* Implementing game logic using deterministic algorithms
* Designing stateful board mechanics
* Working with 2D arrays and grid-based simulations
* Applying modular software design for extensibility and clarity
