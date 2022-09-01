import pygame
import random
import time


BG_LIGHT_GREEN = (137, 200, 80)
BG_DARK_GREEN = (123, 181, 70)
BLUE = (47, 174, 232)
DARK_BLUE = (44, 163, 217)
RED = (217, 42, 42)
DARK_RED = (197, 38, 38)
GRAY = (155, 155, 155)
BLACK = (0, 0, 0)


tile_size = 50
h, w = 10, 10
win_height, win_width = h * tile_size, w * tile_size
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.positions = [(3, h // 2), (2, h // 2), (1, h // 2)]
        self.direction = 'r'
        self.frozen = True
        self.alive = True


def draw_background():
    for x in range(w):
        for y in range(h):
            if (x + y) % 2 == 1:
                tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(win, BG_DARK_GREEN, tile_rect)


def draw_player(player):
    for position in player.positions:
        player_rect = pygame.Rect(position[0] * tile_size, position[1] * tile_size, tile_size, tile_size)
        pygame.draw.rect(win, BLUE, player_rect)
        pygame.draw.rect(win, DARK_BLUE, player_rect, tile_size // 10)


def draw_food(position):
    food_rect = pygame.Rect(position[0] * tile_size, position[1] * tile_size, tile_size, tile_size)
    pygame.draw.rect(win, RED, food_rect)
    pygame.draw.rect(win, DARK_RED, food_rect, tile_size // 10)


def move(player, has_eat):
    if not player.frozen:
        tmp_positions = player.positions[:]
        tmp_head = player.positions[0][:]
        if player.direction == 'u':
            player.positions[0] = (player.positions[0][0], player.positions[0][1] - 1)
        elif player.direction == 'd':
            player.positions[0] = (player.positions[0][0], player.positions[0][1] + 1)
        elif player.direction == 'l':
            player.positions[0] = (player.positions[0][0] - 1, player.positions[0][1])
        elif player.direction == 'r':
            player.positions[0] = (player.positions[0][0] + 1, player.positions[0][1])

        if check_dead(player):
            player.positions[0] = tmp_head

        else:
            player.positions[1:] = tmp_positions[:-1]
            if has_eat:
                player.positions.append(tmp_positions[len(tmp_positions) - 1])


def check_dead(player):
    if player.positions[0][0] not in range(w) \
            or player.positions[0][1] not in range(h) \
            or player.positions[0] in player.positions[1:-1]:
        player.alive = False
        return True
    return False


def generate_food(player):
    available_positions = []
    for x in range(w):
        for y in range(h):
            if (x, y) not in player.positions:
                available_positions.append((x, y))
    if not available_positions:
        return -1, -1
    food_position = available_positions[random.randint(0, len(available_positions) - 1)]
    return food_position


def game_over_message():
    trans = pygame.Surface((win_width, win_height))
    trans.set_alpha(100)
    trans.fill(GRAY)
    win.blit(trans, (0, 0))

    font = pygame.font.SysFont("bahnschrift", win_height // 7)
    text = font.render("GAME OVER", True, BLACK)
    text_rect = text.get_rect(center=(win_width // 2, win_height // 2 - tile_size // 2))
    win.blit(text, text_rect)


def prims_algorithm():
    adj_dict = dict()
    conn_dict = dict()
    for y in range(h // 2):
        for x in range(w // 2):
            conn_dict[x, y] = []
            adj_dict[x, y] = []
            if x > 0:
                adj_dict[x, y].append((x - 1, y))
            if x < w // 2 - 1:
                adj_dict[x, y].append((x + 1, y))
            if y > 0:
                adj_dict[x, y].append((x, y - 1))
            if y < h // 2 - 1:
                adj_dict[x, y].append((x, y + 1))

    total = len(adj_dict)
    x, y = 0, 0
    start = (x, y)

    tree = [start]
    while len(tree) < total:
        current = tree[-1]
        for adj in adj_dict[current]:
            if adj not in tree:
                tree.append(adj)
                if adj[0] - current[0] != 0:
                    if adj[0] - current[0] == 1:
                        conn_dict[current] += 'r'
                        conn_dict[adj] += 'l'
                    else:
                        conn_dict[current] += 'l'
                        conn_dict[adj] += 'r'
                elif adj[1] - current[1] == 1:
                    conn_dict[current] += 'd'
                    conn_dict[adj] += 'u'
                else:
                    conn_dict[current] += 'u'
                    conn_dict[adj] += 'd'

                break
    return conn_dict


def hamiltonian_cycle(player):
    conn_dict = prims_algorithm()
    cycle = player.positions[:2]
    cycle = cycle[::-1]

    cell_dict = dict()
    for y in range(h):
        for x in range(w):
            cell_dict[x, y] = [(x // 2, y // 2), (x % 2, y % 2)]

    while len(cycle) < w * h:
        current_seg = cycle[-1]
        x, y = current_seg

        adj_dict = dict()
        if y > 0:
            adj_dict[(x, y - 1)] = 'u'
        if y < h - 1:
            adj_dict[(x, y + 1)] = 'd'
        if x > 0:
            adj_dict[(x - 1, y)] = 'l'
        if x < w - 1:
            adj_dict[(x + 1, y)] = 'r'

        current_cell, cell_pos = cell_dict[current_seg]
        cell_conn = conn_dict[current_cell]

        for adj_seg in adj_dict.keys():
            if adj_seg not in cycle:
                adj_conn = adj_dict[adj_seg]
                if current_cell != cell_dict[adj_seg][0]:
                    if adj_conn in cell_conn:
                        cycle.append(adj_seg)
                        break

                elif adj_conn in ['u', 'd']:
                    if not (('l' in cell_conn and cell_pos[0] == 0) or ('r' in cell_conn and cell_pos[0] == 1)):
                        cycle.append(adj_seg)
                        break
                elif not (('u' in cell_conn and cell_pos[1] == 0) or ('d' in cell_conn and cell_pos[1] == 1)):
                    cycle.append(adj_seg)
                    break
    return cycle


def is_ordered(player, head, cycle):
    positions = player.positions[:-1]
    prev = head
    for position in positions:
        if cycle.index(position) > cycle.index(prev):
            return False
        prev = position
    return True


def ai_move(player, food_pos, cycle):
    if food_pos == (-1, -1):
        food_pos = (0, 0)
    head_pos = player.positions[0]
    head_index = cycle.index(head_pos)
    food_index = cycle.index(food_pos)
    x, y = head_pos

    adj_dict = dict()
    if y > 0:
        adj_dict[(x, y - 1)] = 'u'
    if y < h - 1:
        adj_dict[(x, y + 1)] = 'd'
    if x > 0:
        adj_dict[(x - 1, y)] = 'l'
    if x < w - 1:
        adj_dict[(x + 1, y)] = 'r'

    if len(player.positions) < (h * w) // 2 or True:
        for adj in adj_dict.keys():
            curr_diff = head_index - food_index
            shortcut_diff = cycle.index(adj) - food_index
            if abs(shortcut_diff) < abs(curr_diff) and curr_diff * shortcut_diff > 0:
                if is_ordered(player, adj, cycle):
                    print("SHORTCUT")
                    return adj_dict[adj]

    if head_index < len(cycle) - 1:
        next_pos = cycle[head_index + 1]
    else:
        next_pos = cycle[0]
    if next_pos[0] != head_pos[0]:
        if next_pos[0] - head_pos[0] == 1 and (x + 1, y) not in player.positions:
            return 'r'
        elif (x - 1, y) not in player.positions:
            return 'l'
    elif next_pos[1] - head_pos[1] == 1 and (x, y + 1) not in player.positions:
        return 'd'
    elif (x, y - 1) not in player.positions:
        return 'u'


def game(mode):
    player = Player()
    frame = 0
    food_pos = generate_food(player)
    has_eat = lock_direction = False

    cycle = hamiltonian_cycle(player)

    pygame.init()
    running = True
    while running:
        clock.tick(60)

        win.fill(BG_LIGHT_GREEN)
        draw_background()
        draw_food(food_pos)
        draw_player(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if player.frozen:
                    player.frozen = False
                if not lock_direction and mode == 1:
                    if event.key == pygame.K_UP and player.direction != 'd':
                        player.direction = 'u'
                        lock_direction = True
                    if event.key == pygame.K_DOWN and player.direction != 'u':
                        player.direction = 'd'
                        lock_direction = True
                    if event.key == pygame.K_LEFT and player.direction != 'r':
                        player.direction = 'l'
                        lock_direction = True
                    if event.key == pygame.K_RIGHT and player.direction != 'l':
                        player.direction = 'r'
                        lock_direction = True
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not player.alive:
                player = Player()
                food_pos = generate_food(player)
                has_eat = lock_direction = False

        frame += 1
        if frame > 10 and player.alive:
            if mode == 2:
                player.direction = ai_move(player, food_pos, cycle)

            move(player, has_eat)
            lock_direction = False

            if has_eat:
                has_eat = False
            if player.positions[0] == food_pos:
                has_eat = True
                food_pos = generate_food(player)
            frame = 0

        if not player.alive:
            game_over_message()

        pygame.display.update()
    pygame.quit()


def main():
    # mode = int(input("Enter (1) for Player\nEnter (2) for AI\n"))
    mode = 2
    game(mode)


if __name__ == '__main__':
    main()
