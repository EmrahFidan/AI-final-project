import numpy as np
import time

class IdsPuzzle:
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
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos - 3), node, 'Up', node['node depth']+1))
        if blank_tile_pos not in [0, 3, 6]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos - 1), node, 'Left', node['node depth']+1))
        if blank_tile_pos not in [2, 5, 8]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos + 1), node, 'Right', node['node depth']+1))
        if blank_tile_pos not in [6, 7, 8]:
            adjacent_nodes.append(self.build_node(self.swap_tiles(node['node state'], blank_tile_pos, blank_tile_pos + 3), node, 'Down', node['node depth']+1))
        return adjacent_nodes
    
    def iterative_deepening_search(self, max_depth, write_file):
        for depth in range(1, max_depth + 1):
            exp_n = 0
            pop_n = 0
            gen_n = 1
            max_fs = 1
            frontier = [self.build_node(self.start_node)]
            visited = set()

            while len(frontier) > 0:
                current_node = frontier.pop(0)
                pop_n += 1  

                if (current_node['node state'] == self.target_node).all():
                    return exp_n, gen_n, pop_n, max_fs, current_node['node depth'], self.find_solution_path(current_node)
                
                visited.add(tuple(current_node['node state']))

                if current_node['node depth'] < depth: 
                    adjacent_nodes = self.explore_node(current_node)
                    
                    if write_file != -1:
                        with open(write_file, 'a') as file:
                            file.write(f"Generating successors to < state = {current_node}>" + '\n')
                            file.write(f"{len(self.explore_node(current_node))} successors generated" + '\n')
                            file.write(f"Closed: {current_node}" + '\n')
                            file.write(f"Fringe: {self.explore_node(current_node)}" + '\n')
                    
                    exp_n += 1 
                    max_fs = max(max_fs, len(frontier) + len(adjacent_nodes))

                    for child in adjacent_nodes:
                        if tuple(child['node state']) not in visited:
                            gen_n += 1
                            frontier.append(child)
                    
        return exp_n, gen_n, pop_n, max_fs, -1, -1

    def track_solution_cost(self, seq):
        solution_moves = []
        solution_cost = 0

        for i in range(len(seq) - 1):
            prev = seq[i]
            curr = seq[i + 1]

            empty_tile = np.where(prev[0] == 0)[0][0]
            if (curr[-1]) != "Down":
                solution_cost += curr[0][empty_tile]
                solution_moves.append((curr[0], curr[0][empty_tile], curr[-1]))

        return solution_moves, solution_cost
        
    def print_styled(self, pop_n, exp_n, gen_n, max_fs, curr_d, cost, soln_moves, time_taken):
        print(f'Solution completed in {len(soln_moves)} steps.')
        print(f'Nodes Expanded: {exp_n}')
        print(f'Solution Depth: {curr_d}')
        print(f'Path Cost: {cost}')
        print(f'Time taken: {time_taken:.4f} seconds')

if __name__ == "__main__":
    initial_state = np.array([7, 1, 8, 0, 4, 6, 2, 3, 5])
    goal_state = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

    puzzle = IdsPuzzle(initial_state, goal_state)
    max_depth = int(input("Enter maximum depth limit: "))
    start_time = time.time()
    result = puzzle.iterative_deepening_search(max_depth, -1)
    end_time = time.time()
    exp_n, gen_n, pop_n, max_fs, soln_depth, soln_path = result
    if soln_path != -1:
        moves, cost = puzzle.track_solution_cost(soln_path)
        puzzle.print_styled(pop_n, exp_n, gen_n, max_fs, soln_depth, cost, moves, end_time - start_time)
    else: 
        print("Method could not find solution.")
