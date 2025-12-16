"""
Monte Carlo Tree Search (MCTS) Implementation

Core MCTS algorithm with UCT (Upper Confidence bounds applied to Trees) selection.
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from copy import deepcopy
import numpy as np


@dataclass
class MCTSNode:
    """
    A node in the MCTS tree.
    
    Attributes:
        state: Current game state
        parent: Parent node
        children: Dictionary of child nodes {action: node}
        visits: Number of times this node has been visited (N)
        value: Total reward accumulated (W)
        untried_actions: Actions that haven't been expanded yet
    """
    state: Any
    parent: Optional['MCTSNode'] = None
    children: Dict[Any, 'MCTSNode'] = field(default_factory=dict)
    visits: int = 0
    value: float = 0.0
    untried_actions: List[Any] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize untried actions from state"""
        if hasattr(self.state, 'get_legal_moves'):
            self.untried_actions = list(self.state.get_legal_moves())
    
    def is_fully_expanded(self) -> bool:
        """Check if all child nodes have been explored"""
        return len(self.untried_actions) == 0
    
    def best_child(self, exploration: float = 1.41) -> Optional['MCTSNode']:
        """
        Select the best child using UCT formula.
        
        UCT = (child.value / child.visits) + exploration * sqrt(ln(parent.visits) / child.visits)
        
        Args:
            exploration: Exploration constant (default: sqrt(2) ≈ 1.41)
            
        Returns:
            Best child node or None if no children
        """
        if not self.children:
            return None
        
        best_value = -float('inf')
        best_child_node = None
        
        for child in self.children.values():
            if child.visits == 0:
                return child  # Prefer unvisited nodes
            
            exploitation = child.value / child.visits
            exploration_term = exploration * math.sqrt(math.log(self.visits) / child.visits)
            uct_value = exploitation + exploration_term
            
            if uct_value > best_value:
                best_value = uct_value
                best_child_node = child
        
        return best_child_node
    
    def add_child(self, action: Any, state: Any) -> 'MCTSNode':
        """
        Create and add a child node.
        
        Args:
            action: The action taken to reach this state
            state: The resulting game state
            
        Returns:
            New child node
        """
        child = MCTSNode(state=state, parent=self)
        self.children[action] = child
        return child
    
    def update(self, reward: float) -> None:
        """
        Update node statistics.
        
        Args:
            reward: Reward from simulation (typically 1 for win, 0.5 for draw, 0 for loss)
        """
        self.visits += 1
        self.value += reward
    
    def ucb_value(self, exploration: float = 1.41) -> float:
        """Calculate UCB value for this node"""
        if self.visits == 0:
            return float('inf')
        
        exploitation = self.value / self.visits
        if self.parent and self.parent.visits > 0:
            exploration_term = exploration * math.sqrt(math.log(self.parent.visits) / self.visits)
        else:
            exploration_term = 0
        
        return exploitation + exploration_term


class MCTS:
    """
    Monte Carlo Tree Search algorithm for game AI.
    
    Usage:
        mcts = MCTS(game_state, time_limit=5.0)
        best_move = mcts.search()
    """
    
    def __init__(self, 
                 initial_state: Any,
                 time_limit: float = 5.0,
                 iteration_limit: Optional[int] = None,
                 exploration: float = 1.41,
                 verbose: bool = False):
        """
        Initialize MCTS.
        
        Args:
            initial_state: Initial game state
            time_limit: Maximum time for search (seconds)
            iteration_limit: Maximum number of iterations
            exploration: UCT exploration constant
            verbose: Print debug information
        """
        self.root = MCTSNode(state=initial_state)
        self.time_limit = time_limit
        self.iteration_limit = iteration_limit
        self.exploration = exploration
        self.verbose = verbose
        self.iterations = 0
    
    def search(self) -> Tuple[Any, MCTSNode]:
        """
        Run MCTS and return best action.
        
        Returns:
            Tuple of (best_action, root_node)
        """
        import time
        start_time = time.time()
        
        while True:
            if self.iteration_limit and self.iterations >= self.iteration_limit:
                break
            
            if time.time() - start_time > self.time_limit:
                break
            
            # Run one MCTS iteration
            self._mcts_iteration()
            self.iterations += 1
        
        if self.verbose:
            print(f"MCTS completed {self.iterations} iterations in {time.time() - start_time:.2f}s")
            print(f"Root visits: {self.root.visits}, children: {len(self.root.children)}")
        
        return self._best_action(), self.root
    
    def _mcts_iteration(self) -> None:
        """Execute one MCTS iteration (Selection -> Expansion -> Simulation -> Backpropagation)"""
        
        # Step 1: Selection
        node = self._select(self.root)
        
        # Step 2: Expansion
        if not node.state.is_terminal():
            node = self._expand(node)
        
        # Step 3: Simulation
        reward = self._simulate(node.state)
        
        # Step 4: Backpropagation
        self._backpropgate(node, reward)
    
    def _select(self, node: MCTSNode) -> MCTSNode:
        """
        Selection phase: traverse tree using UCT until reaching a non-fully-expanded node.
        
        Args:
            node: Current node
            
        Returns:
            Selected node
        """
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node
            
            best_child = node.best_child(self.exploration)
            if best_child is None:
                return node
            node = best_child
        
        return node
    
    def _expand(self, node: MCTSNode) -> MCTSNode:
        """
        Expansion phase: add a new child node from an untried action.
        
        Args:
            node: Node to expand
            
        Returns:
            New child node
        """
        if node.untried_actions:
            action = random.choice(node.untried_actions)
            node.untried_actions.remove(action)
            
            # Create new state by applying action
            new_state = deepcopy(node.state)
            new_state.apply_move(action)
            
            return node.add_child(action, new_state)
        
        return node
    
    def _simulate(self, state: Any) -> float:
        """
        Simulation phase: play out the game randomly from current state.
        
        Args:
            state: Game state to simulate from
            
        Returns:
            Reward: 1.0 for win, 0.5 for draw, 0.0 for loss
        """
        sim_state = deepcopy(state)
        
        while not sim_state.is_terminal():
            legal_moves = sim_state.get_legal_moves()
            if not legal_moves:
                break
            
            move = random.choice(legal_moves)
            sim_state.apply_move(move)
        
        # Evaluate final state
        return sim_state.evaluate()
    
    def _backpropgate(self, node: MCTSNode, reward: float) -> None:
        """
        Backpropagation phase: update all ancestors with simulation result.
        
        Args:
            node: Node to start backpropagation from
            reward: Reward to propagate
        """
        while node is not None:
            node.update(reward)
            node = node.parent
    
    def _best_action(self) -> Any:
        """
        Select best action from root based on visit counts.
        
        Returns:
            Best action
        """
        best_action = None
        best_visits = -1
        
        for action, child in self.root.children.items():
            if child.visits > best_visits:
                best_visits = child.visits
                best_action = action
        
        return best_action
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get MCTS search statistics"""
        return {
            'iterations': self.iterations,
            'root_visits': self.root.visits,
            'num_children': len(self.root.children),
            'tree_size': self._count_nodes(self.root),
        }
    
    @staticmethod
    def _count_nodes(node: MCTSNode) -> int:
        """Count total nodes in tree"""
        count = 1
        for child in node.children.values():
            count += MCTS._count_nodes(child)
        return count
