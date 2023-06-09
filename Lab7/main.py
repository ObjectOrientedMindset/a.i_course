from collections import defaultdict
from copy import deepcopy

import numpy as np


def choose_heuristic() -> str:
    """
    Gets the user to select either the Manhattan or Hamming Distance heuristic.

    Returns:
        The type of heuristic to use for solving the 8-puzzle problem.
    """
    heuristic_input = ""
    while heuristic_input not in ("m", "h"):
        heuristic_input = input(
            "\nThe Manhattan Distance heuristic is based on number of squares "
            "between itself and the goal position, whereas the Hamming "
            "Distance heuristic is based on total number of misplaced tiles.\n"
            "Choose between the Manhattan Distance heuristic (m), "
            "the Hamming Distance heuristic (h), the Euclidean Distance (e) \n").lower()
        if heuristic_input not in ("m", "h", "e"):
            print("Invalid input! Please enter 'm' for the Manhattan Distance "
                  "heuristic, 'h' for the Hamming Distance heuristic"
                  "or 'e' for Euclidean heuristic")
        elif heuristic_input == "m":
            return "Manhattan"
        elif heuristic_input == "e":
            return "Euclidean"
        else:
            return "Hamming"


def choose_states():
    """
    Creates the start and goal states for the 8-puzzle problem.

    Returns:
        The start state and desired goal state of the board.
    """
    start = np.array([5, 0, 8, 4, 2, 1, 7, 3, 6])
    goal = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])
    return start, goal


def is_solvable(start) -> bool:
    """
    Checks whether the 8-puzzle problem is solvable based on inversions.

    Args:
        start: The start state of the board input by the user.

    Returns:
        Whether the 8-puzzle problem is solvable.
    """
    k = start[start != 0]
    num_inversions = sum(
        len(np.array(np.where(k[i + 1:] < k[i])).reshape(-1)) for i in
        range(len(k) - 1))
    return num_inversions % 2 == 0


def assign_coordinates(board):
    """
    Assigns coordinates to each digit to calculate the Manhattan Distance.

    Args:
        board: The state of the board.

    Returns:
        Coordinates to calculate the Manhattan Distance.
    """
    coordinate = np.array(range(9))
    # Gets the index of each value, where the board is the array of values.
    for x, y in enumerate(board):
        coordinate[y] = x
    return coordinate


def calculate_heuristic(heuristic, current, goal) -> int:
    """
    Calculates h(n) using either the Manhattan or Hamming Distance heuristic.

    Args:
        heuristic: The heuristic algorithm chosen by the user.
        current: The current state of the board.
        goal: The desired state of the board.

    Returns:
        The value of h(n) according to the heuristic algorithm used.
    """
    if heuristic == "Manhattan":
        current_c = assign_coordinates(current)
        goal_c = assign_coordinates(goal)
        result = manhattan_heuristic(current_c, goal_c)
    elif heuristic == "Euclidean":
        current_coordinate = assign_coordinates(current)
        goal_coordinate = assign_coordinates(goal)
        result = calc_euclidean_dist(current_coordinate, goal_coordinate)
    else:
        result = hamming_heuristic(current, goal)
    return result

def find_in_sublists(val, lst):
    """
    Helper function used in Node.expand. Find value in list of lists.
    
    Returns:
    A tuple containing the indices of val in lst.
    """
    for i, sub_list in enumerate(lst):
        try:
            j = sub_list.index(val)
        except ValueError:
            continue
        return i, j
            
    return None, None


def manhattan_heuristic(current, goal) -> int:
    """
    Performs the Manhattan Distance heuristic.
    
    Returns:
        Minimum number of moves to reach the goal state from the current state.
    """
    manhattan = abs(current // 3 - goal // 3) + abs(current % 3 - goal % 3)
    return sum(manhattan[1:])

def calc_euclidean_dist(current, goal):
    sum_sq = np.sum(np.square(current - goal))
    
    return np.sqrt(sum_sq)



def hamming_heuristic(current, goal) -> int:
    """
    Performs the Hamming Distance heuristic.

    Args:
        current: The current state of the board.
        goal: The desired state of the board.

    Returns:
        Number of misplaced tiles on the current state of the board.
    """
    return np.sum(current != goal) - 1


def search(heuristic, start, goal):
    """
    Performs the A* search on the 8-puzzle problem.

    Args:
        heuristic: Algorithm used to estimate the cost of reaching the goal.
        start: The start state of the board input by the user.
        goal: The desired state of the board.

    Returns:
        The states of the board, and how many states were explored.
    """
    (goal, moves, previous_boards, priority, priority_queue_type,
     state, state_type) = setup_search(heuristic, start, goal)

    # Searches until the goal state is found.
    while True:
        # Sorts the priority queue according to the total cost.
        priority = np.sort(priority, kind="mergesort",
                           order=["f_function", "position"])
        # Explores the first node from the priority queue, and removes it from
        # the priority queue.
        position = priority[0][0]
        priority = np.delete(priority, 0, 0)
        board = state[position][0]
        g_function = state[position][2] + 1
        location = int(np.where(board == 0)[0])

        # Checks all possible moves which can be made from the current state.
        for move in moves:
            # Performs the move if it is valid.
            if location not in move["position"]:
                # Copies the current state of the board.
                new_state = deepcopy(board)
                # Performs the move.
                delta_location = location + move["delta"]
                new_state[location], new_state[delta_location] = \
                    new_state[delta_location], new_state[location]

                # Ensures that boards aren't repeatedly processed.
                if previous_boards[tuple(new_state)]:
                    continue
                previous_boards[tuple(new_state)] = True

                # Calculates the estimated cost of reaching the goal state from
                # the current state of the board using the chosen heuristic.
                h_function = calculate_heuristic(heuristic, new_state, goal)
                # Generates and adds the new board state.
                new_state_details = np.array(
                    [(new_state, position, g_function, h_function)],
                    dtype=state_type)
                state = np.append(state, new_state_details, 0)
                # Calculates the total cost, and adds the new state to the
                # priority queue.
                f_function = g_function + h_function
                new_state_details = np.array([(len(state) - 1, f_function)],
                                             dtype=priority_queue_type)
                priority = np.append(priority, new_state_details, 0)

                # Stops the search if the goal state has been achieved.
                if np.array_equal(new_state, goal):
                    print("\nGoal state has been achieved with the "
                          "following steps:\n")
                    return state, len(priority)


def setup_search(heuristic, start, goal):
    """
    Sets up the valid moves, priority queue, and state tracking for the search.

    Args:
        heuristic: Algorithm used to estimate the cost of reaching the goal.
        start: The start state of the board input by the user.
        goal: The desired state of the board.

    Returns:
        A record of valid moves, priority queue, and states.
    """
    # Sets the rules for the moves a tile can make, and when it can do them.
    moves = np.array([("up", [0, 1, 2], -3),
                      ("down", [6, 7, 8], 3),
                      ("left", [0, 3, 6], -1),
                      ("right", [2, 5, 8], 1)],
                     dtype=[("move", str, 1),
                            ("position", list),
                            ("delta", int)])
    # Creates the data structures for board state and priority queue.
    state_type = [("board", list),
                  ("parent", int),
                  ("g_function", int),
                  ("h_function", int)]
    priority_queue_type = [("position", int),
                           ("f_function", int)]
    # Creates a dictionary to keep track of boards which have been processed.
    previous_boards = defaultdict(bool)
    # Processes the start position of the board.
    h_function = calculate_heuristic(heuristic, start, goal)
    state = np.array([(start, -1, 0, h_function)],
                     dtype=state_type)
    priority = np.array([(0, h_function)], dtype=priority_queue_type)

    return (goal, moves, previous_boards, priority, priority_queue_type,
            state, state_type)


def generate_steps(state):
    """
    Generates the step-by-step solution to reach the goal state.

    Args:
        state: A record of the state of each 3x3 board.

    Returns:
        The state of the 3x3 board after each step to the goal state.
    """
    # Creates an array of integers to display each board state.
    optimal = np.array([], int)
    last = len(state) - 1
    while last != -1:
        optimal = np.insert(optimal, 0, state[last]["board"])
        last = int(state[last]["parent"])
    return optimal.reshape(-1, 3, 3)


def main():
    """
    Runs the A* algorithm to solve the 8-puzzle problem.
    """
    heuristic = choose_heuristic()
    start, goal = choose_states()
    print(("{} Distance heuristic chosen.\nStart State: {}"
           "\nGoal State: {}").format(heuristic, start, goal))

    # Stops the program if the 8-puzzle is unsolvable.
    if is_solvable(start) is False:
        print("\nThe 8-puzzle problem is unsolvable with this start state!")
        return

    state, explored = search(heuristic, start, goal)
    optimal = generate_steps(state)
    print(("{}\n\nTotal States Generated: {}\nTotal States Explored: {}"
           "\nNumber of Steps for Optimal Solution: {}").format(
        optimal, len(state), len(state) - explored, len(optimal) - 1))


if __name__ == "__main__":
    main()
