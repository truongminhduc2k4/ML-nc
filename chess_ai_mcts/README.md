# Chess AI: MCTS Implementation

A comprehensive implementation of Monte Carlo Tree Search (MCTS) for Chess AI, with comparisons against Minimax and Random agents.

## Project Structure

```
chess_ai_mcts/
├── src/
│   ├── __init__.py
│   ├── mcts.py              # MCTS core algorithm
│   ├── chess_engine.py      # Chess game logic
│   ├── agents.py            # AI agents (MCTS, Minimax, Random)
│   ├── game.py              # Game management & self-play
│   └── evaluation.py        # Performance evaluation
├── tests/
│   ├── test_mcts.py
│   ├── test_chess.py
│   └── test_agents.py
├── data/                    # Game records and statistics
├── reports/                 # Analysis and visualizations
├── requirements.txt
└── README.md
```

## Phases

### Phase 1: Preparation & Foundation ✓
- Project structure created
- Environment setup (requirements.txt)

### Phase 2: Theoretical Basis
- MCTS algorithm fundamentals
- Comparison with Minimax/AlphaBeta

### Phase 3: Basic MCTS Implementation
- Node class implementation
- Selection, Expansion, Simulation, Backpropagation

### Phase 4: Chess Integration
- python-chess library integration
- Legal move generation
- Game state tracking

### Phase 5: Self-Play
- MCTS vs MCTS matches
- Automatic game generation and recording

### Phase 6: Evaluation & Comparison
- Win rate statistics
- Performance benchmarking

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from src.game import ChessGame
from src.agents import MCTSAgent

# Create a game
game = ChessGame(white_agent=MCTSAgent(time_limit=5), 
                 black_agent=MCTSAgent(time_limit=5))

# Play
result = game.play()
print(f"Result: {result}")
```
