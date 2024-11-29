import pygame
import time
from collections import deque

# Colors for visualization
SEARCH_COLOR = (255, 223, 186)  # cells being searched
PATH_COLOR = (255, 69, 0)    # the found path

# BFS Algorithm
def bfs(grid, start, end, window, cell_size):
    queue = deque([start])
    visited = set([start])
    parent = {}
    path_found = False

    while queue:
        current = queue.popleft()
        row, col = current

        if current == end:
            path_found = True
            break

        # Visualize the search process
        if current != start and current != end:
            pygame.draw.rect(window, SEARCH_COLOR,
                             (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.display.update()
            time.sleep(0.05)

        for n_row, n_col in get_neighbors(row, col, len(grid), len(grid[0])):
            neighbor = (n_row, n_col)
            if neighbor not in visited and grid[n_row][n_col] != 1:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    if path_found:
        # Instead of backtracking from end to start, we will collect and visualize the path forward
        path = reconstruct_path(parent, start, end)
        visualize_path(window, path, cell_size)
        return True
    else:
        return False

def get_neighbors(row, col, rows, cols):
    neighbors = []
    if row > 0: neighbors.append((row - 1, col))  # Up
    if row < rows - 1: neighbors.append((row + 1, col))  # Down
    if col > 0: neighbors.append((row, col - 1))  # Left
    if col < cols - 1: neighbors.append((row, col + 1))  # Right
    return neighbors

def reconstruct_path(parent, start, end):
    """Reconstruct the path from start to end"""
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent.get(current)
    path.append(start)
    path.reverse()  # Reverse to go from start to goal
    return path

def visualize_path(window, path, cell_size):
    """Visualize the path from start to goal"""
    for row, col in path:
        pygame.draw.rect(window, PATH_COLOR,
                         (col * cell_size, row * cell_size, cell_size, cell_size))
        pygame.display.update()
        time.sleep(0.4)
