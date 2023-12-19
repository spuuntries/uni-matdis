# Maze generator, I didn't make this.
import random


def generate_maze(width, height):
    # Create a grid with all walls
    maze = [["0" for x in range(width)] for y in range(height)]
    # Create a set to store the frontier cells
    frontier = set()
    # Choose a random starting cell
    start = (random.randint(0, height - 1), random.randint(0, width - 1))
    maze[start[0]][start[1]] = "1"
    # Add the neighbors of the starting cell to the frontier
    add_neighbors_to_frontier(maze, start, frontier)
    # While there are still cells in the frontier
    while frontier:
        # Choose a random cell from the frontier
        cell = random.choice(list(frontier))
        frontier.remove(cell)
        # If the current cell has exactly one visited neighbor
        if count_visited_neighbors(maze, cell) == 1:
            # Mark the current cell as visited (empty)
            maze[cell[0]][cell[1]] = "1"
            # Add the neighbors of the current cell to the frontier
            add_neighbors_to_frontier(maze, cell, frontier)
    # Set end position
    maze[start[0]][start[1]] = "1"
    maze[cell[0]][cell[1]] = "1"
    return maze


def add_neighbors_to_frontier(maze, cell, frontier):
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for dx, dy in directions:
        new_cell = (cell[0] + dx, cell[1] + dy)
        if (
            (0 <= new_cell[0] < len(maze))
            and (0 <= new_cell[1] < len(maze[0]))
            and maze[new_cell[0]][new_cell[1]] == "0"
        ):
            frontier.add(new_cell)


def count_visited_neighbors(maze, cell):
    count = 0
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for dx, dy in directions:
        new_cell = (cell[0] + dx, cell[1] + dy)
        if (
            (0 <= new_cell[0] < len(maze))
            and (0 <= new_cell[1] < len(maze[0]))
            and maze[new_cell[0]][new_cell[1]] != "0"
        ):
            count += 1
    return count


def write_maze_to_file(maze, filename):
    with open(filename, "w") as f:
        # Write the dimensions of the maze
        f.write(f"{len(maze)} {len(maze[0])}\n")
        # Write the maze
        for i, row in enumerate(maze):
            f.write("".join(row) + "\n" if i is not len(maze) - 1 else "".join(row))


# Generate and write the maze to a file
maze = generate_maze(int(input()), int(input()))
print("\n".join(map(lambda m: "".join(m), maze)))
write_maze_to_file(maze, "maze.txt")
