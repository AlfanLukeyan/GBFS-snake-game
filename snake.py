import pygame 
import random
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

class cube:
    rows = 20
    w = 500
    
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = ((self.pos[0] + self.dirnx) % cube.rows, (self.pos[1] + self.dirny) % cube.rows)

    def draw(self, surface, eyes=False, food=False):
        dis = cube.w // cube.rows
        i = self.pos[0]
        j = self.pos[1]
        
        if food:
            centre = dis // 2
            radius = 10
            pygame.draw.circle(surface, self.color, (i * dis + centre + 1, j * dis + centre + 1), radius)
        else:
            pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)

def bfsAlgorithm(): # Best First Search Algorithm to find the shortest path to the snack
    global s, snack, visited # s: snake, snack: snack, visited: visited nodes
    currentPositionX = s.body[0].pos[0] # current position of the snake by x axis 
    currentPositionY = s.body[0].pos[1] # current position of the snake by y axis
    nodes = [] # 0: left, 1: right, 2: up, 3: down

    # adding the nodes to the list 
    p = ((currentPositionX - 1) % 20,currentPositionY) 
    nodes.append(('left', manhattanDistance((currentPositionX - 1,currentPositionY),snack.pos,size = rows), p)) 
    p = ((currentPositionX + 1) % 20,currentPositionY)
    nodes.append(('right', manhattanDistance((currentPositionX + 1,currentPositionY),snack.pos,size = rows), p))
    p = (currentPositionX,(currentPositionY - 1) % 20)
    nodes.append(('up', manhattanDistance((currentPositionX,currentPositionY - 1),snack.pos,size = rows), p))
    p = (currentPositionX,(currentPositionY + 1) % 20)
    nodes.append(('down', manhattanDistance((currentPositionX,currentPositionY + 1),snack.pos,size = rows), p))

    if set(nodes[:][2])<= set(list(map(lambda z:z.pos,s.body))): # if the snake is stuck in a dead end 
        s.move()
        return
    
    i = 0 # index of the node
    print() 
    bestMove = [] # list of the best moves
    distance = [] # list of the distances of the nodes

    # finding the best moves
    for p in nodes:
        priority = 0 # priority of the node
        # if the snake is longer than 2 nodes and the snake can't go to the nodes in the list
        if (len(s.body) > 2):
            temp = [((currentPositionX + 1) % 20,(currentPositionY + 1) % 20),((currentPositionX + 1) % 20,(currentPositionY - 1) % 20)] # list of the nodes that the snake can't go to
            if set(temp) <= set(list(map(lambda z:z.pos,s.body))): 
                if p[0] == "right":
                    priority += 1
                elif (p[0] == "up" and s.curr_dir == "right" and s.last_dir == "up") or (p[0] == "down" and s.curr_dir == "right" and s.last_dir == "down"): 
                    priority += 1 
            temp = [((currentPositionX - 1) % 20,(currentPositionY + 1) % 20),((currentPositionX - 1) % 20,(currentPositionY - 1) % 20)]
            if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                if p[0] == "left":
                    priority += 1
                elif (p[0] == "up" and s.curr_dir == "left" and s.last_dir == "up") or (p[0] == "down" and s.curr_dir == "left" and s.last_dir == "down"):
                    priority += 1
            temp = [((currentPositionX + 1)%20,(currentPositionY + 1)%20),((currentPositionX - 1)%20,(currentPositionY + 1)%20)]
            if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                if p[0] == "down":
                    priority += 1
                elif (p[0] == "left" and s.curr_dir == "down" and s.last_dir == "left") or (p[0] == "right" and s.curr_dir == "down" and s.last_dir == "right"):
                    priority += 1
            temp = [((currentPositionX + 1)%20,(currentPositionY - 1)%20),((currentPositionX - 1)%20,(currentPositionY - 1)%20)]
            if set(temp) <= set(list(map(lambda z:z.pos,s.body))):
                if p[0] == "up":
                    priority += 1
                elif (p[0] == "left" and s.curr_dir == "up" and s.last_dir == "left") or (p[0] == "right" and s.curr_dir == "up" and s.last_dir == "right"):
                    priority += 1
                    
            cy = 0 # number of the nodes in the left side of the snake 
            if currentPositionY > 16 and currentPositionY < 19: # if the snake is in the bottom of the screen
                cy = 19 - currentPositionY 
            elif currentPositionY < 17: # if the snake is in the top of the screen
                cy = 3
            bottom = [q for q in list(map(lambda z:z.pos,s.body)) if q[0] == currentPositionX and q[1] - currentPositionY < cy and currentPositionY < q[1]] # list of the nodes in the bottom of the snake
            for i in range(3-cy): # adding the nodes in the bottom of the snake to the list
                if (currentPositionX,i) in list(map(lambda z:z.pos,s.body)): bottom.append((currentPositionX,i)) # if the node is in the snake add it to the list 
            print("bottom " + str(bottom)) # printing the list of the nodes in the bottom of the snake

            cy = 0  # number of the nodes in the top side of the snake
            if currentPositionY > 0 and currentPositionY < 3: 
                cy = currentPositionY
            elif currentPositionY > 2: # 
                cy = 3
            top = [q for q in list(map(lambda z:z.pos,s.body)) if q[0] == currentPositionX and currentPositionY - q[1] < cy and currentPositionY > q[1]]
            for i in range(19,16+cy,-1):
                if (currentPositionX,i) in list(map(lambda z:z.pos,s.body)): top.append((currentPositionX,i))
            print("top " + str(top))

            cx = 0 # number of the nodes in the right side of the snake
            if currentPositionX > 0 and currentPositionX < 3:
                cx = currentPositionX
            elif currentPositionX > 2:
                cx = 3
            left = [q for q in list(map(lambda z:z.pos,s.body)) if q[1] == currentPositionY and currentPositionX - q[0] < cx and currentPositionX > q[0]]
            for i in range(19,16+cx,-1):
                if (i,currentPositionY) in list(map(lambda z:z.pos,s.body)): left.append((i,currentPositionY))
            print("left " + str(left))

            cx = 0 # number of the nodes in the left side of the snake
            if currentPositionX > 16 and currentPositionX < 19:
                cx = 19 - currentPositionX
            elif currentPositionX < 17:
                cx = 3
            right = [q for q in list(map(lambda z:z.pos,s.body)) if q[1] == currentPositionY and q[0] - currentPositionX < cx and currentPositionX < q[0]]
            for i in range(3 - cx):
                if (i,currentPositionY) in list(map(lambda z:z.pos,s.body)): right.append((i,currentPositionY))
            print("right " + str(right))

            temp = [] # list of the distances between the snake and the food
            if p[0] == "up": # if the direction is up
                if len(top) and s.curr_dir != "down": # if there is a node in the top of the snake and the snake is not going down
                    priority += len(top) # increase the priority by the number of the nodes in the top of the snake
                    for q in top: # for each node in the top of the snake
                        temp.append(manhattanDistance((currentPositionX,currentPositionY),q,size=rows)) # add the distance between the snake and the node to the list of the distances
                    distance.append(("up",min(temp)))
            elif p[0] == "down": # if the direction is down
                if len(bottom) and s.curr_dir != "up":
                    priority += len(bottom)
                    for q in bottom:
                        temp.append(manhattanDistance((currentPositionX,currentPositionY),q,size=rows))
                    distance.append(("down",min(temp)))
            elif p[0] == "left": # if the direction is left
                if len(left) and s.curr_dir != "right":
                    priority += len(left)
                    for q in left:
                        temp.append(manhattanDistance((currentPositionX,currentPositionY),q,size=rows))
                    distance.append(("left",min(temp)))
            elif p[0] == "right": # if the direction is right 
                if len(right) and s.curr_dir != "left":
                    priority += len(right)
                    for q in right:
                        temp.append(manhattanDistance((currentPositionX,currentPositionY),q,size=rows))
                    distance.append(("right",min(temp)))
            if p[2] in list(map(lambda z:z.pos,s.body)):
                priority += 1
        bestMove.append((p[0],p[1],p[2],priority)) # add the direction, the position of the snake after moving in this direction, the position of the food and the priority to the list of the best moves 
    
    # if the snake is in the top of the screen and the food is in the bottom of the screen 
    if len(distance):
        print(distance)
        minDistance = min(distance, key=lambda t: t[1]) # find the direction with the minimum distance between the snake and the food
        print(minDistance)
        temp = [x[0] for x in distance if x[1] == minDistance[1]] # list of the directions with the minimum distance between the snake and the food
        print(temp)
        for j in temp: # for each direction with the minimum distance between the snake and the food 
            print(j)
            near = bestMove.pop([y[0] for y in bestMove].index(j)) # remove the direction from the list of the best moves
            print(near)
            bestMove.append((near[0],near[1],near[2],near[3]+1)) # add the direction to the list of the best moves with the priority increased by 1 
    bestMove = sorted(bestMove,key = lambda t: (t[3],t[1])) # sort the list of the best moves by the priority and the position of the snake after moving in this direction
    print(bestMove)

    for p in bestMove: # for each direction in the list of the best moves
        print(i)
        if p[0] == "left" and s.curr_dir != "right" and p not in visited: # if the direction is left and the snake is not going right and the snake didn't visit this position before
            print("A")
            s.move(control = "left") # move the snake to the left
            visited.add(p) # add the position to the set of the visited positions
            return 
        elif p[0] == "right" and s.curr_dir != "left" and p not in visited:
            print("B")
            s.move(control = "right")
            visited.add(p)
            return
        elif p[0] == "up" and s.curr_dir != "down" and p not in visited:
            print("C")
            s.move(control = "up")
            visited.add(p)
            return
        elif p[0] == "down" and s.curr_dir != "up" and p not in visited:
            print("D")
            s.move(control = "down")
            visited.add(p)
            return 
        i += 1 # increase the index by 1
    s.move() # if the snake didn't move yet, move the snake in the same direction

def manhattanDistance(p,q,size=0):
    dx = min( abs( q[0] - p[0] ), size - abs( q[0] - p[0] ) )
    dy = min( abs( q[1] - p[1] ), size - abs( q[1] - p[1] ) )
    return dx + dy

def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x += sizeBetween
        y += sizeBetween

        pygame.draw.line(surface, (236, 240, 241), (x, 0), (x, w))
        pygame.draw.line(surface, (236, 240, 241), (0, y), (w, y))

def drawScore(score):
    scoreFont = pygame.font.SysFont('Raleway', 20, bold=True)
    scoreSurface = scoreFont.render('Score : ' + str(score), True, pygame.Color(153, 255, 51))
    scoreRect = scoreSurface.get_rect()
    scoreRect.topleft = (width-120, 10)
    win.blit(scoreSurface, scoreRect)

def drawPressKeyMsg():
    pressFont = pygame.font.SysFont('Raleway', 25)
    pressKeySurf = pressFont.render('Press a key to play.', True, (255, 255, 255))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.midtop = (250, 350)
    win.blit(pressKeySurf, pressKeyRect)

def redrawWindow(lose = False):
    win.fill((0,0,0))
    s.draw(win)
    snack.draw(win,food=True)
    if (not(lose)):
        drawGrid(width,rows, win)
    drawScore(len(s.body)-1)
    pygame.display.update()

def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def showGameOverScreen():
    gameOverFont = pygame.font.SysFont("courier new", 150)
    gameSurf = gameOverFont.render('Game', True, pygame.Color(255, 255, 255))
    overSurf = gameOverFont.render('Over', True, pygame.Color(255, 255, 255))
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (width / 2, 10)
    overRect.midtop = (width / 2, gameRect.height + 10 + 25)

    win.blit(gameSurf, gameRect)
    win.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get() 
            return

def checkForKeyPress():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        pygame.quit()
        sys.exit()
    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyUpEvents[0].key

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
    clock = pygame.time.Clock()
    visited = set({})

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        bfsAlgorithm()
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