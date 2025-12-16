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
from .openings import OPENING_BOOK


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
    Minimax with alpha-beta pruning + Opening Book.
    
    Good baseline for comparison with MCTS.
    Uses opening book for strong early game play.
    """
    
    def __init__(self,
                 depth: int = 3,
                 name: str = "Minimax",
                 use_opening_book: bool = True):
        """
        Initialize Minimax Agent.
        
        Args:
            depth: Search depth
            name: Agent name
            use_opening_book: Use opening book for opening play
        """
        self.depth = depth
        self.name = name
        self.use_opening_book = use_opening_book
        self.nodes_evaluated = 0
        self.last_statistics = {}
        self.opening_used = False
    
    def get_move(self, state: ChessState) -> Optional[chess.Move]:
        """Get best move using minimax or opening book"""
        
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        # Try opening book first
        if self.use_opening_book:
            opening_move = self._try_opening(state)
            if opening_move:
                opening_name = OPENING_BOOK.get_opening_name(state.fen())
                self.last_statistics = {
                    'depth': 'opening_book',
                    'opening': opening_name,
                    'source': 'opening_book'
                }
                self.opening_used = True
                return opening_move
        
        # Otherwise use minimax search
        self.nodes_evaluated = 0
        self.opening_used = False
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
            'best_score': best_score,
            'source': 'minimax_search'
        }
        
        return best_move
    
    def _try_opening(self, state: ChessState) -> Optional[chess.Move]:
        """
        Try to get move from opening book.
        
        Args:
            state: Current game state
            
        Returns:
            Opening move or None if not in book
        """
        fen = state.fen()
        move_uci = OPENING_BOOK.get_move(fen)
        
        if move_uci:
            try:
                return chess.Move.from_uci(move_uci)
            except:
                return None
        return None
    
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
        Advanced position evaluation with multiple factors:
        - Material value (pieces)
        - Mobility (number of legal moves)
        - Piece positioning
        - King safety
        - Pawn structure
        
        Args:
            state: Game state
            is_white: Evaluate from white's perspective
            
        Returns:
            Evaluation score
        """
        if state.is_terminal():
            result = state.get_result()
            if result.value == 1:
                return 10000 if is_white else -10000
            elif result.value == -1:
                return -10000 if is_white else 10000
            else:
                return 0
        
        board = state.board
        
        # 1. MATERIAL EVALUATION (most important)
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.2,  # Bishop slightly better than knight
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        material_score = 0
        for piece_type in chess.PIECE_TYPES:
            white_count = len(board.pieces(piece_type, chess.WHITE))
            black_count = len(board.pieces(piece_type, chess.BLACK))
            piece_value = piece_values[piece_type]
            material_score += (white_count - black_count) * piece_value
        
        # 2. MOBILITY EVALUATION (number of legal moves)
        # More moves = more options = better position
        legal_moves = len(state.get_legal_moves())
        mobility_score = legal_moves * 0.1  # 0.1 points per move
        
        # 3. PIECE POSITIONING (basic)
        position_score = self._evaluate_position(board)
        
        # 4. KING SAFETY
        king_safety_score = self._evaluate_king_safety(board)
        
        # 5. PAWN STRUCTURE
        pawn_score = self._evaluate_pawn_structure(board)
        
        # Combine all factors
        # Weights: Material is most important (80%), then others
        total_score = (
            material_score * 0.80 +      # Material: 80%
            mobility_score * 0.05 +       # Mobility: 5%
            position_score * 0.05 +       # Position: 5%
            king_safety_score * 0.07 +    # King safety: 7%
            pawn_score * 0.03             # Pawn structure: 3%
        )
        
        return total_score if is_white else -total_score
    
    def _evaluate_position(self, board: chess.Board) -> float:
        """
        Evaluate piece positioning.
        Better positioning = higher score.
        """
        score = 0
        
        # Piece-square tables (simplified)
        piece_positions = {
            chess.PAWN: self._pawn_position_value,
            chess.KNIGHT: self._knight_position_value,
            chess.BISHOP: self._bishop_position_value,
            chess.ROOK: self._rook_position_value,
            chess.QUEEN: self._queen_position_value,
        }
        
        for piece_type, value_func in piece_positions.items():
            white_pieces = board.pieces(piece_type, chess.WHITE)
            black_pieces = board.pieces(piece_type, chess.BLACK)
            
            for square in white_pieces:
                score += value_func(square, True)
            for square in black_pieces:
                score -= value_func(square, False)
        
        return score * 0.1  # Scale down position factor
    
    def _pawn_position_value(self, square: int, is_white: bool) -> float:
        """Pawn positioning value (advanced pawns are better)"""
        rank = chess.square_rank(square)
        if is_white:
            return rank  # White: higher rank = more advanced
        else:
            return 7 - rank  # Black: lower rank (numerically) = more advanced
    
    def _knight_position_value(self, square: int, is_white: bool) -> float:
        """Knight positioning value (center is better)"""
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        center_distance = abs(file - 3.5) + abs(rank - 3.5)
        return 4 - center_distance / 2
    
    def _bishop_position_value(self, square: int, is_white: bool) -> float:
        """Bishop positioning value (long diagonals are good)"""
        return 2.0  # Simplified
    
    def _rook_position_value(self, square: int, is_white: bool) -> float:
        """Rook positioning value (open files and ranks)"""
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        # Rooks on 7th rank are strong
        if (is_white and rank == 6) or (not is_white and rank == 1):
            return 3.0
        
        return 1.5
    
    def _queen_position_value(self, square: int, is_white: bool) -> float:
        """Queen positioning value"""
        # Queen is similar to rook position value but more flexible
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        center_distance = abs(file - 3.5) + abs(rank - 3.5)
        return 5 - center_distance
    
    def _evaluate_king_safety(self, board: chess.Board) -> float:
        """
        Evaluate king safety.
        - Castled king is safer
        - King in center is dangerous (in opening/middlegame)
        """
        score = 0
        
        # White king safety
        white_king_square = board.king(chess.WHITE)
        white_castled = (
            (board.castling_rights & chess.BB_A1) == 0 or
            (board.castling_rights & chess.BB_H1) == 0
        )
        if white_castled:
            score += 1.0  # Bonus for castling
        
        # Black king safety
        black_king_square = board.king(chess.BLACK)
        black_castled = (
            (board.castling_rights & chess.BB_A8) == 0 or
            (board.castling_rights & chess.BB_H8) == 0
        )
        if black_castled:
            score -= 1.0  # Bonus for castling
        
        return score
    
    def _evaluate_pawn_structure(self, board: chess.Board) -> float:
        """
        Evaluate pawn structure.
        - Connected pawns are good
        - Doubled pawns are bad
        - Passed pawns are very good
        """
        score = 0
        
        # Very simplified pawn evaluation
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        
        # Count pawns (more pawns early is better usually)
        score += len(white_pawns) * 0.1
        score -= len(black_pawns) * 0.1
        
        # Penalize doubled pawns (simplified)
        white_files = [chess.square_file(sq) for sq in white_pawns]
        black_files = [chess.square_file(sq) for sq in black_pawns]
        
        for file in range(8):
            white_doubled = white_files.count(file) > 1
            black_doubled = black_files.count(file) > 1
            if white_doubled:
                score -= 0.5
            if black_doubled:
                score += 0.5
        
        return score
    
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
