"""
GIAI ĐOẠN 5: SELF-PLAY
Script để MCTS chơi với chính nó
"""

import sys
sys.path.insert(0, 'd:\\ML-nc\\chess_ai_mcts')

from src.chess_engine import ChessGame, GameResult
from src.agents import MCTSAgent, RandomAgent
from src.evaluation import Evaluator, GameRecorder
import json
from pathlib import Path

def phase5_selfplay():
    """
    GIAI ĐOẠN 5: MCTS chơi với chính nó
    Chạy nhiều ván tự động và lưu kết quả
    """
    
    print("\n" + "="*60)
    print("GIAI ĐOẠN 5: SELF-PLAY - MCTS chơi với chính nó")
    print("="*60)
    
    # Cấu hình
    num_games = 5  # Số ván (bạn có thể tăng lên)
    time_per_move = 1.0  # Thời gian per nước (giây)
    
    # Tạo agent
    mcts_agent = MCTSAgent(
        time_limit=time_per_move,
        name="MCTS(1s)"
    )
    
    # Tạo evaluator để theo dõi thống kê
    evaluator = Evaluator(output_dir="d:\\ML-nc\\chess_ai_mcts\\data")
    recorder = GameRecorder(output_dir="d:\\ML-nc\\chess_ai_mcts\\data")
    
    print(f"\nChạy {num_games} ván self-play...")
    print(f"Thời gian per nước: {time_per_move}s")
    print(f"Tổng thời gian dự kiến: ~{num_games * 40 * time_per_move:.0f}s")
    
    results = []
    move_histories = []
    
    for game_num in range(num_games):
        print(f"\n--- Ván {game_num + 1}/{num_games} ---")
        
        game = ChessGame(
            white_agent=mcts_agent,
            black_agent=mcts_agent,
            verbose=False
        )
        
        result = game.play()
        results.append(result)
        move_histories.append(game.state.move_count())
        
        # Lưu kết quả
        game_data = recorder.record_game(mcts_agent, mcts_agent, game, result)
        
        # In thống kê
        print(f"Kết quả: {result.name}")
        print(f"Tổng nước: {game.state.move_count()}")
        print(f"Nước của White: {[move for i, move in enumerate(game.state.board.move_stack) if i % 2 == 0][:3]}...")
        print(f"Nước của Black: {[move for i, move in enumerate(game.state.board.move_stack) if i % 2 == 1][:3]}...")
    
    # Tính toán thống kê
    white_wins = sum(1 for r in results if r == GameResult.WHITE_WIN)
    black_wins = sum(1 for r in results if r == GameResult.BLACK_WIN)
    draws = sum(1 for r in results if r == GameResult.DRAW)
    
    print(f"\n" + "="*60)
    print("THỐNG KÊ SELF-PLAY")
    print("="*60)
    print(f"Tổng ván: {num_games}")
    print(f"White wins: {white_wins} ({white_wins*100/num_games:.1f}%)")
    print(f"Black wins: {black_wins} ({black_wins*100/num_games:.1f}%)")
    print(f"Draws: {draws} ({draws*100/num_games:.1f}%)")
    print(f"Trung bình nước/ván: {sum(move_histories)/len(move_histories):.1f}")
    
    # Lưu file
    filepath = recorder.save(filename="phase5_selfplay.json")
    print(f"\nLưu dữ liệu: {filepath}")
    
    return {
        'white_wins': white_wins,
        'black_wins': black_wins,
        'draws': draws,
        'avg_moves': sum(move_histories) / len(move_histories),
        'total_games': num_games
    }


if __name__ == "__main__":
    stats = phase5_selfplay()
    
    print(f"\n" + "="*60)
    print("GIAI ĐOẠN 5 HOÀN THÀNH")
    print("="*60)
    print("\nKết quả chính:")
    print(f"  - White: {stats['white_wins']} ({stats['white_wins']*100/stats['total_games']:.1f}%)")
    print(f"  - Black: {stats['black_wins']} ({stats['black_wins']*100/stats['total_games']:.1f}%)")
    print(f"  - Draws: {stats['draws']} ({stats['draws']*100/stats['total_games']:.1f}%)")
    print(f"  - Avg moves/game: {stats['avg_moves']:.1f}")
