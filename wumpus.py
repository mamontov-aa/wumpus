import sys
import random as rnd
import keyboard as kb

class CGraphNode():
    def __init__(self, name):
        self.name = name
        self.adjacents = []

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

    def reset_actors_positions(self):
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

    def get_bats_random_move(self):
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

    def move_to(self, position_name):
        self.position = self.game_map.nodes[position_name]


class CPlayer(CMapActor):
    def __init__(self, game_map = None, player_name=None):
        super().__init__(game_map)
        if game_map is not None:
            self.game_map.player = self
            self.position = self.game_map.get_player_start_position()
        self.player_name = player_name
        self.arrow_range = 3
        self.lives = 5
        self.reload()
    
    def reload(self):
        self.arrows = 3
        self.lives -= 1
    
    def shoot(self):
        self.arrows -= 1

    def get_stats(self):
        return "Player '" + self.player_name + "', position: [" + self.position.name + "], lives left: " + str(self.lives) + ", arrows left: " + str(self.arrows)

class CWumpus(CMapActor):
    def __init__(self, game_map = None):
        super().__init__(game_map)
        if game_map is not None:
            self.game_map.wumpus = self
            self.position = self.game_map.get_wumpus_start_position()

    def wake_up_and_wander(self):
        self.move_to(rnd.choice([self.position] + self.position.adjacents).name)
        print(f"Wumpus now sleeps at {self.position.name}")


class CBatsFlock(CMapActor):
    def __init__(self, game_map = None):
        super().__init__(game_map)
        if game_map is not None:
            self.game_map.bats.append(self)
            self.position = self.game_map.get_bats_start_position()
    
    def carry_player_random_place(self):
        self.game_map.player.move_to(self.game_map.get_bats_random_move())


class CController():
    def __init__(self, game_map = None, player = None):
        self.available_commands = ["move", "shoot", "describe", "god", "cancel", "reset", "quit", "help"]
        self.cursor_text = "> "
        if game_map is not None:
            self.game_map = game_map
            if self.game_map.player is not None:
                self.player = self.game_map.player
        if player is not None:
            self.player = player

    def read_command(self):
        while True:
            try:
                new_cmd = input(self.cursor_text).lower().split(sep=" ")
            except KeyboardInterrupt:
                new_cmd = ["quit"]
            match_commads = list(x for x in self.available_commands if x.lower().startswith(new_cmd[0].lower()))
            if len(match_commads) == 1:
                return (match_commads[0], list(set(new_cmd) - set([new_cmd[0]])))
            else:
                print(f"ERROR: Command '{new_cmd}' not recognized")

    def exit_game(self):
        print("Bye ...")
        sys.exit()

    def print_help(self):
        print(f"Available commands: {self.available_commands}")
    
    def print_describe(self):
        print(f"Player stats")
        print(self.player.get_stats())


print("Hello and welcome to the game")
print("You are in labirynth, move and shoot arrows to kill Wumpus")

the_world = CGameMap()
the_world.load_by_edges("AB, BC, CD, DE, EA, AG, BH, CI, DJ, EF, GL, LH, HM, MI, IN, NJ, JO, OF, FK, KG, OP, KQ, LR, MS, NT, PQ, QR, RS, ST, TP")
the_world.set_gulfs()

the_player = CPlayer(game_map=the_world, player_name="WumpusHunter")
the_wumpus = CWumpus(game_map=the_world)
bats1 = CBatsFlock(game_map=the_world)
bats2 = CBatsFlock(game_map=the_world)

cc = CController(the_world, the_player)
cc.print_help()

while True:
    (cmd, args) = cc.read_command()
    if cmd == "quit":
        cc.exit_game()
    elif cmd == "help":
        cc.print_help()
    elif cmd == "describe":
        cc.print_describe()
