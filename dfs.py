import pygame
import time

# Colors for visualization
SEARCH_COLOR = (255, 223, 186)  # cells being searched
PATH_COLOR = (255, 69, 0)    # the found path

# DFS Algorithm
def dfs(grid, start, end, window, cell_size):
    stack = [start]
    visited = set([start])
    parent = {}
    path_found = False

    while stack:
        current = stack.pop()
        row, col = current

        if current == end:
            path_found = True
            break

        if current != start and current != end:
            pygame.draw.rect(window, SEARCH_COLOR,
                             (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.display.update()
            time.sleep(0.05)

        for n_row, n_col in get_neighbors(row, col, len(grid), len(grid[0])):
            neighbor = (n_row, n_col)
            if neighbor not in visited and grid[n_row][n_col] != 1:
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    if path_found:
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
    """Trace back the path from the end to the start"""
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
