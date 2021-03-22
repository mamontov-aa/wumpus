import sys
import random as rnd
import keyboard as kb

class CGraphNode():
    def __init__(self, name):
        self.name = name
        self.adjacents = []
    
    def get_adjacents_names(self):
        return list(x.name for x in self.adjacents)


class CGraph():
    def __init__(self):
        self.nodes = {}

    def load_by_edges(self, descr: str):
        load_edges = descr.split(", ")
        load_nodes = set("".join(load_edges))
        for i_node in load_nodes:
            self.nodes[i_node] = CGraphNode(i_node)
        for i_edge in load_edges:
            self.nodes[i_edge[0]].adjacents.append(self.nodes[i_edge[1]])
            self.nodes[i_edge[1]].adjacents.append(self.nodes[i_edge[0]])

    def get_nodenames(self):
        return list(x for x in self.nodes)

    def get_correct_route(self, first_pos: CGraphNode, route_str: str, n_limit: int = None):
        route_list = route_str.split(" ")
        last_node = first_pos
        route_list_correct = []
        for i in range(len(route_list)):
            if (n_limit is not None and i < n_limit) and route_list[i] in self.get_nodenames() and route_list[i] in last_node.get_adjacents_names():
                good_node = self.nodes[route_list[i]]
                route_list_correct.append(good_node)
                last_node = good_node
            else:
                print(f"Route {route_list} is shrinked to {route_list_correct}")
                break
        return (route_list_correct, len(route_list)-len(route_list_correct))

    def get_subgraph(self, sub_node, sub_range: int = 0):
        if sub_range == 0:
            return [sub_node]
        else:
            sub_graph = [sub_node]
            for i_adjacent in sub_node.adjacents:
                sub_graph += self.get_subgraph(i_adjacent, sub_range-1)
            return set(sub_graph)

class CGameMap(CGraph):
    def __init__(self):
        self.player = None
        self.wumpus = None
        self.bats = []
        super().__init__()

    def set_gulfs(self, n: str = 2):
        self.gulfs = []
        for _ in range(n):
            self.gulfs.append(CMapObject(self, self.get_gulf_start_position()))

    def reset_actors(self):
        for self.i_gulf in self.gulfs:
            self.i_gulf.position = None
        for self.i_bat in self.bats:
            self.i_bat.position = None
        if self.player is not None:
            self.player.position = None
        if self.wumpus is not None:
            self.wumpus.position = None
        for self.i_gulf in self.gulfs:
            self.i_gulf.position = self.get_gulf_start_position()
        for self.i_bat in self.bats:
            self.i_bat.position = self.get_bats_start_position()
        if self.player is not None:
            self.player.position = self.get_player_start_position()
        if self.wumpus is not None:
            self.wumpus.position = self.get_wumpus_start_position()
        self.player.is_dead = False
        self.wumpus.is_dead = False
        print("The world was reset")

    def get_bats_random_move_to(self):
        return rnd.choice(list(set(self.nodes) - set(self.bats[0].position, self.bats[1].position)))

    def get_player_start_position(self):
        avoid_pos = []
        if self.wumpus is not None:
            avoid_pos += [self.wumpus.position]
        for i_bat in self.bats:
            if i_bat is not None:
                avoid_pos += [i_bat.position]
        for i_gulf in self.gulfs:
            if i_gulf is not None:
                avoid_pos += [i_gulf.position]
        return self.nodes[rnd.choice(list(set(self.nodes) - set(avoid_pos)))]

    def get_wumpus_start_position(self):
        avoid_pos = []
        if self.player is not None:
            avoid_pos += [self.player.position]
        return self.nodes[rnd.choice(list(set(self.nodes) - set(avoid_pos)))]

    def get_bats_start_position(self):
        avoid_pos = []
        if self.player is not None:
            avoid_pos += [self.player.position]
        for i_bat in self.bats:
            if i_bat is not None:
                avoid_pos += [i_bat.position]
        return self.nodes[rnd.choice(list(set(self.nodes) - set(avoid_pos)))]

    def get_gulf_start_position(self):
        avoid_pos = []
        if self.player is not None:
            avoid_pos += [self.player.position]
        for i_gulf in self.gulfs:
            if i_gulf is not None:
                avoid_pos += [i_gulf.position]
        return self.nodes[rnd.choice(list(set(self.nodes) - set(avoid_pos)))]


class CMapObject():
    def __init__(self, game_map = None, position = None):
        self.game_map = game_map
        self.position = position


class CMapActor(CMapObject):
    def __init__(self, game_map = None):
        super().__init__(game_map)
        self.is_dead = False

    def move_to(self, position_name):
        self.position = self.game_map.nodes[position_name]

    def die(self):
        self.is_dead = True


class CPlayer(CMapActor):
    def __init__(self, game_map = None, name=None):
        super().__init__(game_map)
        if game_map is not None:
            self.game_map.player = self
            self.position = self.game_map.get_player_start_position()
        self.name = name
        self.arrow_range = 3
        self.lifes = 2
        self.reload()
    
    def reload(self):
        self.arrows = 3

    def shoot(self, shooting_str):
        self.arrows -= 1
        shooting_list, n_random = self.game_map.get_correct_route(self.position, shooting_str, self.arrow_range)
        if self.game_map.wumpus.position in shooting_list:
            self.game_map.wumpus.die()
        else:
            if n_random > 0:
                random_shoot_start = self.position if len(shooting_list) == 0 else shooting_list[-1]
                random_shooting_area = self.game_map.get_subgraph(random_shoot_start, n_random)
                if self.position == rnd.choice(random_shooting_area):
                    print("Player commited suicide")
                    self.die()
            if not self.is_dead:
                print(f"You missed and woke up Wumpus. Arrows left: {self.arrows}")
                self.game_map.wumpus.wake_up()

    def get_stats(self):
        return "Player '" + self.name + "', position: [" + self.position.name + "], lifes left: " + str(self.lifes) + ", arrows left: " + str(self.arrows)

    def move_to(self, position):
        if not self.is_dead:
            super().move_to(position)
            if self.position == self.game_map.wumpus.position:
                print("Player came to wumpus")
                self.die()
            elif self.position in list(x.position for x in self.game_map.gulfs):
                print("Player died fallen into bottmless gulf")
                self.die()
            elif self.position in list(x.position for x in self.game_map.bats):
                print("Player came to bats - random flight!")
                # TODO: find exact bats
                self.game_map.bats[0].carry_player()


class CWumpus(CMapActor):
    def __init__(self, game_map = None):
        super().__init__(game_map)
        if game_map is not None:
            self.game_map.wumpus = self
            self.position = self.game_map.get_wumpus_start_position()
            # self.woken_up = False

    def move_to(self, position_name):
        if not self.is_dead:
            super().move_to(position_name)
            if self.game_map.player.position == self.position:
                self.game_map.player.die()

    def wake_up(self):
        if not self.is_dead:
            # 25% probability to stay at home
            self.move_to(rnd.choice([self.position] + self.position.adjacents).name)
            self.woken_up = False


class CBatFlock(CMapActor):
    def __init__(self, game_map = None):
        super().__init__(game_map)
        if game_map is not None:
            self.game_map.bats.append(self)
            self.position = self.game_map.get_bats_start_position()

    def get_random_flight_position_name(self):
        return rnd.choice(list(set(self.game_map.nodes) - set(x.position for x in self.game_map.bats)))

    def carry_player(self):
        new_player_pos_name = self.get_random_flight_position_name()
        print(f"Bats carried player to [{new_player_pos_name}]")
        self.game_map.player.move_to(new_player_pos_name)


class CController():
    def __init__(self, game_map = None, player = None):
        self.available_commands = ["move", "shoot", "info", "godmode", "quit", "help"]
        self.cursor_text = "> "
        if game_map is not None:
            self.game_map = game_map
            if self.game_map.player is not None:
                self.player = self.game_map.player
        if player is not None:
            self.player = player
        self.godmode = False

    def read_command(self):
        while True:
            try:
                new_cmd_list = input(self.cursor_text).split(sep=" ")
            except KeyboardInterrupt:
                new_cmd_list = ["quit"]
            match_commands = list(x for x in self.available_commands if x.lower().startswith(new_cmd_list[0].lower()))
            if len(match_commands) == 1:
                return (match_commands[0], new_cmd_list[1:])
            else:
                print(f"ERROR: Command '{new_cmd_list}' not recognized")

    def exit_game(self):
        print("\nBye ...")
        sys.exit()

    def print_help(self):
        print(f"Available commands: {self.available_commands}\nCommand can be recognized by first matching symbols: [help] = [h] ")
    
    def print_player_position_info(self):
        print(f"You are in [{self.player.position.name}] close to {self.player.position.get_adjacents_names()}")
        if self.game_map.wumpus.position in self.player.position.adjacents:
            print(f"Smells like Wumpus is {f'in [{self.game_map.wumpus.position.name}]' if self.godmode else 'near'}")
        for i_bat in self.game_map.bats:
            if i_bat.position in self.player.position.adjacents:
                print(f"Chir-chir... bats are {f'in [{i_bat.position.name}]' if self.godmode else 'quite close'}")
                break
        for i_gulf in self.game_map.gulfs:
            if i_gulf.position in self.player.position.adjacents:
                print(f"Whoa-a-a-o-o... it sounds like gulf is {f'in [{i_gulf.position.name}]' if self.godmode else 'aside'}")
                break

    def print_info(self):
        print(self.player.get_stats())

    def print_hello(self):
        print("Hello and welcome to the game")
        print("You are in labirynth, move and shoot arrows to kill Wumpus")
        print("If you don`t know what to do - ask for [help]")

    def toggle_godmode(self):
        self.godmode = not self.godmode
        print(f"GodMode {'On' if self.godmode else 'Off'}")
        if self.godmode:
            print(f"Wumpus in [{self.game_map.wumpus.position.name}]")
        
    def continue_game(self, msg = None, take_life: int = 0):
        if self.player.lifes < 1:
            cc.exit_game()
        while True:
            play_again = input(f"{f'Continue ({self.player.lifes} left)' if msg is None else msg} - [y/n]? > ").lower()
            if play_again == 'n':
                cc.exit_game()
            elif play_again == 'y':
                self.player.lifes -= take_life
                self.game_map.reset_actors()
                print("================================================================")
                break
            else:
                print(f"Unrecognized answer [{play_again}], try again.")

    def main(self):
        while True:
            # main player step
            print()
            self.print_player_position_info()
            # input
            (cmd, args) = self.read_command()
            if cmd == "quit":
                self.exit_game()
            elif cmd == "help":
                self.print_help()
            elif cmd == "info":
                self.print_info()
            elif cmd == "move":
                move_to = " ".join(args) if len(args) > 0 else input(f"Move to {self.player.position.get_adjacents_names()} or stay in [{self.player.position.name}]? > ")
                if move_to in self.player.position.get_adjacents_names() + [self.player.position.name]:
                    self.player.move_to(move_to)
                else:
                    print(f"Can`t move to [{move_to}], try again. Hint: cave names are case-sensitive.")
            elif cmd == "shoot":
                if self.player.arrows > 0:
                    shooting_str = " ".join(args) if len(args) > 0 else input(f"Type shoot route in one line space-delimited (like [A B C]) up to {self.player.arrow_range} steps > ")
                    self.player.shoot(shooting_str)
                else:
                    print("Nothing to shoot")
            elif cmd =="godmode":
                self.toggle_godmode()
            else:
                print(f"Command [{cmd}] not implemented yet")
            # check step for final conditions
            if self.game_map.wumpus.is_dead:
                print("You WIN ;-)")
                self.continue_game("Play again [y/n]? > ")
            if self.player.is_dead:
                print("You LOOSE :-(")
                self.continue_game(take_life=1)


the_world = CGameMap()
the_world.load_by_edges("AB, BC, CD, DE, EA, AG, BH, CI, DJ, EF, GL, LH, HM, MI, IN, NJ, JO, OF, FK, KG, OP, KQ, LR, MS, NT, PQ, QR, RS, ST, TP")

the_world.set_gulfs()

the_player = CPlayer(game_map=the_world, name="WumpusHunter")
the_wumpus = CWumpus(game_map=the_world)
bats1 = CBatFlock(game_map=the_world)
bats2 = CBatFlock(game_map=the_world)

cc = CController(the_world, the_player)
cc.print_hello()

cc.main()
