import curses
from curses import wrapper
import time
from entities.player import Player

raw_level_map = ['                              ',
                 '                              ',
                 '                              ',
                 '                              ',
                 '   #######     ##########     ',
                 '   #     #     #        #     ',
                 '   #     #######        #     ',
                 '   #                    #     ',
                 '   #                    #     ',
                 '   #              #######     ',
                 '   #              #           ',
                 '   #              #           ',
                 '   ################           ']

level_map = []

player = Player(x_position=7, y_position=7, symbol='@')
turn = 0

obj_wall = '#'

def load_level_map():
    global level_map
    level_map = []
    for row_index  in range(len(raw_level_map)):
        level_map.append([])
        for collumn_index in range(len(raw_level_map[row_index])):
            level_map[row_index].append(raw_level_map[row_index][collumn_index])

def render_level_map(stdscr):
    for row_index in range(len(level_map)):
        for collumn_index in range(len(level_map[row_index])):
            obj = level_map[row_index][collumn_index]
            if obj == obj_wall:
                stdscr.addstr(row_index, collumn_index, obj)
            else:
                stdscr.addstr(row_index, collumn_index, obj)
    # Render the Player

    stdscr.addstr(player.y_position, player.x_position, player.symbol)


def move_player(new_x, new_y):
    global player, turn
    lookahead = level_map[new_y][new_x]
    if lookahead == obj_wall:
        return
    else:
        player.set_position(new_x, new_y)
        turn += 1

def check_for_enemy_encounter():
    if turn % 20 == 0:
        return True
    return False

def enemy_encounter(stdscr):
    stdscr.clear()

    stdscr.addstr("Something attacks!!")

    stdscr.refresh()
    time.sleep(1)

    while True:
        stdscr.erase()
        stdscr.addstr("Something attacks!!")
        stdscr.addstr(1,0,"Attack [z]")
        stdscr.addstr(2,0,"Flee [x]")

        battle_end_status = 0

        stdscr.refresh()

        try:
            key = stdscr.getkey()
        except:
            continue

        # Attack
        if key == 'z':
            stdscr.addstr("\n\nYou attacked!")
            stdscr.refresh()
            time.sleep(1)
        # Flee
        elif key == 'x':
            battle_end_status = 2
            break

    if battle_end_status == 2:
        stdscr.addstr("\n\nYou fled")
        stdscr.refresh()
        time.sleep(1)

def game(stdscr):
    global player

    load_level_map()

    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        render_level_map(stdscr)
        stdscr.addstr(0,0, f"turn: {turn}")

        try:
            key = stdscr.getkey()
        except:
            continue
        if key == "w":
            move_player(player.x_position, player.y_position - 1) 
        elif key == "a":
            move_player(player.x_position - 1, player.y_position) 
        elif key == "s":
            move_player(player.x_position, player.y_position + 1) 
        elif key == "d":
            move_player(player.x_position + 1, player.y_position) 

        if check_for_enemy_encounter():
            enemy_encounter(stdscr)

    stdscr.refresh()

def main(stdscr):
    game(stdscr)
    stdscr.getkey()

wrapper(main)
