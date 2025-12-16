"""
Chess Game Engine Integration with python-chess

Provides wrapper around python-chess with MCTS-compatible interface.
"""

import chess
from typing import List, Tuple, Optional, Any
from copy import deepcopy
from enum import Enum


class GameResult(Enum):
    """Game result enumeration"""
    WHITE_WIN = 1
    DRAW = 0
    BLACK_WIN = -1


class ChessState:
    """
    Wrapper around chess.Board for MCTS compatibility.
    
    Provides interface:
    - get_legal_moves()
    - apply_move(move)
    - is_terminal()
    - evaluate()
    - whose_turn() (added for symmetry)
    """
    
    def __init__(self, board: Optional[chess.Board] = None):
        """Initialize ChessState"""
        if board is None:
            self.board = chess.Board()
        else:
            self.board = deepcopy(board)
    
    def get_legal_moves(self) -> List[chess.Move]:
        """Get list of legal moves"""
        return list(self.board.legal_moves)
    
    def apply_move(self, move: chess.Move) -> None:
        """Apply a move to the board"""
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            raise ValueError(f"Illegal move: {move}")
    
    def undo_move(self) -> Optional[chess.Move]:
        """Undo last move"""
        return self.board.pop() if self.board.move_stack else None
    
    def is_terminal(self) -> bool:
        """Check if game is over"""
        return self.board.is_game_over()
    
    def whose_turn(self) -> str:
        """Return whose turn it is"""
        return "white" if self.board.turn else "black"
    
    def get_result(self) -> Optional[GameResult]:
        """
        Get game result.
        
        Returns:
            GameResult or None if game not over
        """
        if not self.is_terminal():
            return None
        
        outcome = self.board.outcome()
        if outcome is None:
            return GameResult.DRAW
        
        if outcome.winner == chess.WHITE:
            return GameResult.WHITE_WIN
        elif outcome.winner == chess.BLACK:
            return GameResult.BLACK_WIN
        else:
            return GameResult.DRAW
    
    def evaluate(self, perspective: str = "white") -> float:
        """
        Evaluate position from given perspective.
        
        Args:
            perspective: "white" or "black"
            
        Returns:
            1.0 for win, 0.5 for draw, 0.0 for loss
        """
        if not self.is_terminal():
            return 0.5  # Neutral evaluation for ongoing game
        
        result = self.get_result()
        
        if perspective == "white":
            if result == GameResult.WHITE_WIN:
                return 1.0
            elif result == GameResult.DRAW:
                return 0.5
            else:
                return 0.0
        else:  # black
            if result == GameResult.BLACK_WIN:
                return 1.0
            elif result == GameResult.DRAW:
                return 0.5
            else:
                return 0.0
    
    def fen(self) -> str:
        """Get FEN representation"""
        return self.board.fen()
    
    def move_count(self) -> int:
        """Get number of moves made"""
        return len(self.board.move_stack)
    
    def move_history(self) -> List[str]:
        """Get move history in algebraic notation"""
        return [self.board.san(move) for move in self.board.move_stack]
    
    def copy(self) -> 'ChessState':
        """Create deep copy"""
        return ChessState(self.board)
    
    def __repr__(self) -> str:
        return f"ChessState(moves={self.move_count()}, turn={self.whose_turn()})"


class ChessGame:
    """
    Manages a complete game between two agents.
    """
    
    def __init__(self, 
                 white_agent: Any = None,
                 black_agent: Any = None,
                 max_moves: int = 500,
                 verbose: bool = True):
        """
        Initialize game.
        
        Args:
            white_agent: White piece agent
            black_agent: Black piece agent
            max_moves: Maximum number of moves before declaring draw
            verbose: Print game progress
        """
        self.state = ChessState()
        self.white_agent = white_agent
        self.black_agent = black_agent
        self.max_moves = max_moves
        self.verbose = verbose
        self.move_history = []
        self.move_times = []
    
    def play(self, max_move_time: float = 60.0) -> GameResult:
        """
        Play game to completion.
        
        Args:
            max_move_time: Maximum time per move (seconds)
            
        Returns:
            GameResult
        """
        import time
        
        while not self.state.is_terminal():
            # Check move limit
            if self.state.move_count() >= self.max_moves:
                if self.verbose:
                    print(f"Max moves ({self.max_moves}) reached. Game is a draw.")
                return GameResult.DRAW
            
            # Get current player
            is_white = self.state.board.turn
            agent = self.white_agent if is_white else self.black_agent
            
            if agent is None:
                raise ValueError("Agent not set")
            
            # Get move from agent
            move_start = time.time()
            move = agent.get_move(self.state)
            move_time = time.time() - move_start
            
            if move is None or move not in self.state.get_legal_moves():
                if self.verbose:
                    print(f"Invalid move from {'WHITE' if is_white else 'BLACK'}")
                return GameResult.BLACK_WIN if is_white else GameResult.WHITE_WIN
            
            # Apply move
            self.state.apply_move(move)
            self.move_history.append(move)
            self.move_times.append(move_time)
            
            if self.verbose:
                move_san = self.state.board.san(move) if self.state.board.move_stack else str(move)
                print(f"Move {self.state.move_count()}: {move_san} ({move_time:.2f}s)")
        
        result = self.state.get_result()
        if self.verbose:
            print(f"\nGame Over: {result}")
        
        return result
    
    def get_statistics(self) -> dict:
        """Get game statistics"""
        # Reconstruct move history in algebraic notation
        board_copy = chess.Board()
        move_history_san = []
        for move in self.move_history:
            try:
                move_history_san.append(board_copy.san(move))
                board_copy.push(move)
            except:
                move_history_san.append(str(move))
        
        return {
            'moves': self.state.move_count(),
            'move_history': move_history_san,
            'move_times': self.move_times,
            'avg_move_time': sum(self.move_times) / len(self.move_times) if self.move_times else 0,
            'result': self.state.get_result(),
            'fen': self.state.fen()
        }
    
    def __repr__(self) -> str:
        return f"ChessGame(moves={self.state.move_count()})"
