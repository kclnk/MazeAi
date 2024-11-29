import pygame
import sys
from bfs import bfs
from dfs import dfs
from ucs import ucs

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 600, 650  # Extra height for buttons
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
BUTTON_HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (0, 0, 255)
BUTTON_HOVER_COLOR = (100, 100, 255)
TEXT_COLOR = WHITE

# Initialize the grid (0 = empty, 1 = wall, 2 = start, 3 = end), list of lists representing each row
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Track if start and end points have been placed
start_set = False # green point flag
end_set = False # red point flag
start_pos, end_pos = None, None # coordinates of each point

# Button positions and dimensions
button_width = WIDTH // 3
button_positions = [ # coordinates of each button
    (0, GRID_SIZE * CELL_SIZE, button_width, BUTTON_HEIGHT),  # BFS button
    (button_width, GRID_SIZE * CELL_SIZE, button_width, BUTTON_HEIGHT),  # DFS button
    (button_width * 2, GRID_SIZE * CELL_SIZE, button_width, BUTTON_HEIGHT),  # UCS button
]
button_texts = ["BFS", "DFS", "UCS"] # list for button texts

def draw_grid():
    """Draw the grid and its elements"""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE
            if grid[row][col] == 1:  # Wall
                color = GREY
            elif grid[row][col] == 2:  # Start point
                color = GREEN
            elif grid[row][col] == 3:  # End point
                color = RED
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # for cells
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1) # for lines

def draw_buttons():
    """Draw algorithm buttons"""
    font = pygame.font.Font(None, 36)
    for idx, (x, y, w, h) in enumerate(button_positions):
        # Highlight button if hovered
        mouse_x, mouse_y = pygame.mouse.get_pos() # get mouse coordinated on screen
        if x <= mouse_x < x + w and y <= mouse_y < y + h:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, w, h))
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h))
        pygame.draw.rect(screen, BLACK, (x, y, w, h), 2) # draw outer lines for buttons

        # Draw button text
        text = font.render(button_texts[idx], True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(text, text_rect) # render text

def get_cell(pos): # get cell position
    """Convert screen coordinates to grid coordinates"""
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

def handle_left_click(pos):
    """Handle left-click to place or remove start/end points"""
    global start_set, end_set, start_pos, end_pos # global to modify the variables outside the function (global scope)
    row, col = get_cell(pos) # get click position on grid

    if row < GRID_SIZE and col < GRID_SIZE:  # Only interact with grid cells, in range (0-9 for rows and cols)
        if grid[row][col] == 2:  # Remove the start point
            grid[row][col] = 0
            start_set = False # flag -> false
            start_pos = None # coordinates
        elif grid[row][col] == 3:  # Remove the end point
            grid[row][col] = 0
            end_set = False
            end_pos = None
        elif grid[row][col] == 0:  # Place start or end point if empty
            if not start_set:
                grid[row][col] = 2  # Place the start point (green)
                start_set = True
                start_pos = (row, col)
            elif not end_set:
                grid[row][col] = 3  # Place the end point (red)
                end_set = True
                end_pos = (row, col)

def handle_right_click(pos):
    """Handle right-click to place or remove walls"""
    row, col = get_cell(pos) # get click position on grid

    if row < GRID_SIZE and col < GRID_SIZE:  # Only interact with grid cells, in range (0-9 for rows and cols)
        if grid[row][col] == 1:  # Remove the wall
            grid[row][col] = 0
        elif grid[row][col] == 0:  # Place a wall
            grid[row][col] = 1

def check_button_click(pos):
    """Check if a button is clicked and trigger the corresponding algorithm"""
    mouse_x, mouse_y = pos
    for idx, (x, y, w, h) in enumerate(button_positions):
        if x <= mouse_x < x + w and y <= mouse_y < y + h:
            if not start_set or not end_set:
                print("Both start and end points must be set")
                return

            start = None # for green point coordinates
            end = None # for red point coordinates

            # Locate start and end points
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if grid[row][col] == 2:
                        start = (row, col)
                    elif grid[row][col] == 3:
                        end = (row, col)

            # Check if start and end are valid
            if start is None or end is None:
                print("Start or end point not found.")
                return

            # Trigger the selected algorithm
            if button_texts[idx] == "BFS":
                print("Running BFS...")
                bfs(grid, start, end, screen, CELL_SIZE)
            elif button_texts[idx] == "DFS":
                print("Running DFS...")
                dfs(grid, start, end, screen, CELL_SIZE)
            elif button_texts[idx] == "UCS":
                print("Running UCS...")
                ucs(grid, start, end, screen, CELL_SIZE)

def main():
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_buttons()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # when close (X) button is clicked
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN: # check for mouse clicks
                if event.button == 1:  # Left click
                    if event.pos[1] < GRID_SIZE * CELL_SIZE: # ensure click is inside the grid
                        handle_left_click(event.pos)
                    else:
                        check_button_click(event.pos)
                elif event.button == 3:  # Right click
                    if event.pos[1] < GRID_SIZE * CELL_SIZE: # ensure click is inside the grid
                        handle_right_click(event.pos)

        pygame.display.flip() # update frames
        pygame.time.Clock().tick(15) # set frame rate to 30fps

    pygame.quit() # shutdown PyGame
    sys.exit() # terminate script (process)

if __name__ == "__main__":
    main()
