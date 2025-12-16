"""
Opening Book for Chess AI
Database of famous chess openings with move sequences
"""

import chess
from typing import Dict, List, Optional, Tuple

class OpeningBook:
    """
    Opening book with famous chess opening sequences.
    Used to improve play in early game.
    """
    
    def __init__(self):
        """Initialize opening book with popular openings"""
        # Database format: FEN -> (best_move, move_name, depth)
        self.openings = {}
        self.opening_names = {}
        self._load_openings()
    
    def _load_openings(self):
        """Load popular chess openings into database"""
        
        # Starting position
        start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        
        # 1. ITALIAN GAME - Giuoco Piano
        # 1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5
        self._add_opening("Italian Game", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", "e7e5", "1...e5", 1),
            ("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2", "b8c6", "2...Nc6", 2),
            ("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3", "f1c4", "3.Bc4", 3),
        ])
        
        # 2. SPANISH OPENING (Ruy Lopez)
        # 1.e4 e5 2.Nf3 Nc6 3.Bb5
        self._add_opening("Ruy Lopez (Spanish)", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", "e7e5", "1...e5", 1),
            ("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2", "b8c6", "2...Nc6", 2),
            ("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3", "f1b5", "3.Bb5", 3),
        ])
        
        # 3. FRENCH DEFENSE
        # 1.e4 e6 2.d4
        self._add_opening("French Defense", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkbnr/pppppppp/4p3/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "d2d4", "2.d4", 1),
        ])
        
        # 4. SICILIAN DEFENSE - Dragon Variation
        # 1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 g6
        self._add_opening("Sicilian Dragon", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1", "g1f3", "2.Nf3", 1),
            ("rnbqkbnr/pp1ppppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 2", "d2d4", "3.d4", 2),
        ])
        
        # 5. CARO-KANN DEFENSE
        # 1.e4 c6 2.d4
        self._add_opening("Caro-Kann Defense", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkbnr/pp1ppppp/2p5/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "d2d4", "2.d4", 1),
        ])
        
        # 6. ENGLISH OPENING
        # 1.c4
        self._add_opening("English Opening", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "c2c4", "1.c4", 0),
        ])
        
        # 7. QUEEN'S GAMBIT
        # 1.d4 d5 2.c4
        self._add_opening("Queen's Gambit", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "d2d4", "1.d4", 0),
            ("rnbqkbnr/pppppppp/8/3p4/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "c2c4", "2.c4", 1),
        ])
        
        # 8. INDIAN DEFENSE
        # 1.d4 Nf6 2.c4
        self._add_opening("Indian Defense", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "d2d4", "1.d4", 0),
            ("rnbqkb1r/pppppppp/5n2/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 1 1", "c2c4", "2.c4", 1),
        ])
        
        # 9. SCANDINAVIAN DEFENSE
        # 1.e4 d5 2.exd5
        self._add_opening("Scandinavian Defense", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkbnr/ppp1pppp/8/3p4/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e4d5", "2.exd5", 1),
        ])
        
        # 10. ALEKHINE'S DEFENSE
        # 1.e4 Nf6 2.e5
        self._add_opening("Alekhine's Defense", [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4", "1.e4", 0),
            ("rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 1", "e4e5", "2.e5", 1),
        ])
    
    def _add_opening(self, name: str, moves: List[Tuple[str, str, str, int]]):
        """
        Add opening to database.
        
        Args:
            name: Opening name
            moves: List of (fen, move, move_notation, move_number)
        """
        for fen, move_uci, move_notation, move_number in moves:
            self.openings[fen] = (move_uci, name, move_notation)
    
    def get_move(self, fen: str) -> Optional[str]:
        """
        Get opening move for given position.
        
        Args:
            fen: Board FEN string
            
        Returns:
            Move in UCI format, or None if not in opening book
        """
        return self.openings.get(fen, (None, None, None))[0]
    
    def get_opening_name(self, fen: str) -> Optional[str]:
        """Get name of opening for given position"""
        return self.openings.get(fen, (None, None, None))[1]
    
    def get_move_notation(self, fen: str) -> Optional[str]:
        """Get algebraic notation of move"""
        return self.openings.get(fen, (None, None, None))[2]
    
    def in_opening(self, fen: str) -> bool:
        """Check if position is in opening book"""
        return fen in self.openings
    
    def get_all_openings(self) -> Dict[str, List[str]]:
        """Get all openings by name"""
        openings_by_name = {}
        for fen, (move, name, notation) in self.openings.items():
            if name not in openings_by_name:
                openings_by_name[name] = []
            openings_by_name[name].append(f"{notation} ({move})")
        return openings_by_name
    
    def print_openings(self):
        """Print all openings in database"""
        print("\n=== CHESS OPENING BOOK ===")
        openings = {}
        for fen, (move, name, notation) in self.openings.items():
            if name not in openings:
                openings[name] = []
            openings[name].append(notation)
        
        for name in sorted(openings.keys()):
            moves = " -> ".join(openings[name])
            print(f"{name}: {moves}")


# Global opening book instance
OPENING_BOOK = OpeningBook()


if __name__ == "__main__":
    # Test opening book
    book = OpeningBook()
    book.print_openings()
    
    # Test lookup
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    move = book.get_move(start_fen)
    print(f"\nStarting position move: {move}")
    print(f"Opening: {book.get_opening_name(start_fen)}")
