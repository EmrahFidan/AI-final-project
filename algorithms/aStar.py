import heapq
import unittest
import time

def get_initial_and_goal_states():
    initial_state = (7, 1, 8, 0, 4, 6, 2, 3, 5)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return initial_state, goal_state

class EightPuzzle:
    def __init__(self, initial):
        self.initial = initial
        self.goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    def actions(self, state):
        def swap(state, i, j):
            lst = list(state)
            lst[i], lst[j] = lst[j], lst[i]
            return tuple(lst)
        
        empty_index = state.index(0)
        actions = []
        if empty_index % 3 != 0:  # Can move empty tile to the left
            actions.append(swap(state, empty_index, empty_index - 1))
        if empty_index % 3 != 2:  # Can move empty tile to the right
            actions.append(swap(state, empty_index, empty_index + 1))
        if empty_index // 3 != 0:  # Can move empty tile up
            actions.append(swap(state, empty_index, empty_index - 3))
        if empty_index // 3 != 2:  # Can move empty tile down
            actions.append(swap(state, empty_index, empty_index + 3))
        return actions

    def goal_test(self, state):
        return state == self.goal

    def h(self, state):
        """Heuristic: Manhattan distance"""
        return sum(abs((val // 3) - (goal // 3)) + abs((val % 3) - (goal % 3))
                   for val, goal in ((state[i], self.goal[i]) for i in range(9)))

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, node):
        return self.path_cost < node.path_cost

def astar_search(problem):
    start_time = time.time()
    node = Node(problem.initial)
    frontier = [(problem.h(node.state), node)]  # Priority queue for nodes, ordered by heuristic value
    explored = set()
    num_expanded = 0
    while frontier:
        _, node = heapq.heappop(frontier)  # Get the node with the lowest heuristic value
        num_expanded += 1
        if problem.goal_test(node.state):
            duration = f"{time.time() - start_time:.4f}"
            solution_depth = node.depth
            solution_path_cost = node.path_cost
            print("\nSolution completed in {} steps.".format(solution_path_cost))
            print("\nNodes Expanded:", num_expanded)
            print("\nSolution Depth:", solution_depth)
            print("\nPath Cost:", solution_path_cost)
            print("\nTime taken:.", duration, "seconds")
            return node, duration  # Return the goal node and elapsed time
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node(action, node, action, node.path_cost + 1)
            if child.state not in explored and child not in (n for _, n in frontier):
                heapq.heappush(frontier, (child.path_cost + problem.h(child.state), child))
            elif child in (n for _, n in frontier):
                incumbent = next(n for _, n in frontier if n == child)
                if child.path_cost < incumbent.path_cost:
                    frontier.remove((incumbent.path_cost + problem.h(incumbent.state), incumbent))
                    heapq.heappush(frontier, (child.path_cost + problem.h(child.state), child))
    return None, 0

def solution(node):
    # Retrieve the solution path from the goal node
    actions = []
    while node.parent:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions

class TestEightPuzzle(unittest.TestCase):

    def test_eight_puzzle(self):
        initial_state, goal_state = get_initial_and_goal_states()

        problem = EightPuzzle(initial_state)
        goal_node, duration = astar_search(problem)
        
        self.assertIsNotNone(goal_node)
        solution_actions = solution(goal_node)

if __name__ == '__main__':
    unittest.main()
