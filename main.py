import pygame
import random

# Color constants:
BG_LIGHT_GREEN = (137, 200, 80)
BG_DARK_GREEN = (123, 181, 70)
BLUE = (47, 174, 232)
DARK_BLUE = (44, 163, 217)
RED = (217, 42, 42)
DARK_RED = (197, 38, 38)
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)


# Game constants:
tile_size = 40
h, w = 18, 18
win_height, win_width = h * tile_size, w * tile_size
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


# The Snake class holds all relevant information regarding the player's current snake. These are:
# The snake's body segments' positions,
# The direction it is currently aiming to move to,
# Whether or not it is currently frozen (used just as a new game is beginning)
# And whether or not it is currently alive (used to know when to end the game).
class Snake:
    def __init__(self):
        self.segments = [(x, h // 2) for x in range(3)][::-1]
        self.direction = ''
        self.frozen = True
        self.alive = True


# The draw_background function is used to draw onto the window the checkered background of the game.
def draw_background():
    for x in range(w):
        for y in range(h):
            if (x + y) % 2 == 1:
                tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(win, BG_DARK_GREEN, tile_rect)


# The draw_snake function takes in the current snake object and draws it onto the window at the appropriate positions.
def draw_snake(snake):
    for position in snake.segments:
        snake_rect = pygame.Rect(position[0] * tile_size, position[1] * tile_size, tile_size, tile_size)
        pygame.draw.rect(win, BLUE, snake_rect)
        pygame.draw.rect(win, DARK_BLUE, snake_rect, tile_size // 10)


# The draw_food function takes in the food's current position and draws it onto the window at that position.
def draw_food(food_pos):
    food_rect = pygame.Rect(food_pos[0] * tile_size, food_pos[1] * tile_size, tile_size, tile_size)
    pygame.draw.rect(win, RED, food_rect)
    pygame.draw.rect(win, DARK_RED, food_rect, tile_size // 10)


# The move function takes in the current snake object and the current position of the food, and moves the snake's
# segments according to it's current intended direction of movement.
# This function is also responsible for extending the snake's body whenever he eats food.
def move(snake, food_pos):
    if not snake.frozen:
        tmp_segments = snake.segments[:]
        ghost_head = snake.segments[0][:]
        if snake.direction == 'u':
            snake.segments[0] = (snake.segments[0][0], snake.segments[0][1] - 1)
        elif snake.direction == 'd':
            snake.segments[0] = (snake.segments[0][0], snake.segments[0][1] + 1)
        elif snake.direction == 'l':
            snake.segments[0] = (snake.segments[0][0] - 1, snake.segments[0][1])
        elif snake.direction == 'r':
            snake.segments[0] = (snake.segments[0][0] + 1, snake.segments[0][1])

        # Moves the snake back one tile when he dies, so that he doesn't collide with the walls / itself.
        if check_dead(snake):
            snake.segments[0] = ghost_head

        # If the snake is alive, shift its' body segments forward by one tile and extend the snake's body if he has
        # eaten food.
        else:
            snake.segments[1:] = tmp_segments[:-1]

            if snake.segments[0] == food_pos:  # If the snake's head shares the same tile with the food, extend it.
                snake.segments.append(tmp_segments[-1])
                return True
    return False


# The check_dead function takes in the current snake object and checks if he has collided with a wall / itself.
# If it has indeed collided with another object, the function sets the snake's "alive" status to False and return True,
# otherwise the function returns False
def check_dead(snake):
    if snake.segments[0][0] not in range(w) \
            or snake.segments[0][1] not in range(h) \
            or snake.segments[0] in snake.segments[1:]:
        snake.alive = False
        return True
    return False


# The generate_food function returns a new randomized position for food.
def generate_food(snake):
    available_positions = []
    for x in range(w):
        for y in range(h):
            if (x, y) not in snake.segments:  # Ensures that the new food position is not within the snake's segments.
                available_positions.append((x, y))

    if not available_positions:
        return False
    food_position = available_positions[random.randint(0, len(available_positions) - 1)]
    return food_position


# The game_over_message function darkens the game window and displays a "GAME OVER" message across it.
def game_over_message():
    # Sets a translucent gray overlay on top of the game window.
    trans = pygame.Surface((win_width, win_height))
    trans.set_alpha(100)
    trans.fill(GRAY)
    win.blit(trans, (0, 0))

    # Displays the "GAME OVER" text.
    font = pygame.font.SysFont("bahnschrift", win_height // 7)
    text = font.render("GAME OVER", True, BLACK)
    text_rect = text.get_rect(center=(win_width // 2, win_height // 2 - tile_size // 2))
    win.blit(text, text_rect)


# The get_dir_dict takes in a cell's x and y coordinates, as well as the x and y limits of the grid it is sitting on,
# and returns a dictionary containing all of the adjacent cells and their direction relative to the inputted cell.
def get_dir_dict(x, y, x_lim, y_lim):
    adj_dict = dict()
    if y > 0:
        adj_dict[(x, y - 1)] = 'u'
    if y < y_lim:
        adj_dict[(x, y + 1)] = 'd'
    if x > 0:
        adj_dict[(x - 1, y)] = 'l'
    if x < x_lim:
        adj_dict[(x + 1, y)] = 'r'
    return adj_dict


# The prims_algorithm function creates a Minimum Spanning Tree using Prim's Algorithm with randomized choice instead of
# edge weights.
# The created MST is half the dimensions of the game grid, and is used as a guide to construct a Hamiltonian Cycle
# around the game grid.
def prims_algorithm():
    # The conn_dict dictionary is assigned all nodes in the guide grid as keys, and an empty array as values. The arrays
    # are gradually filled up with the chosen path of the Minimum Spanning Tree according to Prim's Algorithm

    # The full_dir_dict dictionary is assigned all nodes in the guide grid as keys, and their corresponding "dir_dict"
    # as values (see the get_dir_dict function for an explanation on "dir_dict"s).
    conn_dict, full_dir_dict = dict(), dict()
    for y in range(h // 2):
        for x in range(w // 2):
            conn_dict[(x, y)] = []
            full_dir_dict[(x, y)] = get_dir_dict(x, y, w // 2 - 1, h // 2 - 1)
    start = random.choice(list(full_dir_dict.keys()))  # Picks a node at random to start the MST.
    frontier = list(full_dir_dict[start].keys())  # Lists all available nodes that currently border the MST.
    visited = [start]  # Lists all nodes that have already been visited and are a part of the MST.
    desired_size = (w // 2) * (h // 2)

    # Repeat until all nodes have been visited:
    while len(visited) < desired_size:
        # Picks a random node from within the frontier.
        a = random.choice(frontier)
        available = []
        new_frontier = []

        # Checks all nodes that border the selected node.
        for adj in full_dir_dict[a].keys():
            # If the node has been visited and is a part of the MST, add it as a possible connection.
            if adj in visited:
                available.append(adj)
            # Otherwise, add it to the extended frontier, since it border the tree after the new edge is created.
            elif adj not in frontier:
                new_frontier.append(adj)

        # Pick a random node from the possible connections.
        b = random.choice(available)

        # Add the frontier node to the visited list and add the connection directions to the conn_dict for each of
        # the nodes.
        visited.append(a)
        conn_dict[b].append(full_dir_dict[b][a])
        conn_dict[a].append(full_dir_dict[a][b])

        # Remove the node from the frontier and add the new nodes that border the MST.
        frontier.remove(a)
        frontier += new_frontier
    return conn_dict


# The hamiltonian_cycle function takes in the current snake object and builds a Hamiltonian Cycle that begins and ends
# at the snake's head. The function uses a Prim's Minimum Spanning Tree with half the dimensions as a guideline to build
# the hamiltonian cycle.
def hamiltonian_cycle(snake):
    # The conn_dict holds the connection of all the Prim's MST nodes.
    conn_dict = prims_algorithm()
    cycle = [snake.segments[0]]

    # The cell_dict contains information about a tile's relative position within a cell (MST node).
    cell_dict = dict()
    for y in range(h):
        for x in range(w):
            cell_dict[x, y] = [(x // 2, y // 2), (x % 2, y % 2)]

    # Repeat the cycle contains all tiles in the game grid.
    while len(cycle) < w * h:
        # Selects the current final tile in the cycle.
        current_tile = cycle[-1]
        x, y = current_tile

        # The dir_dict dictionary contains information about the tiles bordering the currently selected tile, and their
        # relative direction to that tile.
        dir_dict = get_dir_dict(x, y, w - 1, h - 1)

        # Selects the cell that contains the currently selected tile.
        current_cell, cell_pos = cell_dict[current_tile]
        cell_conn = conn_dict[current_cell]

        # Repeat for all adjacent tiles that are not already within the cycle:
        for adj_tile in dir_dict.keys():
            if adj_tile not in cycle:
                # adj_conn contains the adjacent tile's relative direction to the selected tile.
                adj_conn = dir_dict[adj_tile]

                # If the adjacent tile is within a different cell to the selected one, and the current cell has a
                # connection to the other cell in the same direction as the selected tile to the adjacent tile,
                # add the adjacent tile to the cycle.
                if current_cell != cell_dict[adj_tile][0]:
                    if adj_conn in cell_conn:
                        cycle.append(adj_tile)
                        break

                # Otherwise if the adjacent tile is within the same cell and is connected vertically to the selected
                # tile, check that no horizontal cell connections "block" the vertical tile connection.
                # If indeed no cell connections block the tile connection, add the adjacent tile to the cycle.
                elif adj_conn in ['u', 'd']:
                    if not (('l' in cell_conn and cell_pos[0] == 0) or ('r' in cell_conn and cell_pos[0] == 1)):
                        cycle.append(adj_tile)
                        break
                # Otherwise, repeat for horizontal tile connections.
                elif not (('u' in cell_conn and cell_pos[1] == 0) or ('d' in cell_conn and cell_pos[1] == 1)):
                    cycle.append(adj_tile)
                    break

    # If the snake is facing the opposite direction from the cycle, flip the cycle's direction.
    if cycle.index(snake.segments[1]) == 1:
        cycle = cycle[::-1]

    return cycle


# The is_ordered function takes in the current Hamiltonian Cycle and a snake's body segments, and returns whether or not
# the snake is ordered (body is after the tail and before the head) within the cycle.
# EXAMPLES:
# EMPTY-TAIL-BODY-HEAD-EMPTY    > ORDERED
# BODY-HEAD-EMPTY-TAIL-BODY     > ORDERED
# EMPTY-HEAD-BODY-TAIL-EMPTY    > NOT ORDERED
# EMPTY-BODY-TAIL-HEAD-EMPTY    > NOT ORDERED
def is_ordered(cycle, segments):
    head = segments[0]
    tail = segments[-1]
    head_index = cycle.index(head)
    tail_index = cycle.index(tail)

    # If the head has overtaken the tail in the cycle, check that no snake segments appear before the tail or after
    # the head.
    if head_index > tail_index:
        for i in range(0, tail_index):
            if cycle[i] in segments:
                return False
        for i in range(head_index + 1, len(cycle)):
            if cycle[i] in segments:
                return False
    # If the tail has overtaken the head, check that no snake segments appear between the head and the tail.
    else:
        for i in range(head_index + 1, tail_index):
            if cycle[i] in segments:
                return False
    return True


# The generate_move function takes in the current Snake object, the current food position and the Hamiltonian Cycle and
# finds the next optimal move for the snake.
def generate_move(snake, food_pos, cycle):
    if not food_pos:  # If there is no food generated, act as though there is food at (0, 0) in order to avoid errors.
        food_pos = (0, 0)
    head_pos = snake.segments[0]
    food_index = cycle.index(food_pos)
    head_index = cycle.index(head_pos)

    # The dir_dict dictionary contains information about the tiles bordering the snakes head, and their relative
    # direction to it.
    dir_dict = get_dir_dict(head_pos[0], head_pos[1], w - 1, h - 1)

    # Sets the next position the snake will move to as the next position in the Hamiltonian Cycle. Default case in the
    # situation that no better shortcut is found for the snake to take.
    if head_index < len(cycle) - 1:
        next_pos = cycle[head_index + 1]
    else:
        next_pos = cycle[0]

    # Edge case, in case the snake has grown rapidly and the next position in the Hamiltonian Cycle will result in the
    # snake crashing into itself, select the first available tile to move to.
    if next_pos in snake.segments:
        for adj in dir_dict.keys():
            if adj not in snake.segments:
                next_pos = adj
                break

    # Default case, set the best_skip (the best move for the snake to take) as the next position in the Hamiltonian
    # Cycle, paired with it's distance to the food.
    next_pos_dist = food_index - cycle.index(next_pos)
    best_skip = (next_pos, next_pos_dist)

    # Only check for shortcuts if the snake takes up less than 85% of the game grid.
    if len(snake.segments) < (w * h) * 0.85:
        # Repeat for all adjacent tiles "skips" that are not a part of the snake's body:
        for skip in dir_dict.keys():
            if skip not in snake.segments:
                # Check if the snake's body will be ordered if the skip is taken.
                new_segments = [skip] + snake.segments
                if is_ordered(cycle, new_segments):
                    # Calculate the distance to the food if the skip is taken.
                    skip_dist = food_index - cycle.index(skip)
                    if skip_dist < 0:
                        skip_dist = len(cycle) - abs(skip_dist)

                    # If the skip is better than the current best skip, set the skip as the new best skip.
                    if skip_dist < best_skip[1]:
                        best_skip = (skip, skip_dist)
    return dir_dict[best_skip[0]]


# The game function contains the game loop which handles all game objects, including graphics, FPS (speeding up/down),
# generating new food if needed and controlling the various pause states (game over and before game begins).
def game():
    # Create game objects:
    snake = Snake()
    food_pos = generate_food(snake)
    cycle = hamiltonian_cycle(snake)

    fps = 20
    running = True
    while running:
        # FPS (also functions as the snake's speed):
        clock.tick(fps)

        # Graphics:
        win.fill(BG_LIGHT_GREEN)
        draw_background()
        if food_pos:
            draw_food(food_pos)
        draw_snake(snake)

        # Event loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Player has quit the game, close the game loop and return to main function.
                running = False
            if event.type == pygame.KEYDOWN:  # Player has pressed a keyboard button.
                if event.key == pygame.K_UP:  # Speed up snake.
                    fps *= 2
                if event.key == pygame.K_DOWN:  # Slow down snake.
                    fps //= 2

                # If the snake if frozen (before game has begun), unfreeze it and begin the game.
                if snake.frozen:
                    snake.frozen = False

                # If the snake is dead, reset the game.
                if not snake.alive:
                    snake = Snake()
                    food_pos = generate_food(snake)
                    cycle = hamiltonian_cycle(snake)

        # Determine the snake's next direction using the generate_move function.
        snake.direction = generate_move(snake, food_pos, cycle)
        # Move snake's body and generate new food if necessary.
        if move(snake, food_pos):
            food_pos = generate_food(snake)

        # If the snake is dead, display "GAME OVER" message.
        if not snake.alive:
            game_over_message()

        pygame.display.update()  # Refresh window.
    pygame.quit()


# The main function is simply used to initialize pygame, begin the game loop and close pygame once the game loop is
# closed (once the player quits).
def main():
    pygame.init()
    game()
    pygame.quit()


if __name__ == '__main__':
    main()
