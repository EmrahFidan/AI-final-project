from initialState import get_initial_and_goal_states, print_initial_and_goal_states

# Yukarıdaki 8 taş problemi için çözüm algoritmasını içe aktarın

def main():
    initial_state, goal_state = get_initial_and_goal_states()
    print_initial_and_goal_states(initial_state, goal_state)

if __name__ == "__main__":
    main()
