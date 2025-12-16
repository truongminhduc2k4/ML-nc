"""
Test game: MCTS vs Random
Quick demo of Phase 5 & 6
"""

import sys
sys.path.insert(0, 'd:\\ML-nc\\chess_ai_mcts')

from src.chess_engine import ChessGame, GameResult
from src.agents import MCTSAgent, RandomAgent
import time

print("="*70)
print("  MCTS vs RANDOM - DEMO GAME")
print("="*70)

# Create agents
print("\n[1] Creating agents...")
mcts = MCTSAgent(iteration_limit=30, name="MCTS(30)")
random_agent = RandomAgent(name="Random")
print("    - MCTS agent created (30 iterations per move)")
print("    - Random agent created")

# Play game
print("\n[2] Playing game...")
print("    White: MCTS")
print("    Black: Random")
print("-"*70)

game = ChessGame(white_agent=mcts, black_agent=random_agent, verbose=False)

start = time.time()
result = game.play()
elapsed = time.time() - start

stats = game.get_statistics()

print(f"\n[3] Game completed!")
print("    Result: " + ("WHITE (MCTS) WIN" if result == GameResult.WHITE_WIN else 
                       ("BLACK (RANDOM) WIN" if result == GameResult.BLACK_WIN else "DRAW")))
print(f"    Moves: {stats['moves']}")
print(f"    Time: {elapsed:.1f}s")
print(f"    Average move time: {stats['avg_move_time']:.2f}s")

# Show some moves
print("\n[4] Move history (first 10):")
moves = stats['move_history'][:10]
for i, move in enumerate(moves):
    print(f"    {i+1}. {move}", end="  ")
    if (i+1) % 4 == 0:
        print()

print("\n\n[DEMO COMPLETE]")
