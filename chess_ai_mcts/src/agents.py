"""
AI Agents: MCTS, Minimax, and Random

Different agents for playing chess with various strategies.
"""

import random
import chess
from typing import Optional, List, Tuple
from abc import ABC, abstractmethod
import time

from .mcts import MCTS, MCTSNode
from .chess_engine import ChessState


class Agent(ABC):
    """Base agent class"""
    
    @abstractmethod
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get the next move from current state"""
        pass


class MCTSAgent(Agent):
    """
    MCTS-based chess AI.
    
    Usage:
        agent = MCTSAgent(time_limit=5.0)
        move = agent.get_move(chess_state)
    """
    
    def __init__(self, 
                 time_limit: float = 5.0,
                 iteration_limit: Optional[int] = None,
                 exploration: float = 1.41,
                 verbose: bool = False,
                 name: str = "MCTS"):
        """
        Initialize MCTS Agent.
        
        Args:
            time_limit: Time budget per move (seconds)
            iteration_limit: Iteration limit (alternative to time)
            exploration: UCT exploration constant
            verbose: Print debug info
            name: Agent name
        """
        self.time_limit = time_limit
        self.iteration_limit = iteration_limit
        self.exploration = exploration
        self.verbose = verbose
        self.name = name
        self.last_statistics = {}
    
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get best move using MCTS"""
        
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        # Run MCTS search
        mcts = MCTS(
            initial_state=state,
            time_limit=self.time_limit,
            iteration_limit=self.iteration_limit,
            exploration=self.exploration,
            verbose=self.verbose
        )
        
        best_move, root = mcts.search()
        self.last_statistics = mcts.get_statistics()
        
        if self.verbose:
            print(f"{self.name} Statistics: {self.last_statistics}")
        
        return best_move
    
    def get_statistics(self) -> dict:
        """Get last search statistics"""
        return self.last_statistics


class RandomAgent(Agent):
    """
    Random move selection agent.
    
    Useful baseline for comparison.
    """
    
    def __init__(self, name: str = "Random"):
        """
        Initialize Random Agent.
        
        Args:
            name: Agent name
        """
        self.name = name
    
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get random legal move"""
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None
        return random.choice(legal_moves)


class MinimaxAgent(Agent):
    """
    Minimax with alpha-beta pruning.
    
    Good baseline for comparison with MCTS.
    """
    
    def __init__(self,
                 depth: int = 3,
                 name: str = "Minimax"):
        """
        Initialize Minimax Agent.
        
        Args:
            depth: Search depth
            name: Agent name
        """
        self.depth = depth
        self.name = name
        self.nodes_evaluated = 0
        self.last_statistics = {}
    
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get best move using minimax"""
        
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        self.nodes_evaluated = 0
        best_move = None
        best_score = -float('inf')
        
        for move in legal_moves:
            state_copy = state.copy()
            state_copy.apply_move(move)
            
            score = self._minimax(state_copy, self.depth - 1, -float('inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        self.last_statistics = {
            'depth': self.depth,
            'nodes_evaluated': self.nodes_evaluated,
            'best_score': best_score
        }
        
        return best_move
    
    def _minimax(self, state: ChessState, depth: int, alpha: float, beta: float, 
                 is_maximizing: bool) -> float:
        """
        Minimax with alpha-beta pruning.
        
        Args:
            state: Current game state
            depth: Remaining depth
            alpha: Alpha value
            beta: Beta value
            is_maximizing: Whether maximizing or minimizing
            
        Returns:
            Score
        """
        self.nodes_evaluated += 1
        
        # Terminal node or depth limit
        if state.is_terminal() or depth == 0:
            return self._evaluate(state, is_maximizing)
        
        legal_moves = state.get_legal_moves()
        
        if is_maximizing:
            max_eval = -float('inf')
            for move in legal_moves:
                state_copy = state.copy()
                state_copy.apply_move(move)
                eval_score = self._minimax(state_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                state_copy = state.copy()
                state_copy.apply_move(move)
                eval_score = self._minimax(state_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def _evaluate(self, state: ChessState, is_white: bool) -> float:
        """
        Evaluate position.
        
        Simple evaluation: piece values + mobility
        """
        if state.is_terminal():
            result = state.get_result()
            if result.value == 1:
                return 10000 if is_white else -10000
            elif result.value == -1:
                return -10000 if is_white else 10000
            else:
                return 0
        
        # Material evaluation
        board = state.board
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        score = 0
        for piece_type in chess.PIECE_TYPES:
            white_count = len(board.pieces(piece_type, chess.WHITE))
            black_count = len(board.pieces(piece_type, chess.BLACK))
            piece_value = piece_values[piece_type]
            score += (white_count - black_count) * piece_value
        
        # Mobility bonus
        legal_moves = len(state.get_legal_moves())
        score += legal_moves * 0.1
        
        return score if is_white else -score
    
    def get_statistics(self) -> dict:
        """Get last search statistics"""
        return self.last_statistics


class HumanAgent(Agent):
    """
    Interactive human player agent.
    """
    
    def __init__(self, name: str = "Human"):
        """Initialize Human Agent"""
        self.name = name
    
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get move from user input"""
        
        print("\nLegal moves:")
        legal_moves = state.get_legal_moves()
        
        for i, move in enumerate(legal_moves):
            move_san = state.board.san(move)
            print(f"  {i+1}. {move_san}")
        
        while True:
            try:
                choice = input(f"\nEnter move (1-{len(legal_moves)}) or move in UCI format: ").strip()
                
                # Try as index
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(legal_moves):
                        return legal_moves[idx]
                except ValueError:
                    pass
                
                # Try as UCI format
                try:
                    move = chess.Move.from_uci(choice)
                    if move in legal_moves:
                        return move
                except:
                    pass
                
                print("Invalid input. Try again.")
            
            except KeyboardInterrupt:
                return None


class AlternatingAgent(Agent):
    """
    Agent that alternates between multiple agents.
    
    Useful for testing different agent combinations.
    """
    
    def __init__(self, white_agent: Agent, black_agent: Agent):
        """
        Initialize Alternating Agent.
        
        Args:
            white_agent: Agent for white pieces
            black_agent: Agent for black pieces
        """
        self.white_agent = white_agent
        self.black_agent = black_agent
        self.name = f"{white_agent.name} vs {black_agent.name}"
    
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get move from appropriate agent"""
        is_white = state.board.turn
        agent = self.white_agent if is_white else self.black_agent
        return agent.get_move(state)
