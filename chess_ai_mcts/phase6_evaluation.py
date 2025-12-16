"""
GIAI ĐOẠN 6: ĐÁNH GIÁ & SO SÁNH
So sánh MCTS với Random và Minimax
"""

import sys
sys.path.insert(0, 'd:\\ML-nc\\chess_ai_mcts')

from src.agents import MCTSAgent, RandomAgent, MinimaxAgent
from src.evaluation import Evaluator
import json
from datetime import datetime
from pathlib import Path

def phase6_evaluation():
    """
    GIAI ĐOẠN 6: Đánh giá và so sánh
    - MCTS vs Random
    - MCTS vs Minimax
    - Thống kê: Win rate, thời gian
    """
    
    print("\n" + "="*60)
    print("GIAI ĐOẠN 6: ĐÁNH GIÁ & SO SÁNH")
    print("="*60)
    
    evaluator = Evaluator(output_dir="d:\\ML-nc\\chess_ai_mcts\\reports")
    
    # ===== TEST 1: MCTS vs Random =====
    print("\n" + "-"*60)
    print("TEST 1: MCTS vs Random")
    print("-"*60)
    
    mcts = MCTSAgent(time_limit=2.0, name="MCTS(2s)")
    random = RandomAgent(name="Random")
    
    results_vs_random = evaluator.comparison(
        white_agent=mcts,
        black_agent=random,
        num_games=3,  # 3 ván với mỗi màu
        swap_colors=True,
        verbose=True
    )
    
    # ===== TEST 2: MCTS vs Minimax =====
    print("\n" + "-"*60)
    print("TEST 2: MCTS vs Minimax")
    print("-"*60)
    
    minimax = MinimaxAgent(depth=2, name="Minimax(d=2)")
    
    results_vs_minimax = evaluator.comparison(
        white_agent=mcts,
        black_agent=minimax,
        num_games=2,  # Minimax chậm hơn
        swap_colors=True,
        verbose=True
    )
    
    # ===== TEST 3: Random vs Minimax =====
    print("\n" + "-"*60)
    print("TEST 3: Random vs Minimax")
    print("-"*60)
    
    results_random_vs_minimax = evaluator.comparison(
        white_agent=random,
        black_agent=minimax,
        num_games=2,
        swap_colors=False,
        verbose=True
    )
    
    # ===== In tóm tắt =====
    print("\n" + "="*60)
    print("TÓMS TẮT KẾT QUẢ")
    print("="*60)
    
    evaluator.print_summary()
    
    # ===== Lưu báo cáo =====
    report_file = evaluator.save_report(filename="phase6_evaluation.json")
    print(f"\nLưu báo cáo: {report_file}")
    
    # ===== Tạo bảng so sánh =====
    comparison_table = {
        'timestamp': datetime.now().isoformat(),
        'evaluations': [
            {
                'name': 'MCTS vs Random',
                'mcts_win_rate': results_vs_random['white_win_rate'],
                'random_win_rate': results_vs_random['black_wins'] / results_vs_random['total_games'],
                'draws': results_vs_random['draws'],
                'total_games': results_vs_random['total_games']
            },
            {
                'name': 'MCTS vs Minimax',
                'mcts_win_rate': results_vs_minimax['white_win_rate'],
                'minimax_win_rate': results_vs_minimax['black_wins'] / results_vs_minimax['total_games'],
                'draws': results_vs_minimax['draws'],
                'total_games': results_vs_minimax['total_games']
            }
        ]
    }
    
    print("\n" + "="*60)
    print("BẢNG SO SÁNH WIN RATE")
    print("="*60)
    print(f"\n{'Agent':<20} {'Win Rate':<15} {'Games':<10}")
    print("-"*45)
    print(f"{'MCTS vs Random':<20}")
    print(f"  MCTS{'':<16} {results_vs_random['white_win_rate']*100:>6.1f}%{'':<8} {results_vs_random['total_games']}")
    print(f"  Random{'':<14} {(results_vs_random['black_wins']/results_vs_random['total_games'])*100:>6.1f}%")
    
    print(f"\n{'MCTS vs Minimax':<20}")
    print(f"  MCTS{'':<16} {results_vs_minimax['white_win_rate']*100:>6.1f}%{'':<8} {results_vs_minimax['total_games']}")
    print(f"  Minimax{'':<13} {(results_vs_minimax['black_wins']/results_vs_minimax['total_games'])*100:>6.1f}%")
    
    print(f"\n{'Random vs Minimax':<20}")
    print(f"  Random{'':<14} {(results_random_vs_minimax['white_win_rate'])*100:>6.1f}%{'':<8} {results_random_vs_minimax['total_games']}")
    print(f"  Minimax{'':<13} {(results_random_vs_minimax['black_wins']/results_random_vs_minimax['total_games'])*100:>6.1f}%")
    
    return {
        'mcts_vs_random': results_vs_random,
        'mcts_vs_minimax': results_vs_minimax,
        'random_vs_minimax': results_random_vs_minimax
    }


if __name__ == "__main__":
    results = phase6_evaluation()
    
    print(f"\n" + "="*60)
    print("GIAI ĐOẠN 6 HOÀN THÀNH")
    print("="*60)
    print("\nKỳ lực chính:")
    print(f"  - MCTS thắng Random: {results['mcts_vs_random']['white_win_rate']*100:.1f}%")
    print(f"  - MCTS vs Minimax: {results['mcts_vs_minimax']['white_win_rate']*100:.1f}% win (MCTS)")
    print(f"  - Random vs Minimax: Minimax chiếm ưu thế")
    print("\nBáo cáo chi tiết: reports/phase6_evaluation.json")
