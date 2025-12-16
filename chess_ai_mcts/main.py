"""
Example usage and quick tests for the Chess AI MCTS implementation.
"""

from src.chess_engine import ChessGame, ChessState
from src.agents import MCTSAgent, RandomAgent, MinimaxAgent, HumanAgent
from src.evaluation import Evaluator, GameRecorder


def test_basic_mcts():
    """Test basic MCTS functionality"""
    print("\n" + "="*50)
    print("TEST 1: Basic MCTS Move Selection")
    print("="*50)
    
    state = ChessState()
    agent = MCTSAgent(time_limit=2.0, verbose=True)
    
    move = agent.get_move(state)
    print(f"Selected move: {move}")
    print(f"Legal move count: {len(state.get_legal_moves())}")


def test_single_game():
    """Test a single game between two agents"""
    print("\n" + "="*50)
    print("TEST 2: MCTS vs Random (Single Game)")
    print("="*50)
    
    white_agent = MCTSAgent(time_limit=3.0, name="MCTS(3s)")
    black_agent = RandomAgent(name="Random")
    
    game = ChessGame(
        white_agent=white_agent,
        black_agent=black_agent,
        verbose=True
    )
    
    result = game.play()
    stats = game.get_statistics()
    
    print(f"\nResult: {result}")
    print(f"Moves: {stats['moves']}")
    print(f"Average move time - MCTS: {stats['avg_move_time']:.2f}s")


def test_self_play():
    """Test self-play with MCTS"""
    print("\n" + "="*50)
    print("TEST 3: MCTS Self-play (5 games)")
    print("="*50)
    
    agent = MCTSAgent(time_limit=1.0, name="MCTS(1s)")
    evaluator = Evaluator()
    
    stats = evaluator.self_play(agent, num_games=5, verbose=True)
    
    print(f"\nSelf-play Statistics:")
    print(f"  White win rate: {stats['white_win_rate']*100:.1f}%")
    print(f"  Average moves: {stats['avg_move_count']:.1f}")


def test_comparison():
    """Compare MCTS vs Random and MCTS vs Minimax"""
    print("\n" + "="*50)
    print("TEST 4: MCTS vs Opponents (3 games each)")
    print("="*50)
    
    mcts_agent = MCTSAgent(time_limit=2.0, name="MCTS(2s)")
    random_agent = RandomAgent(name="Random")
    minimax_agent = MinimaxAgent(depth=2, name="Minimax(d=2)")
    
    evaluator = Evaluator()
    
    # MCTS vs Random
    print("\n" + "-"*50)
    stats1 = evaluator.comparison(
        mcts_agent, random_agent, 
        num_games=3, swap_colors=False, verbose=True
    )
    
    # MCTS vs Minimax
    print("\n" + "-"*50)
    stats2 = evaluator.comparison(
        mcts_agent, minimax_agent,
        num_games=2, swap_colors=False, verbose=True
    )
    
    evaluator.print_summary()


def test_chess_state():
    """Test ChessState interface"""
    print("\n" + "="*50)
    print("TEST 5: ChessState Interface")
    print("="*50)
    
    state = ChessState()
    
    print(f"Initial state: {state}")
    print(f"Whose turn: {state.whose_turn()}")
    print(f"Legal moves: {len(state.get_legal_moves())}")
    print(f"First 5 moves: {[str(m) for m in state.get_legal_moves()[:5]]}")
    
    # Make some moves
    moves = state.get_legal_moves()
    state.apply_move(moves[0])
    print(f"\nAfter 1st move: {state}")
    print(f"Legal moves: {len(state.get_legal_moves())}")


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("CHESS AI MCTS - Test Suite")
    print("="*50)
    
    # Run selected tests based on command line args
    tests = {
        '1': test_basic_mcts,
        '2': test_single_game,
        '3': test_self_play,
        '4': test_comparison,
        '5': test_chess_state,
        'all': lambda: [test_chess_state(), test_basic_mcts(), test_single_game(), 
                       test_self_play(), test_comparison()]
    }
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        if test_name in tests:
            tests[test_name]()
        else:
            print(f"Unknown test: {test_name}")
            print(f"Available: {list(tests.keys())}")
    else:
        # Run a quick demo
        print("\nRunning quick demo (use 'python main.py <test_num>' for specific tests)")
        test_chess_state()
        test_basic_mcts()
        test_single_game()
