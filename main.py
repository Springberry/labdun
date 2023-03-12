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
        return False
    else:
        player.set_position(new_x, new_y)
        turn += 1
        return True

def check_for_enemy_encounter():
    if turn % 20 == 0 and turn > 0:
        return True
    return False

def battle_end_scene(stdscr, battle_end_status):
    match battle_end_status:
        case 1:
            stdscr.addstr("\n\nYou won the battle!!")
            stdscr.refresh()
            time.sleep(1)
        case 2:
            stdscr.addstr("\n\nYou died")
            stdscr.refresh()
            time.sleep(1)
        case 3:
            stdscr.addstr("\n\nYou fled")
            stdscr.refresh()
            time.sleep(1)

def enemy_encounter(stdscr):
    stdscr.clear()

    stdscr.addstr("Something attacks!!")

    stdscr.refresh()
    time.sleep(1)

    enemy_health = 5
    battle_end_status = 0

    while True:
        stdscr.erase()
        stdscr.addstr("Something attacks!!")
        stdscr.addstr(f"\nYour health:{player.health}")
        stdscr.addstr(f"\nEnemy health:{enemy_health}")
        stdscr.addstr("\nAttack [z]")
        stdscr.addstr("\nFlee [x]")


        stdscr.refresh()

        # Player Turn
        while True:
            try:
                key = stdscr.getkey()
            except:
                continue

            # Attack
            if key == 'z':
                stdscr.addstr("\n\nYou attacked!")
                damage = 1
                enemy_health -= damage
                stdscr.addstr(f"\nYou did {damage} damage")
                stdscr.refresh()
                time.sleep(1)

                if enemy_health <= 0:
                    battle_end_status = 1

                break
            # Flee
            elif key == 'x':
                battle_end_status = 3
                break

        if battle_end_status != 0:
            battle_end_scene(stdscr, battle_end_status)
            break

        # Enemy Turn

        stdscr.addstr("\n\nEnemy attacks you!")
        enemy_damage = 1
        player.health -= enemy_damage
        stdscr.addstr(f"\nEnemy did {enemy_damage} damage")
        stdscr.refresh()
        time.sleep(1)

        if player.health <=0:
            battle_end_status = 2
        
        if battle_end_status != 0:
            battle_end_scene(stdscr, battle_end_status)
            break

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

        moved = False
        if key == "w":
            moved = move_player(player.x_position, player.y_position - 1) 
        elif key == "a":
            moved =move_player(player.x_position - 1, player.y_position) 
        elif key == "s":
            moved =move_player(player.x_position, player.y_position + 1) 
        elif key == "d":
            moved =move_player(player.x_position + 1, player.y_position) 

        if check_for_enemy_encounter() and moved:
            enemy_encounter(stdscr)

    stdscr.refresh()

def main(stdscr):
    game(stdscr)
    stdscr.getkey()

wrapper(main)
