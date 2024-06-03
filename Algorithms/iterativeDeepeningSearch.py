from initialState import get_initial_and_goal_states
import time

def dfs(state, goal_state, depth, max_depth):
    if depth > max_depth:
        return None, None  # Return if the maximum depth is exceeded

    if state == goal_state:
        return [], 0  # Return if the goal state is reached

    zero_index = state.index(0)  # Find the position of the empty tile (0)
    row, col = zero_index // 3, zero_index % 3  # Calculate the row and column of the empty tile

    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Explore the neighboring states
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]  # Swap the empty tile with the adjacent tile
            new_state = tuple(new_state)

            path, expanded_nodes = dfs(new_state, goal_state, depth + 1, max_depth)  # Recursive call with increased depth
            if path is not None:
                return [new_state] + path, (expanded_nodes or 0) + 1  # Return the solution path and expanded nodes

    return None, 1  # Return if no solution is found

def iterative_deepening_search(initial_state, goal_state):
    max_depth = 0  # Initialize the maximum depth
    start_time = time.time()

    while True:
        solution, expanded_nodes = dfs(initial_state, goal_state, 0, max_depth)  # Depth-Limited Search
        if solution:
            end_time = time.time()
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            return solution, elapsed_time, expanded_nodes  # Return the solution details
        max_depth += 1  # Increment the maximum depth

def main():
    initial_state, goal_state = get_initial_and_goal_states()  # Get initial and goal states from the module
    solution, elapsed_time, expanded_nodes = iterative_deepening_search(initial_state, goal_state)
    
    if solution:
        print("\nSolution path:")
        for step in solution:
            print(step)
        print(f"\nSolution completed in {len(solution)} steps.\n")
        print(f"Total number of expanded nodes: {expanded_nodes}\n")
        print(f"Time taken to find solution: {elapsed_time:.5f} seconds\n")
    else:
        print("Solution not found.\n")

if __name__ == "__main__":
    main()