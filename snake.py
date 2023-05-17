import pygame
import math
import random
import copy
import sys

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos,color=(102,178,255))
        self.body.append(self.head)
        self.last_dir = ""
        self.curr_dir = "right"
        self.dirnx = 1
        self.dirny = 0

    def move(self, control=""):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        keys = pygame.key.get_pressed()
        if control != self.curr_dir:
            self.last_dir = self.curr_dir
            if control == "left":
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "left"

            elif control == "right":
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "right" 

            elif control == "up":
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "up"

            elif control == "down":
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.curr_dir = "down"

            else:
                for key in keys:
                    if keys[pygame.K_LEFT] and self.curr_dir != "left":
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "left"

                    elif keys[pygame.K_RIGHT] and self.curr_dir != "right":
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "right"

                    elif keys[pygame.K_UP] and self.curr_dir != "up":
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "up"

                    elif keys[pygame.K_DOWN] and self.curr_dir != "down":
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                        self.curr_dir = "down"
        print(self.dirnx)
        print(self.dirny)
                    
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: # out of left bound
                    c.pos = (19, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= 19: # out of right bound
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= 19: # out of bottom bound
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: # out of top bound
                    c.pos = (c.pos[0],19)
                else: c.move(c.dirnx,c.dirny)

    def reset(self, pos):
        self.head = cube(pos,color=(102,178,255))
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        for i in range(len(self.body)):
            if i:
                self.body[i].color = (255, 255, 255)

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]),color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]),color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1),color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1),color=self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def main():
    global width, rows, s, snack, win, visited
    pygame.init()
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Snake BFS')

    startx = random.randint(0, rows-1)
    starty = random.randint(0, rows-1)
    s = snake((255,255,51), (startx, starty))
    snack = cube(randomSnack(rows, s), color=(255,51,51))
    flag = True
    cost = 0
    clock = pygame.time.Clock()
    visited = set({})

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        #BFS
        if s.body[0].pos == snack.pos:
            visited = set({})
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 51, 51))
        
        if s.body[0].pos in list(map(lambda z:z.pos,s.body[1:])):
                redrawWindow(lose = True)
                print('Score: ', len(s.body)-1)
                showGameOverScreen()
                startx = random.randint(0, rows-1)
                starty = random.randint(0, rows-1)
                s.reset((startx,starty))
                snack = cube(randomSnack(rows, s), color=(255, 51, 51))
        
        redrawWindow()

main()