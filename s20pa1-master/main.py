import pygame, sys, random
from pygame.locals import *
from algorithms import *
from maps import *
import argparse

parser = argparse.ArgumentParser(description='Search in a grid world.')
parser.add_argument('--mode', '-m', dest='mode', type = int, default=0, help='0: random map, 1: predefined map, 2: autograde')
parser.add_argument('--load', '-l', dest='load_num', type = int, default=0, help='map number to load')
args = parser.parse_args()
random.seed(0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 82, 33)
GREY = (220, 220, 220)
DARKGREY = (128, 128, 128)
GREENGREY = (125, 164, 120)
RED = (160, 27, 16)
REDGREY = (182, 128, 109)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GOLD = (230, 230, 138)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

class GridWorld():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grid World")
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [450, 450]
        self.font = pygame.font.SysFont("Calibri", 16)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        self.show_checked = True
        self.quit = False
        self.type = "dfs"
    def new_grid(self, _random):
        self.grid = Grid(self)
        self.agent = Agent(self.grid, self.grid.start, self.grid.goal, self.type)
        if _random:
            self.grid.random()
        else:
            self.grid.load(args.load_num)
        self.run = False
    def loop(self, mode):
        if mode == 0:
            self.new_grid(True)
        elif mode == 1:
            self.new_grid(False)
        elif mode == 2:
            for i in range(len(Maps)):
                self.grid = Grid(self)
                self.agent = Agent(self.grid, self.grid.start, self.grid.goal, self.type)
                self.grid.load(i)
                self.agent.search("ucs")
                print("== Checking Map", i, "==")
                while not self.agent.finished and not self.agent.failed:
                    self.agent.make_step()
                c = self.agent.final_cost
                if c == Ans[i]:
                    print("[UCS] Correct optimal cost: ", c)
                else:
                    print("[UCS] Incorrect optimal cost: ", c, "!=", Ans[i])
                self.agent.search("astar")
                while not self.agent.finished and not self.agent.failed:
                    self.agent.make_step()
                c = self.agent.final_cost
                if c == Ans[i]:
                    print("[AStar] Correct optimal cost: ", c)
                else:
                    print("[AStar] Incorrect optimal cost: ", c, "!=", Ans[i])
            return        
        else:
            print("--mode only takes 0,1,2.")
            return
        while True:
            self.draw()
            self.clock.tick(60)
            self.mpos = pygame.mouse.get_pos()
            if self.run:
                if self.agent.finished:
                    self.agent.show_result()
                    self.run = False
                elif self.agent.failed:
                    self.run = False
                else:
                    self.agent.make_step()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        self.run = not self.run
                    if event.key == K_c:
                        if mode == 0:
                            self.new_grid(True)
                        elif mode == 1:
                            self.new_grid(False)
                    if event.key == K_1:
                        self.grid.clear_path()
                        self.type = "dfs"
                        self.agent.search(self.type)
                    if event.key == K_2:
                        self.grid.clear_path()
                        self.type = "bfs"
                        self.agent.search(self.type)
                    if event.key == K_3:
                        self.grid.clear_path()
                        self.type = "ucs"
                        self.agent.search(self.type)
                    if event.key == K_4:
                        self.grid.clear_path()
                        self.type = "astar"
                        self.agent.search(self.type)
    def blitInfo(self):
        line1 = self.font.render("Press Enter to find path or pause, press 'c' to clear board", 1, WHITE)
        line2 = self.font.render("Press 1 for DFS, 2 for BFS, 3 for UCS, 4 for A*", 1, WHITE)
        self.screen.blit(line1, (5, 5))
        self.screen.blit(line2, (5, 20))
    def draw(self):
        self.screen.fill(0)
        self.grid.update()
        self.blitInfo()
        pygame.display.update()

class Grid:
    def __init__(self, game):
        self.game = game
        self.width = int(self.game.screen_res[0]/15)
        self.height = int((self.game.screen_res[1]/15)-3)
        self.nodes = {(i, j): Node(self, (i+3, j)) for i in range(self.height) for j in range(self.width)}
        self.row_range = self.width-3
        self.col_range = self.height+3
        self.start = (5,3)
        self.goal = (self.height-3, self.width-5)
    def random(self):
        for node in self.nodes.values():
            node.random_puddle()
            node.random_grass()
    def load(self, index):
        m = Maps[index]
        for i in range(self.height):
            for j in range(self.width):
                if m[(i,j)] == 2:
                    self.nodes[(i,j)].make_puddle()
                elif m[(i,j)] == 1:
                    self.nodes[(i,j)].make_grass()
    def update(self):
        for node in self.nodes.values():
            node.update()
            node.draw(self.game.screen)
        for i in range(self.width):
            pygame.draw.line(self.game.screen, [100]*3, (15*i, 45), (15*i, 750))
        for i in range(self.height):
            pygame.draw.line(self.game.screen, [100]*3, (0, (15*i)+45), (750, (15*i)+45))
    def clear_path(self):
        for node in self.nodes.values():
            if node.checked:
                node.checked = False
            if node.in_path:
                node.in_path = False
            if node.frontier:
                node.frontier = False

class Node():
    def __init__(self, grid, pos):
        self.grid = grid
        self.game = self.grid.game
        self.pos = pos
        self.blit_pos = [self.pos[1]*15, self.pos[0]*15]
        self.color = BLACK
        self.image = pygame.Surface((15, 15))
        self.rect = self.image.get_rect(topleft=self.blit_pos)
        self.in_path = False
        self.checked = False
        self.frontier = False
        self.puddle = False
        self.grass = False
        self.start = False
        self.goal = False
    def update(self):
        #The order of these lines is important
        if self.puddle:
            self.color = BLUE
        elif self.start:
            self.color = YELLOW
        elif self.goal:
            self.color = ORANGE
        elif self.in_path:
            self.color = RED
            if self.grass:
                self.color = REDGREY
        elif self.frontier:
            self.color = GREY
        elif self.checked:
            self.color = DARKGREY
            if self.grass:
                self.color = GREENGREY
        elif self.grass:
            self.color = GREEN
        elif not self.game.run:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.game.mpos):
                self.puddle = True
            if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(self.game.mpos):
                self.puddle = False
        else:
            self.color = BLACK
    def make_puddle(self):
        if not self.goal and not self.start:
            self.puddle = True
    def make_grass(self):
        if not self.puddle:
            self.grass = True
    def random_puddle(self):
        if not random.randint(0,8): 
            self.make_puddle()
    def random_grass(self):
        if not random.randint(0,3):
            self.make_grass()
    def cost(self):
        if self.grass:
            return 10
        else:
            return 1
    def draw(self, screen):
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)

if __name__ == '__main__':
    game = GridWorld()
    game.loop(args.mode)
