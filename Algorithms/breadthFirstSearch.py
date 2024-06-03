from initialState import get_initial_and_goal_states
from collections import deque
import time

# Import the solution algorithm for the 8-puzzle problem

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    visited = set()

    start_time = time.time()

    while queue:
        state, path = queue.popleft()  # Get the first element from the queue
        visited.add(state)  # Mark the current state as visited

        if state == goal_state:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return path, elapsed_time  # Return the solution path and elapsed time

        zero_index = state.index(0)  # Find the position of the empty tile (0)
        row, col = zero_index // 3, zero_index % 3  # Calculate the row and column of the empty tile

        # Explore the neighboring states
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]  # Swap the empty tile with the adjacent tile
                new_state = tuple(new_state)

                if new_state not in visited:
                    queue.append((new_state, path + [new_state]))  # Add the new state to the queue

def main():
    initial_state, goal_state = get_initial_and_goal_states()  # Get initial and goal states from the module
    solution, elapsed_time = bfs(initial_state, goal_state)
    
    if solution:
        print("\nSolution path:")
        for step in solution:
            print(step)
        print(f"\nSolution completed in {len(solution)} steps.\n")
        print(f"Time taken to find solution: {elapsed_time:.5f} seconds\n")
    else:
        print("Solution not found.\n")

if __name__ == "__main__":
    main()
