import heapq
import time
import pygame

# Colors for path and visited cells
VISITED_COLOR = (255, 223, 186)
PATH_COLOR = (255, 69, 0)

def ucs(grid, start, end, window, cell_size):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    open_list = []
    heapq.heappush(open_list, (0, start))
    cost = {start: 0}
    parent = {}
    visited = set()

    while open_list:
        current_cost, current = heapq.heappop(open_list)
        row, col = current

        if current == end:
            path = reconstruct_path(parent, start, end)
            visualize_path(window, path, cell_size)
            return

        if current in visited:
            continue

        visited.add(current)

        # Only draw the visited cell if it's not the start or end
        if current != start and current != end:
            pygame.draw.rect(window, VISITED_COLOR, 
                             (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.display.update()
            time.sleep(0.05)

        for dr, dc in directions:
            n_row, n_col = row + dr, col + dc

            if 0 <= n_row < len(grid) and 0 <= n_col < len(grid[0]) and grid[n_row][n_col] != 1:
                new_cost = current_cost + 1
                if (n_row, n_col) not in cost or new_cost < cost[(n_row, n_col)]:
                    cost[(n_row, n_col)] = new_cost
                    parent[(n_row, n_col)] = (row, col)
                    heapq.heappush(open_list, (new_cost, (n_row, n_col)))

    print("No path found!")
    return

def reconstruct_path(parent, start, end):
    """Reconstruct the path from the end to the start"""
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent.get(current)
    path.append(start)
    path.reverse()  # Reverse the path to go from start to end
    return path

def visualize_path(window, path, cell_size):
    """Visualize the path from start to goal"""
    for row, col in path:
        pygame.draw.rect(window, PATH_COLOR,
                         (col * cell_size, row * cell_size, cell_size, cell_size))
        pygame.display.update()
        time.sleep(0.4)
