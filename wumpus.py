import sys
import random
import keyboard as kb

def read_input(message: str):
    try:
        my_input = input(message).upper()
    except KeyboardInterrupt:
        my_input = 'X'
    return my_input


def exit_game():
    print("\nBye ...")
    sys.exit()


the_cave = { 'A': ['B', 'E', 'G'], 'B': ['A', 'C', 'H'], 
             'C': ['B', 'D', 'I'], 'D': ['C', 'E', 'J'], 
             'E': ['A', 'D', 'F'], 'F': ['E', 'K', 'O'],
             'G': ['A', 'K', 'L'], 'H': ['B', 'L', 'M'],  
             'I': ['C', 'M', 'N'], 'J': ['D', 'N', 'O'],
             'K': ['F', 'G', 'Q'], 'L': ['G', 'H', 'R'],
             'M': ['H', 'I', 'S'], 'N': ['I', 'J', 'T'],
             'O': ['J', 'F', 'P'], 'P': ['O', 'Q', 'T'],
             'Q': ['K', 'P', 'R'], 'R': ['L', 'Q', 'S'],
             'S': ['M', 'R', 'T'], 'T': ['N', 'P', 'S']
           }

def get_list_of_nodes(graph: dict):
    try:
        return("".join(graph.keys()))
    except:
        return("")

list_of_nodes = "ABCDEFGHIJKLMNOPQRST"

def get_connected(my_pos: str):
    global the_cave
    try:
        return the_cave[my_pos].copy()
    except:
        return []

player_lives = 3
player_arrows = 5
arrow_dist = 5

while True:
    player_pos = random.choice(list_of_nodes)
    while True:
        wumpus_pos = 'A' #random.choice(list_of_nodes)
        if wumpus_pos != player_pos:
            break
    while True:
        bats_pos = random.choice(list_of_nodes)
        if bats_pos not in [player_pos, wumpus_pos]:
            break
    while True:
        hole_pos = random.choice(list_of_nodes)
        if hole_pos not in [player_pos]:
            break

    print("Wumpus is in cave '" + wumpus_pos + "'")
    print("Bats are in cave '" + bats_pos + "'")
    print("Hole is in cave '" + hole_pos + "'")


    player_action = 0
    while True:
        if player_pos == wumpus_pos:
            print("\nOhm-nom-nom... You loose!")
            player_lives -= 1
            if player_lives > 0:
                player_action = read_input("Continue [" + str(player_lives) + "] or eXit? (c/x)? ")
                break
            else:
                exit_game()
        if player_pos == hole_pos:
            print("\nWhee-e-... You loose!")
            player_lives -= 1
            if player_lives > 0:
                player_action = read_input("Continue [" + str(player_lives) + "] or eXit? (c/x)? ")
                break
            else:
                exit_game()
        print("========================================")
        print("You are in cave: '" + player_pos + "' near to: " + str(the_cave[player_pos]))
        if wumpus_pos in get_connected(player_pos):
            print("What`s that spinch? Smells like wumpus is near...")
        if bats_pos in get_connected(player_pos):
            print("Bats nearby, watch out...")
        if hole_pos in get_connected(player_pos):
            print("Hole nearby, wsatch out...")
        while True:
            moved = False
            player_action = read_input("Shoot or move (S/M)? ").upper()
            if player_action == 'X':
                exit_game()
            elif player_action == 'M':
                while True:
                    player_move_to = read_input("Where do you want to move (" + the_cave[player_pos][0]+ "/" + the_cave[player_pos][1] + "/" + the_cave[player_pos][2] + ")? ").upper()
                    if player_move_to in the_cave[player_pos]:
                        player_pos = player_move_to
                        moved = True
                        break
                    elif player_move_to == 'X':
                        exit_game()
                    else:
                        print("You cannot move to '" + player_move_to + "'")
            elif player_action == 'S':
                if player_arrows < 1:
                    print("No arrows to shoot")
                else:
                    player_arrows -= 1
                    arrow_pos = player_pos
                    for i in range(5):
                        shoot_pos = read_input("Shoot " + str(i + 1) + " of " + str(arrow_dist) + " from cave '" + arrow_pos + "' to ? > ")
                        if shoot_pos == 'X':
                            exit_game()
                        if shoot_pos in get_connected(arrow_pos):
                            arrow_pos = shoot_pos
                            if arrow_pos == wumpus_pos:
                                print("You shot Wumpus! Well done =)")
                                break
                            else:
                                print("Arrow in cave '" + arrow_pos + "'")
                        else:
                            print("Cannot move arrow from '" + arrow_pos + "' to '" + shoot_pos + "'")
                            break
                    print("Arrows left: " + str(player_arrows))
                    wumpus_move_to = get_connected(wumpus_pos)
                    wumpus_move_to.append(wumpus_pos)
                    wumpus_pos = random.choice(wumpus_move_to)
                    print("Wumpus new position is: " + wumpus_pos)

            else:
                print("Unknown command: [" + player_action + "], try again")
            if moved:
                break
        if player_pos == bats_pos:
            player_pos = random.choice(list_of_nodes)
            print("Fly to random cave: " + player_pos)
    if player_action == 'X':
        exit_game()