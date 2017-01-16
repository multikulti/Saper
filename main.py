import math
import operator
from time import sleep
import re
import pygame
import pyscroll
import pytmx
import inputbox
from astar import AStar
from pygame.locals import *
from pytmx.util_pygame import load_pygame

FPS = 60
MOVEMENT_DELAY = 0.3
MAP_FILE = 'map.tmx'
PLAYER_IMAGE = 'player.png'


# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


class Player(pygame.sprite.Sprite):

    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()

        # private variables
        self._position = [0, 0]

    @property
    def position(self):
        return tuple(self._position)
        
    def getx(self):
        return int(self.rect.x/32)
        
    def gety(self):
        return (self.rect.y/32)
        
    def printposition(self):
        print(str(self.rect.x) + "   " + str(self.rect.y))

    @position.setter
    def position(self, value):
        self._position = list(value)
        self.rect.topleft = self._position
		
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Pathfinder(AStar):

    def __init__(self, mesh):
        self.width = mesh.width
        self.height = mesh.height

    def heuristic_cost_estimate(self, n1, n2):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1
        (x2, y2) = n2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adjacent"""
        return 1

    def neighbors(self, node):
        """for a given coordinate on the mesh, returns up to 8 adjacent nodes that can be reached (=any adjacent coordinate that is walkable)"""
        x, y = node
        for i, j in [(0, -1), (0, +1), (-1, 0), (+1, 0)]:
            x1 = x + i
            y1 = y + j
            if x1 > 0 and y1 > 0 and x1 < self.width and y1 < self.height and game.layer.data[y1][x1]==0:
                yield (x1, y1)


class RandomGame(object):

    def __init__(self, mapfile):
        self._move_queue = []
        self.running = False
        self.last_position_update = 0
        map = load_pygame(mapfile)

        self.layer = map.layers[1]

        map_data = pyscroll.data.TiledMapData(map)

        w, h = screen.get_size()

        self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size(), clamp_camera=True)

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.map_layer.zoom = .5

        self.player = Player(PLAYER_IMAGE)
        self.player.position = self.map_layer.map_rect.center

        self.group.add(self.player)

        self.mesh = Pathfinder(map)

    def draw(self, surface):
        self.group.center(self.player.rect.center)

        self.group.draw(surface)

    def handle_input(self):                
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    pygame.exit()
                    break

                if event.key == K_SPACE:
                    command = inputbox.ask(screen, "ROZKAZ")
        
                    '''actionlist = {"zmień":"move", "przejdź":"move", "dojdź":"move", "idź":"move", "jedź":"move", "pojedź":"move",
                        "przejedź":"move", "dojedź":"move", "dotrzyj":"move", "podjedź":"move", "podejdź":"move",
                        "detonuj":"detonate", "zniszcz":"detonate", "niszcz":"detonate", "zdetonuj":"detonate", "przetnij":"defuse",
                        "rozbrój":"defuse", "rozbrajaj":"defuse", "przesuń":"movebomb", "przenieś":"movebomb", "zanieś":"movebomb",
                        "podnieś":"movebomb"}

                    numbers = {"jedną":1, "1":1, "dwie":2, "2":2, "trzy":3, "3":3, "cztery":4, "4":4, "pięć":5, "5":5, "sześć":6, "6":6, "siedem":7, "7":7, "osiem":8,
                               "8":8, "dziewięć":9, "9":9}

                    directions = {"góry":"up", "górę":"up", "północ":"up", "górny":"up", "góra":"up", "górnym":"up", "północnym":"up", "północny":"up", "północy":"up", "prawo":"right",
                                  "wschód":"right", "wschodni":"right", "wschodnim":"right", "lewo":"left", "zachód":"left", "zachodnim":"left", "zachodni":"left", "dół":"down", "dołu":"down", "południe":"down",
                                  "południową":"down", "południowy":"down", "dolny":"down", "dolnym":"down", "południowym":"down"}

                    randomstring = "przejedź na pozycję D5, zmień lokalizację na E2 i przesuń się o 9 kratek w lewo, dotrzyj na pole C5, podnieś bombę, zanieś ją na pole E6, zdetonuj bombę, przesuń się do góry o 5 kratek, idź w lewo 3 razy, przesuń bombę na F7, idź na A4, rozbrajaj, podejdź na B5, detonuj, jedź na pole G9, rozbrajaj ładnuek, przetnij, idź 5 kratek na zachód, dojedź na B7, dojdź na H8, idź w górę 5 kratek, podejdź do miny na A2, detonuj bombę"'''
                    
                    actionlist = {"zmien":"move", "przejdz":"move", "dojdz":"move", "idz":"move", "jedz":"move", "pojedz":"move",
                        "przejedz":"move", "dojedz":"move", "dotrzyj":"move", "podjedz":"move", "podejdz":"move",
                        "detonuj":"detonate", "zniszcz":"detonate", "niszcz":"detonate", "zdetonuj":"detonate", "przetnij":"defuse",
                        "rozbroj":"defuse", "rozbrajaj":"defuse", "przesun":"move", "przenies":"movebomb", "zanies":"movebomb",
                        "podnies":"movebomb"}

                    numbers = {"jedna":1, "1":1, "dwie":2, "2":2, "trzy":3, "3":3, "cztery":4, "4":4, "piec":5, "5":5, "szesc":6, "6":6, "siedem":7, "7":7, "osiem":8,
                               "8":8, "dziewiec":9, "9":9}

                    directions = {"gory":"up", "gore":"up", "polnoc":"up", "gorny":"up", "gora":"up", "gornym":"up", "polnocnym":"up", "polnocny":"up", "polnocy":"up", "prawo":"right",
                                  "wschod":"right", "wschodni":"right", "wschodnim":"right", "lewo":"left", "zachod":"left", "zachodnim":"left", "zachodni":"left", "dol":"down", "dolu":"down", "poludnie":"down",
                                  "poludniowa":"down", "poludniowy":"down", "dolny":"down", "dolnym":"down", "poludniowym":"down"}

                    randomstring = "przejedz na pozycje D5, zmien lokalizacje na E2 i przesun sie o 9 kratek w lewo, dotrzyj na pole C5, podnies bombe, zanies ja na pole E6, zdetonuj bombe, przesun sie do gory o 5 kratek, idz w lewo 3 razy, przesun bombe na F7, idz na A4, rozbrajaj, podejdz na B5, detonuj, jedz na pole G9, rozbrajaj ladnuek, przetnij, idz 5 kratek na zachod, dojedz na B7, dojdz na H8, idz w gore 5 kratek, podejdz do miny na A2, detonuj bombe"


                    splitted = command.lower().replace('.', ',').replace(" i ", ",").split(",")

                    pattern = re.compile("\d+\-\d+")
                    
                    for i in range(len(splitted)): #pojedyncze komendy
                        commandsinglewords = splitted[i].split()
                        order = ["", "", ""]
                        for word in commandsinglewords:
                            for action, key in actionlist.items():
                                if word == action:
                                    order[0] = key
                            for direction, key in directions.items():
                                if word == direction:
                                    order[1] = key
                            for number, key in numbers.items():
                                if word == number:
                                    order[2] = key
                            if re.match(pattern, word):
                                order[2] = word
                        if order[0]=="move":
                            if order[1]=="":
                                cords = order[2].split("-")
                                print(cords[0])
                                print(cords[1])                              
                                tile_position = tuple(map(operator.floordiv, self.player.position, self.map_layer.data.tile_size))
                                self._move_queue = self.mesh.astar(tile_position, (int(cords[0]), int(cords[1])))

                                
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w / 2, event.h / 2))

    def update(self, dt):
        """ Tasks that occur over time should be handled here"""
        if self.last_position_update >= MOVEMENT_DELAY:
            if self._move_queue != []:
                self.player.position = list(map(operator.mul, self._move_queue[0], self.map_layer.data.tile_size))
                del self._move_queue[0]
            self.last_position_update = 0

    def run(self):
        """ Run the game loop"""
        clock = pygame.time.Clock()
        self.running = True

        try:
            while self.running:
                dt = clock.tick(FPS) / 1000.
                self.last_position_update += dt
                self.handle_input()
                self.update(dt)
                self.draw(screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False
            pygame.exit()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = init_screen(800, 600)
    pygame.display.set_caption('Moving X on the desert')

    try:
        game = RandomGame(MAP_FILE)
        game.run()
    except:
        pygame.quit()
        raise
