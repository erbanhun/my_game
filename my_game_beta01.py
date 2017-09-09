# snake game in python

import pygame, sys, time, random

# check for initialising error
check_error = pygame.init()
if check_error[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_error[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized")

# Play Surface
W = 500
H = 300
playSurface = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake & Pingpang Game (Beta 01) ----:>')
#time.sleep(5)

# Colors
red = pygame.Color(255,0,0)#gameOver
green = pygame.Color(0,255,0)#Snake
black = pygame.Color(0,0,0)#Score
white = pygame.Color(255,255,255)#background
brown = pygame.Color(162,42,42)#food

# FPS Controller
fpsController = pygame.time.Clock()

# Important Variables
snakePos = [100,50] # start position
snakeBody = [[100,50],[90,50],[80,50]] #,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

foodPos = [random.randrange(1,W/10)*10, random.randrange(1,H/10)*10] # food positon
foodSpawn = True    # regenerate a food signal
'''
    Pingpang part var
'''
Pingpang_PosGen = [random.randrange(1, W/10) * 10, random.randrange(1, H/10) * 10]
Pingpang_Pos = [Pingpang_PosGen]
Pingpang_No = 1
Pingpang_V = [[random.choice([-1,1]), random.choice([-1,1])]] # pingpang direction

direction = 'RIGHT'
changeTo = direction

score = 0

#Game Over Function
def gameOver(W, H):
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (W/2,H/3)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# score function
def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score : {0}'.format(score), True, black)
    #Tip = sFont.render('Esc to quit ' )
    Srect = Ssurf.get_rect()
    if choice ==1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 150)

    playSurface.blit(Ssurf, Srect)
    #playSurface. bilt(Tip)

def showTip(W, H):
    myFont = pygame.font.SysFont('monaco', 24)
    Tip_surf = myFont.render('Esc to quit', True, red)
    Tip_rect = Tip_surf.get_rect()
    Tip_rect.midtop = (W-100,15)
    playSurface.blit(Tip_surf, Tip_rect)

def new_pingpang(W, H):
    pos = [random.randrange(1, W/10) * 10, random.randrange(1, H/10) * 10]
    v = [random.choice([-1,1]), random.choice([-1,1])] # pingpang direction
    return pos, v
'''
    Main Logic Of Game ==================================
'''
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Validation of direction
    if changeTo == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeTo == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
    # speed in 4 direction
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    # pingpang run
    for i in range(0, Pingpang_No):
        #print(i)
        Pingpang_Pos[i][0] += 10 * Pingpang_V[i][0]
        Pingpang_Pos[i][1] += 10 * Pingpang_V[i][1]
    # pignpang reflect when touch boundary
    for i in range(0, Pingpang_No):
        if (Pingpang_Pos[i][0] > W and Pingpang_V[i][0] == 1)or (Pingpang_Pos[i][0] < 0 and Pingpang_V[i][0] == -1):
            Pingpang_V[i][0] = -Pingpang_V[i][0]
        if(Pingpang_Pos[i][1] > H and Pingpang_V[i][1] == 1) or (Pingpang_Pos[i][1] < 0 and Pingpang_V[i][1] == -1):
            Pingpang_V[i][1] = -Pingpang_V[i][1]

    # snake body mechanism
    snakeBody.insert(0, list(snakePos)) #insert a square(at the head of list)
    #print(snakeBody)

    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score+=10
        foodSpawn = False
        pos, v = new_pingpang(W, H)
        Pingpang_Pos += [pos]
        Pingpang_V += [v]
        Pingpang_No += 1
        print("===============")
        print(Pingpang_Pos, "\n---------", Pingpang_V)
    else:
        snakeBody.pop()

    if foodSpawn == False:
        foodPos = [random.randrange(1, W/10) * 10, random.randrange(1, H/10) * 10]

    foodSpawn = True

    playSurface.fill(white)
    for pos in snakeBody:
        pygame.draw.rect(playSurface,green,pygame.Rect(pos[0], pos[1],10,10)) # snakebody shape

    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))
    # show pingpang in screen
    print(Pingpang_Pos)
    print(Pingpang_No)
    for i in range(0, Pingpang_No):
        pygame.draw.rect(playSurface, black, pygame.Rect(Pingpang_Pos[i][0], Pingpang_Pos[i][1],10,10))
        if snakePos[0] == Pingpang_Pos[i][0] and snakePos[1] == Pingpang_Pos[i][1]:
            gameOver(W, H) # snake attacked by pingpang to die
    # touch the boundary to die
    if snakePos[0] > W or snakePos[0] < 0:
        gameOver(W, H)
    if snakePos[1] > H or snakePos[1] < 0:
        gameOver(W, H)
    # touch itself to die
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver(W, H)
    '''
        tochu the ball to die 1
    '''

    showScore( 1)
    showTip(W, H)
    pygame.display.flip()
    fpsController.tick(10)

    #pygame.display.update()
