"""
Quick Start Guide for Chess AI MCTS Project
"""

# QUICK START GUIDE

## Installation

1. Navigate to the project directory:
```bash
cd d:\ML-nc\chess_ai_mcts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

The `main.py` script provides several test cases:

### Test 1: Basic MCTS
```bash
python main.py 1
```
Tests MCTS move selection on an initial position.

### Test 2: Single Game
```bash
python main.py 2
```
Plays one game: MCTS (White) vs Random (Black).

### Test 3: Self-play
```bash
python main.py 3
```
MCTS plays against itself for 5 games.

### Test 4: Comparisons
```bash
python main.py 4
```
Compares MCTS against Random and Minimax agents.

### Test 5: ChessState Interface
```bash
python main.py 5
```
Tests the ChessState wrapper class.

### Run All Tests
```bash
python main.py all
```

## Using the Agents

### MCTS Agent
```python
from src.agents import MCTSAgent
from src.chess_engine import ChessState

agent = MCTSAgent(time_limit=5.0)  # 5 seconds per move
state = ChessState()
move = agent.get_move(state)
```

### Random Agent
```python
from src.agents import RandomAgent

agent = RandomAgent()
move = agent.get_move(state)
```

### Minimax Agent
```python
from src.agents import MinimaxAgent

agent = MinimaxAgent(depth=3)  # 3 ply depth
move = agent.get_move(state)
```

## Playing Games

```python
from src.chess_engine import ChessGame
from src.agents import MCTSAgent, RandomAgent

white = MCTSAgent(time_limit=3.0)
black = RandomAgent()

game = ChessGame(white_agent=white, black_agent=black)
result = game.play()
print(f"Result: {result}")
```

## Evaluating Performance

```python
from src.evaluation import Evaluator
from src.agents import MCTSAgent, RandomAgent

evaluator = Evaluator()

# Self-play
mcts = MCTSAgent(time_limit=2.0)
stats = evaluator.self_play(mcts, num_games=10)

# Comparison
random = RandomAgent()
comparison = evaluator.comparison(mcts, random, num_games=5)

# Save report
evaluator.save_report()
```

## Project Structure

- `src/mcts.py` - Core MCTS algorithm with MCTSNode class
- `src/chess_engine.py` - ChessState wrapper and ChessGame manager
- `src/agents.py` - AI agents (MCTS, Random, Minimax, Human, etc.)
- `src/evaluation.py` - Game evaluation and comparison framework
- `main.py` - Example tests and quick start
- `data/` - Game records and statistics (auto-generated)
- `reports/` - Evaluation reports (auto-generated)

## Key Classes

### MCTSNode
- Represents a node in the MCTS search tree
- Stores state, parent, children, visit counts, values
- Implements UCT selection and best child calculation

### MCTS
- Implements Monte Carlo Tree Search algorithm
- 4 main phases: Selection → Expansion → Simulation → Backpropagation
- Configurable time limit or iteration limit

### ChessState
- Wraps python-chess Board for MCTS compatibility
- Provides: get_legal_moves(), apply_move(), is_terminal(), evaluate()
- Compatible with game tree search algorithms

### Agents
- MCTSAgent: Uses MCTS for move selection
- RandomAgent: Selects random legal moves
- MinimaxAgent: Uses minimax with alpha-beta pruning
- HumanAgent: Interactive human player

## Next Steps

1. Run the tests to verify everything works
2. Experiment with different time limits and depths
3. Modify the evaluation functions for better play
4. Add neural network evaluation (AlphaZero-lite)
5. Generate performance reports and visualizations

## Tips

- MCTS performance improves with more time/iterations
- RandomAgent is a weak baseline (good for testing)
- MinimaxAgent with depth=2-3 is reasonable
- Adjust exploration constant (default 1.41) to balance exploration/exploitation
- Use verbose=True to see detailed search information

## Troubleshooting

If you get "module not found" errors:
```bash
pip install -r requirements.txt
```

If games are too slow:
- Reduce MCTSAgent time_limit
- Reduce MinimaxAgent depth
- Use iteration_limit instead of time_limit

If agents make illegal moves:
- Check that get_move() is returning valid moves
- Verify ChessState.get_legal_moves() works correctly
