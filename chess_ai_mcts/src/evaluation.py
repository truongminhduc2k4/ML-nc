"""
Game Evaluation Framework

Tools for evaluating agent performance through self-play and comparisons.
"""

import json
import time
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from pathlib import Path
import statistics

from .chess_engine import ChessGame, GameResult, ChessState
from .agents import Agent, MCTSAgent, RandomAgent, MinimaxAgent


class GameRecorder:
    """Records game results and statistics"""
    
    def __init__(self, output_dir: str = "data"):
        """Initialize recorder"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.games = []
    
    def record_game(self, 
                   white_agent: Agent,
                   black_agent: Agent,
                   game: ChessGame,
                   result: GameResult) -> Dict:
        """Record a game"""
        
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'white_agent': white_agent.name,
            'black_agent': black_agent.name,
            'result': result.name,
            'moves': game.state.move_count(),
            'move_history': game.move_history,
            'move_times': game.move_times,
            'fen': game.state.fen()
        }
        
        # Add agent-specific statistics
        if hasattr(white_agent, 'last_statistics'):
            game_data['white_stats'] = white_agent.last_statistics
        if hasattr(black_agent, 'last_statistics'):
            game_data['black_stats'] = black_agent.last_statistics
        
        self.games.append(game_data)
        return game_data
    
    def save(self, filename: Optional[str] = None) -> str:
        """Save recorded games to JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"games_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.games, f, indent=2, default=str)
        
        return str(filepath)


class Evaluator:
    """Evaluates and compares agent performance"""
    
    def __init__(self, output_dir: str = "reports"):
        """Initialize evaluator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def self_play(self,
                  agent: Agent,
                  num_games: int = 10,
                  verbose: bool = True) -> Dict:
        """
        Run self-play games with one agent.
        
        Args:
            agent: Agent to play with itself
            num_games: Number of games
            verbose: Print progress
            
        Returns:
            Statistics dictionary
        """
        
        results = []
        move_counts = []
        total_time = 0
        
        print(f"\n{'='*50}")
        print(f"Self-play: {agent.name} ({num_games} games)")
        print(f"{'='*50}")
        
        for game_num in range(num_games):
            game = ChessGame(
                white_agent=agent,
                black_agent=agent,
                verbose=False
            )
            
            start = time.time()
            result = game.play()
            elapsed = time.time() - start
            
            results.append(result)
            move_counts.append(game.state.move_count())
            total_time += elapsed
            
            if verbose:
                print(f"Game {game_num+1}: {result.name} ({game.state.move_count()} moves, {elapsed:.1f}s)")
        
        stats = self._compute_statistics(
            results=results,
            move_counts=move_counts,
            agent_name=agent.name,
            total_time=total_time
        )
        
        self.results.append(stats)
        return stats
    
    def comparison(self,
                   white_agent: Agent,
                   black_agent: Agent,
                   num_games: int = 10,
                   swap_colors: bool = True,
                   verbose: bool = True) -> Dict:
        """
        Compare two agents by playing games.
        
        Args:
            white_agent: First agent
            black_agent: Second agent
            num_games: Games per color (doubled if swap_colors)
            swap_colors: If True, play with swapped colors too
            verbose: Print progress
            
        Returns:
            Comparison statistics
        """
        
        white_results = []
        black_results = []
        move_counts = []
        total_time = 0
        
        total_to_play = num_games * (2 if swap_colors else 1)
        
        print(f"\n{'='*50}")
        print(f"Comparison: {white_agent.name} vs {black_agent.name}")
        print(f"Total games: {total_to_play}")
        print(f"{'='*50}")
        
        # Play games with initial colors
        for game_num in range(num_games):
            game = ChessGame(
                white_agent=white_agent,
                black_agent=black_agent,
                verbose=False
            )
            
            start = time.time()
            result = game.play()
            elapsed = time.time() - start
            
            white_results.append(result)
            black_results.append(result)
            move_counts.append(game.state.move_count())
            total_time += elapsed
            
            if verbose:
                print(f"Game {game_num+1}: {result.name} ({game.state.move_count()} moves)")
        
        # Play with swapped colors
        if swap_colors:
            for game_num in range(num_games):
                game = ChessGame(
                    white_agent=black_agent,
                    black_agent=white_agent,
                    verbose=False
                )
                
                start = time.time()
                result = game.play()
                elapsed = time.time() - start
                
                # Flip result perspective
                flipped = GameResult(result.value * -1)
                
                black_results.append(result)
                white_results.append(flipped)
                move_counts.append(game.state.move_count())
                total_time += elapsed
                
                if verbose:
                    print(f"Game {num_games+game_num+1}: {result.name} ({game.state.move_count()} moves)")
        
        stats = {
            'comparison': True,
            'white_agent': white_agent.name,
            'black_agent': black_agent.name,
            'timestamp': datetime.now().isoformat(),
            'total_games': len(white_results),
            'total_time': total_time,
            'white_wins': sum(1 for r in white_results if r == GameResult.WHITE_WIN),
            'black_wins': sum(1 for r in white_results if r == GameResult.BLACK_WIN),
            'draws': sum(1 for r in white_results if r == GameResult.DRAW),
            'white_win_rate': sum(1 for r in white_results if r == GameResult.WHITE_WIN) / len(white_results),
            'avg_move_count': statistics.mean(move_counts),
            'std_move_count': statistics.stdev(move_counts) if len(move_counts) > 1 else 0,
        }
        
        print(f"\nResults:")
        print(f"  {white_agent.name}: {stats['white_wins']} wins ({stats['white_win_rate']*100:.1f}%)")
        print(f"  {black_agent.name}: {stats['black_wins']} wins")
        print(f"  Draws: {stats['draws']}")
        print(f"  Average moves: {stats['avg_move_count']:.1f}")
        print(f"  Total time: {stats['total_time']:.1f}s")
        
        self.results.append(stats)
        return stats
    
    @staticmethod
    def _compute_statistics(results: List[GameResult],
                           move_counts: List[int],
                           agent_name: str,
                           total_time: float) -> Dict:
        """Compute statistics from game results"""
        
        return {
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'total_games': len(results),
            'white_wins': sum(1 for r in results if r == GameResult.WHITE_WIN),
            'black_wins': sum(1 for r in results if r == GameResult.BLACK_WIN),
            'draws': sum(1 for r in results if r == GameResult.DRAW),
            'white_win_rate': sum(1 for r in results if r == GameResult.WHITE_WIN) / len(results),
            'avg_move_count': statistics.mean(move_counts),
            'std_move_count': statistics.stdev(move_counts) if len(move_counts) > 1 else 0,
            'total_time': total_time,
            'avg_time_per_game': total_time / len(results),
        }
    
    def save_report(self, filename: Optional[str] = None) -> str:
        """Save evaluation report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        return str(filepath)
    
    def print_summary(self) -> None:
        """Print summary of all evaluations"""
        print(f"\n{'='*50}")
        print("EVALUATION SUMMARY")
        print(f"{'='*50}")
        
        for result in self.results:
            if result.get('comparison'):
                print(f"\n{result['white_agent']} vs {result['black_agent']}")
                print(f"  Games: {result['total_games']}")
                print(f"  {result['white_agent']}: {result['white_win_rate']*100:.1f}%")
                print(f"  Draws: {result['draws']}")
            else:
                print(f"\n{result['agent']} self-play")
                print(f"  Games: {result['total_games']}")
                print(f"  White wins: {result['white_wins']}")
                print(f"  Black wins: {result['black_wins']}")
                print(f"  Draws: {result['draws']}")
