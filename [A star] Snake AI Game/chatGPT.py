from queue import PriorityQueue

# Define the grid size
grid_size = (10, 10)

# Define the start and goal positions
start = (0, 0)
end = (9, 9)

# Define the obstacles
obstacles = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]

# Define the directions that the algorithm can move
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Define a function to calculate the manhattan distance between two points
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Define a function to check if a position is within the grid
def within_grid(position):
    return 0 <= position[0] < grid_size[0] and 0 <= position[1] < grid_size[1]

# Define a function to check if a position is an obstacle
def is_obstacle(position):
    return position in obstacles

# Define the A* algorithm
def a_star(start, end):
    open_list = PriorityQueue()
    open_list.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not open_list.empty():
        current = open_list.get()[1]

        if current == end:
            break

        for direction in directions:
            next_position = (current[0] + direction[0], current[1] + direction[1])
            if not within_grid(next_position) or is_obstacle(next_position):
                continue
            new_cost = cost_so_far[current] + 1
            if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                cost_so_far[next_position] = new_cost
                priority = new_cost + manhattan_distance(end, next_position)
                open_list.put((priority, next_position))
                came_from[next_position] = current

    return came_from, cost_so_far

# Run the A* algorithm
came_from, cost_so_far = a_star(start, end)

# Extract the path from the came_from dictionary
current = end
path = [current]
while current != start:
    current = came_from[current]
    path.append(current)
path.reverse()

# Print the path
print(path)
