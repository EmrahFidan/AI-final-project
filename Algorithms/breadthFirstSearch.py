from initialState import get_initial_and_goal_states
from collections import deque
import time

# Yukarıdaki 8 taş problemi için çözüm algoritmasını içe aktarın

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    visited = set()

    start_time = time.time()

    while queue:
        state, path = queue.popleft()
        visited.add(state)

        if state == goal_state:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return path, elapsed_time

        zero_index = state.index(0)
        row, col = zero_index // 3, zero_index % 3

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                new_state = tuple(new_state)

                if new_state not in visited:
                    queue.append((new_state, path + [new_state]))

def main():
    initial_state, goal_state = get_initial_and_goal_states()
    solution, elapsed_time = bfs(initial_state, goal_state)
    
    if solution:
        print("\nÇözüm yolu:")
        for step in solution:
            print(step)
        print(f"\nÇözüm {len(solution)} adımda tamamlandı.\n")
        print(f"Çözüm bulma süresi: {elapsed_time:.5f} saniye\n")
    else:
        print("Çözüm bulunamadı.\n")

if __name__ == "__main__":
    main()
