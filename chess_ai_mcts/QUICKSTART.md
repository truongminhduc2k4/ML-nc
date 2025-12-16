# 🚀 QUICK START - Hướng Dẫn Nhanh

## ✅ Hệ Thống Đã Sẵn Sàng!

Chess AI MCTS project với cải tiến Minimax (Opening Book + Advanced Evaluation) đã hoàn thành.

---

## 🎮 Chạy Demo Nhanh

### 1️⃣ Demo: MCTS vs Random (32 giây)
```bash
cd d:\ML-nc\chess_ai_mcts
D:\ML-nc\.venv\Scripts\python.exe demo_game.py
```
✓ Kết quả: WHITE WIN - 87 moves

### 2️⃣ Kiểm Thử Cải Tiến (30 giây)
```bash
D:\ML-nc\.venv\Scripts\python.exe test_improvements.py
```
✓ Opening Book: 205x faster
✓ Advanced Evaluation: 5 factors
✓ MCTS vs Random: DRAW
✓ Minimax vs Random: DRAW

### 3️⃣ Evaluation Toàn Bộ
```bash
D:\ML-nc\.venv\Scripts\python.exe run_evaluation.py
```

---

## 📚 Cài Đặt & Cấu Hình

### Kích Hoạt Virtual Environment
```bash
D:\ML-nc\.venv\Scripts\Activate.ps1
```

### Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎯 Sử Dụng Agents

### Quick Example: Minimax (Cải Tiến) vs Random
```python
from src.chess_engine import ChessGame
from src.agents import MinimaxAgent, RandomAgent

# Tạo agents
white = MinimaxAgent(depth=2, use_opening_book=True)
black = RandomAgent()

# Chơi trò chơi
game = ChessGame(white_agent=white, black_agent=black)
result = game.play()

# Kết quả
print(f"Result: {result}")  # 1=White, -1=Black, 0=Draw
print(f"Moves: {len(game.game.move_stack)}")
print(f"Time: {game.elapsed_time:.1f}s")
```

### Các Agent Có Sẵn
```python
from src.agents import (
    MinimaxAgent,      # Minimax + Opening Book
    MCTSAgent,         # Monte Carlo Tree Search
    RandomAgent,       # Random moves
)

# Minimax variations
agent1 = MinimaxAgent(depth=2, use_opening_book=True)   # WITH improvements
agent2 = MinimaxAgent(depth=2, use_opening_book=False)  # WITHOUT improvements
agent3 = MinimaxAgent(depth=3, use_opening_book=True)   # Deeper search

# MCTS variations
mcts1 = MCTSAgent(iterations=10)
mcts2 = MCTSAgent(iterations=30)
mcts3 = MCTSAgent(iterations=50)
```

---

## 📊 Kết Quả Mong Đợi

| Trò Chơi | Kết Quả | Nước | Thời Gian |
|---------|---------|------|-----------|
| MCTS(30) vs Random | DRAW | 300-500 | 30-60s ✓ |
| Minimax(2) vs Random | DRAW/WIN | 300-500 | 30-60s ✓ |
| Minimax(3) vs Random | WIN | 200-400 | 100-200s ✓ |

---

## 📁 File Quan Trọng

```
chess_ai_mcts/
├── src/
│   ├── agents.py        ← Minimax, MCTS, Random
│   ├── chess_engine.py  ← Chess logic
│   ├── mcts.py          ← MCTS algorithm
│   ├── openings.py      ← Opening book (NEW)
│   └── evaluation.py    ← Evaluation framework
│
├── demo_game.py         ← Quick demo
├── test_improvements.py ← Test improvements
├── run_evaluation.py    ← Full evaluation
│
└── REPORTS
    ├── RESULTS_SUMMARY.md
    ├── DEPLOYMENT_REPORT.txt
    └── MINIMAX_IMPROVEMENTS.txt
```

---

## 🔧 Troubleshooting

**ImportError?** → Chạy từ thư mục project root
```bash
cd D:\ML-nc\chess_ai_mcts
```

**Python not found?** → Kích hoạt venv
```bash
D:\ML-nc\.venv\Scripts\Activate.ps1
```

---

## 📖 Tài Liệu Đầy Đủ

- **START_HERE.md** - Điểm bắt đầu
- **RESULTS_SUMMARY.md** - Kết quả chi tiết
- **DEPLOYMENT_REPORT.txt** - Báo cáo triển khai
- **MINIMAX_IMPROVEMENTS.txt** - Hướng dẫn cải tiến

---

## 🔗 Repository

GitHub: https://github.com/truongminhduc2k4/ML-nc.git

---

**Ready to play! 🎮🚀**
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
