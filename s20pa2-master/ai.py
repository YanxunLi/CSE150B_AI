from __future__ import absolute_import, division, print_function
import copy, random, math
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.depth = current_depth
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        return self.children == []

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth): 
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth: 
            return 

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)

            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)
            for direction in MOVES:
                self.simulator.reset(*(node.state))
                if self.simulator.move(direction):
                    current_state = self.simulator.get_state()
                    child_node = Node(current_state, node.depth+1, CHANCE_PLAYER)
                    node.children.append((direction, child_node))

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            self.simulator.reset(*(node.state))
            open_tiles = self.simulator.get_open_tiles()
            current_state = self.simulator.get_state()
            for i, j in open_tiles: 
                child_node = Node(current_state, node.depth+1, MAX_PLAYER)
                child_node.state[0][i][j] = 2
                node.children.append((None, child_node))

        # TODO: build a tree for each child of this node
        for _, child_node in node.children:
            self.build_tree(child_node)

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return None, node.state[1]

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            best_val = -math.inf
            for direction, child_node in node.children:
                if self.expectimax(child_node)[1] > best_val:
                    best_val = self.expectimax(child_node)[1]
                    best_dir = direction
            return best_dir, best_val

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0
            chance = 1 / len(node.children)
            for _, child_node in node.children:
                value += self.expectimax(child_node)[1] * chance
            return None, value

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        return random.randint(0, 3)
