import numpy as np
from collections import deque
import time

class BfsPuzzle:
    def __init__(self, start_node, target_node):
        self.start_node = start_node
        self.target_node = target_node
        self.exp_n = 0  # Nodes expanded
        self.gen_n = 0  # Nodes generated
        self.pop_n = 0  # Nodes popped from the frontier
        self.max_fs = 0  # Maximum frontier size
        self.soln_depth = -1  # Solution depth
        self.soln_path = []  # Solution path
        self.solution_cost = 0  # Solution cost

    def build_node(self, state, parent_node=None, action=None, node_depth=0):
        # Build a new node
        return {
            'node state': state,
            'parent node': parent_node,
            'action': action,
            'node depth': node_depth,
        }

    def find_solution_path(self, node):
        # Trace back the solution path
        solution_path = []
        while node is not None:
            solution_path.append((node['node state'], node['action']))
            node = node['parent node']
        solution_path.reverse()
        return solution_path

    def swap_tiles(self, node, position1, position2):
        # Swap two tiles in the puzzle
        new_node = np.copy(node)
        temp = new_node[position1]
        new_node[position1] = new_node[position2]
        new_node[position2] = temp
        return new_node

    def explore_node(self, node):
        # Generate adjacent nodes by moving the blank tile
        blank_tile_pos = np.where(node['node state'] == 0)[0][0]
        adjacent_nodes = []

        if blank_tile_pos not in [0, 1, 2]:  # Not in the top row
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos - 3), node, 'Down', node['node depth']+1))
        if blank_tile_pos not in [0, 3, 6]:  # Not in the first column
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos - 1), node, 'Right', node['node depth']+1))
        if blank_tile_pos not in [2, 5, 8]:  # Not in the last column
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos + 1), node, 'Left', node['node depth']+1))
        if blank_tile_pos not in [6, 7, 8]:  # Not in the bottom row
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos + 3), node, 'Up', node['node depth']+1))
        return adjacent_nodes

    def breadth_first_search(self, write_file):
        # Perform BFS to find the solution
        frontier = deque([self.build_node(self.start_node)])
        visited = set()

        while frontier:
            self.max_fs = max(self.max_fs, len(frontier))
            current_node = frontier.popleft()
            self.pop_n += 1

            if (current_node['node state'] == self.target_node).all():
                self.soln_path = self.find_solution_path(current_node)
                self.soln_depth = current_node['node depth']
                return

            visited.add(tuple(current_node['node state']))

            for child in self.explore_node(current_node):
                self.gen_n += 1
                if tuple(child['node state']) not in visited:
                    frontier.append(child)
                    visited.add(tuple(child['node state']))
            self.exp_n += 1

    def track_solution_cost(self):
        # Calculate the cost of the solution path
        solution_moves = []
        solution_cost = 0

        for idx, curr in enumerate(self.soln_path):
            if idx == 0:
                continue

            prev = self.soln_path[idx - 1]
            empty_tile = np.where(prev[0] == 0)[0][0]
            moved_tile = np.where(curr[0] == 0)[0][0]

            if (curr[-1]) == "Down":
                solution_cost += prev[0][moved_tile]
                solution_moves.append((prev[0][empty_tile], "Down"))
            elif (curr[-1]) == "Up":
                solution_cost += prev[0][moved_tile]
                solution_moves.append((prev[0][empty_tile], "Up"))
            elif (curr[-1]) == "Right":
                solution_cost += prev[0][moved_tile]
                solution_moves.append((prev[0][empty_tile], "Right"))
            elif (curr[-1]) == "Left":
                solution_cost += prev[0][moved_tile]
                solution_moves.append((prev[0][empty_tile], "Left"))

        self.solution_cost = solution_cost

    def print_styled(self):
        # Print the solution path and statistics
        # print("\nSolution path:\n")
        # for i, (state, action) in enumerate(self.soln_path):
        #     if i == 0:
        #         print(f"({state[0]}, {state[1]}, {state[2]}, {state[3]}, {state[4]}, {state[5]}, {state[6]}, {state[7]}, {state[8]}) -> initial state")
        #     else:
        #         prev_state = self.soln_path[i-1][0]
        #         moved_tile = prev_state[np.where(state == 0)[0][0]]
        #         print(f"({state[0]}, {state[1]}, {state[2]}, {state[3]}, {state[4]}, {state[5]}, {state[6]}, {state[7]}, {state[8]}) -> {moved_tile} {action} ")
        
        print(f"\nSolution completed in {self.soln_depth} steps.\n")
        print(f'Nodes Expanded: {self.exp_n}\n')
        print(f'Solution Depth: {self.soln_depth}\n')
        print(f'Path Cost:  {self.solution_cost}\n')

if __name__ == "__main__":
    initial_state = (7, 1, 8, 0, 4, 6, 2, 3, 5)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    puzzle = BfsPuzzle(np.array(initial_state), np.array(goal_state))
    
    # Measure the time taken for the search
    start_time = time.time()
    puzzle.breadth_first_search(-1)
    end_time = time.time()
    
    if puzzle.soln_path:
        puzzle.track_solution_cost()
        puzzle.print_styled()
    else:
        print("No solution found.")

    # Print the time taken
    print(f"Time taken: {end_time - start_time:.4f} seconds\n")
