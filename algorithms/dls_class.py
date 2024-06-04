import numpy as np
import time

class DlsPuzzle:
    def __init__(self, start_node, target_node):
        self.start_node = start_node
        self.target_node = target_node

    def build_node(self, state, parent_node=None, action=None, node_depth=0):
        return {
            'node state': state,
            'parent node': parent_node,
            'action': action,
            'node depth': node_depth,
        }
    
    def find_solution_path(self, node):
        solution_path = []
        while node is not None:
            solution_path.append((node['node state'], node['action']))
            node = node['parent node']
        solution_path.reverse()
        return solution_path
    
    def swap_tiles(self, node, position1, position2):
        new_node = np.copy(node)
        temp = new_node[position1]
        new_node[position1] = new_node[position2]
        new_node[position2] = temp
        return new_node
    
    def explore_node(self, node):
        blank_tile_pos = np.where(node['node state'] == 0)[0][0]
        adjacent_nodes = []

        if blank_tile_pos not in [0, 1, 2]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos - 3), node, 'Down', node['node depth']+1))
        if blank_tile_pos not in [0, 3, 6]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos - 1), node, 'Right', node['node depth']+1))
        if blank_tile_pos not in [2, 5, 8]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos + 1), node, 'Left', node['node depth']+1))
        if blank_tile_pos not in [6, 7, 8]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos + 3), node, 'Up', node['node depth']+1))
        return adjacent_nodes
    
    def depth_limit_search(self, max_depth):
        exp_n = 0
        gen_n = 0
        pop_n = 0
        max_fs = 0
        frontier = [self.build_node(self.start_node)]
        visited = set()

        while len(frontier) > 0:
            max_fs = max(max_fs, len(frontier))
            current_node = frontier.pop()
            pop_n += 1

            if (current_node['node state'] == self.target_node).all():
                return exp_n, gen_n, pop_n, max_fs, current_node['node depth'], self.find_solution_path(current_node)

            if current_node['node depth'] < max_depth:
                visited.add(tuple(current_node['node state']))

                for child in self.explore_node(current_node):
                    if tuple(child['node state']) not in visited:
                        gen_n += 1
                        frontier.append(child)
                exp_n += 1

        return exp_n, gen_n, pop_n, max_fs, -1, -1

    def track_solution_cost(self, seq):
        solution_moves = []
        solution_cost = 0

        end = True
        curr_idx = 0

        while end:
            curr_idx += 1
            prev_idx = curr_idx - 1

            prev = seq[prev_idx]
            curr = seq[curr_idx]

            empty_tile = np.where(prev[0] == 0)[0][0]
            if (curr[-1])  == "Down":
                solution_cost += curr[0][empty_tile]
                solution_moves.append((curr[0], curr[0][empty_tile], "Down"))
            if (curr[-1]) == "Up":
                solution_cost += curr[0][empty_tile]
                solution_moves.append((curr[0], curr[0][empty_tile], "Up"))
            if (curr[-1]) == "Right":
                solution_cost += curr[0][empty_tile]
                solution_moves.append((curr[0], curr[0][empty_tile], "Right"))
            if (curr[-1]) == "Left":
                solution_cost += curr[0][empty_tile]
                solution_moves.append((curr[0], curr[0][empty_tile], "Left"))

            if curr_idx > len(seq) - 2:
                end = False
        
        return solution_moves, solution_cost
        
    def print_styled(self, pop_n, exp_n, gen_n, max_fs, curr_d, cost, soln_moves):
        print("\nSolution completed in", len(soln_moves), "steps.")
        print("\nNodes Expanded:", exp_n)
        print("\nSolution Depth:", curr_d)
        print("\nPath Cost:", cost)
        print(f"\nTime taken: {time.time() - self.start_time:.4f} seconds\n")


if __name__ == "__main__":
    initial_state = np.array([7, 1, 8, 0, 4, 6, 2, 3, 5])
    goal_state = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

    puzzle = DlsPuzzle(initial_state, goal_state)
    puzzle.start_time = time.time()

    limits = [44, 75639]

    for depth_limit in limits:
        print(f"\nRunning Depth Limited Search with max depth limit: {depth_limit}\n")
        result = puzzle.depth_limit_search(depth_limit)
        exp_n, gen_n, pop_n, max_fs, soln_depth, soln_path = result
        if soln_path != -1:
            moves, cost = puzzle.track_solution_cost(soln_path)
            puzzle.print_styled(pop_n, exp_n, gen_n, max_fs, soln_depth, cost, moves)
        else: 
            print("Method could not find solution.")
