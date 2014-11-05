#/usr/bin/python
#####################################
#          ATARI BREAKOUT           #
#                                   #
#          Python code by           #
#           Adam Knuckey            #
#               2013                #
#                                   #
#    Original Game by Atari, inc    #
#                                   #
#  Controls:                        #
#  -arrow keys/mouse to move paddle #
#  -spacebar to launch ball         #
#  -enter key to use menu           #
#                                   #
#  Scoring:                         #
#  -Green and blue rows...........1 #
#  -Yellow and lower orange rows..4 #
#  -Upper orange and red rown.....7 #
#                                   #
#####################################

#Add mouse controls
#add half size paddle after hitting back wall

import math,pygame,sys,shutil,getpass
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((640,480)) #create screen - 640 pix by 480 pix
pygame.display.set_caption('Breakout') #set title bar

#add the font; use PressStart2P, but otherwise default if not available
try:
    fontObj = pygame.font.Font('PressStart2P.ttf',36)
except:
    fontObj = pygame.font.Font('freesansbold.ttf',36)

#generic colors-------------------------------
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
grey = pygame.Color(142,142,142)
black = pygame.Color(0,0,0)

#row colors-----------------------------------
r1 = pygame.Color(200,72,72)
r2 = pygame.Color(198,108,58)
r3 = pygame.Color(180,122,48)
r4 = pygame.Color(162,162,42)
r5 = pygame.Color(72,160,72)
r6 = pygame.Color(67,73,202)
colors = [r1,r2,r3,r4,r5,r6]

#variables------------------------------------
controls = 'keys' #control method
mousex,mousey = 0,0 #mouse position
dx,dy = 18,6 #dimensions of board
bx,by = 50,150 #board position
score = 0 #score
wall1 = pygame.Rect(20,100,30,380) #walls of the game
wall2 = pygame.Rect(590,100,30,380)
wall3 = pygame.Rect(20,80,600,30)

#Creates a board of rectangles----------------
def new_board():
    board = []
    for x in range(dx):
        board.append([])
        for y in range(dy):
            board[x].append(1)
    return board
          
#Classes defined------------------------------ 
class Paddle: #class for paddle vars
    x = 320
    y = 450
    size = 2 #2 is normal size, 1 is half-size
    direction = 'none'

class Ball: #class for ball vars
    x = 0
    y = 0
    remaining = 3
    xPos = 1 #amount increasing by for x. adjusted for speed
    yPos = 1
    adjusted = False #says wether the xPos and yPos have been adjusted for speed
    speed = 5
    collisions = 0
    alive = False
    moving = False
    def adjust(self): #adjusts the x and y being added to the ball to make the hypotenuse the ball speed
        tSlope = math.sqrt(self.xPos**2 + self.yPos**2)
        self.xPos = (self.speed / tSlope) * self.xPos
        self.yPos = (self.speed / tSlope) * self.yPos
        self.adjusted = True

#Functions defined----------------------------
def print_board(board,colors): #prints the board
    for x in range(dx):
        for y in range(dy):
            if board[x][y] == 1:
                pygame.draw.rect(screen,colors[y],(((x*30)+bx),((y*12)+by),30,12))
          
def print_paddle(paddle): #prints the paddle
    if paddle.size == 2:
        pygame.draw.rect(screen,red,((paddle.x-20),(paddle.y),40,5))

def collide_paddle(paddle,ball): #recalculates the trajectory for the ball after collision with the paddle
    ball.adjusted = False
    if ball.x - paddle.x != 0:
        ball.xPos = (ball.x-paddle.x) / 8
        ball.yPos = -1
    else:
        ball.xPos = 0
        ball.yPos = 1
    return ball.adjusted,float(ball.xPos), float(ball.yPos)

def write(x,y,color,msg): #prints onto the screen in selected font
    msgSurfaceObj = fontObj.render(msg, False, color)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (x,y)
    screen.blit(msgSurfaceObj,msgRectobj)

def game(score,paddle,ball,board,wall1): #The game itself
    #starting variables
    running = True
    ball.alive = True
    ball.moving = False
    ball.x = 53
    ball.y = 300
    ball.collisions, ball.speed = 0,5
    colO = False #check collision with the orange row, for speed purposes
    colR = False #same but for red row
    ball.speed = 5
    ball.xPos = 1
    ball.yPos = 1
    ball.adjusted = False
          
    while running == True:
        #Draw all the things------------------------------
        screen.fill(black)
        pygame.draw.rect(screen,grey,wall1)
        pygame.draw.rect(screen,grey,wall2)
        pygame.draw.rect(screen,grey,wall3)
        pygame.draw.rect(screen,red,(ball.x-3,ball.y-3,6,6))
        print_board(board,colors)
        print_paddle(paddle)
        write(20,20,grey,str(score))
        temp = 0
        for life in range(ball.remaining):
            if life != 0:
                pygame.draw.rect(screen,red,(600,400-temp,10,10))
                temp += 15

        #check all the collisions-------------------------
        if ball.moving == True:
            if ball.adjusted == False:
                ball.adjust()
            ball.x += ball.xPos
            ball.y += ball.yPos
            if ball.y < 455 and ball.y > 445:
                if ball.x > paddle.x-20 and ball.x < paddle.x+20:
                    ball.adjusted, ball.xPos, ball.yPos = collide_paddle(paddle,ball)#paddle collide
                    ball.collisions += 1
                    #increase ball speeds at 4 hits on paddle, 12 hits, orange row, red row
                    if ball.collisions == 4:
                        ball.speed += 1
                    if ball.collisions == 12:
                        ball.speed += 1
                    #if ball hits the back wall, paddle cuts in half
            #check wall collide----------------------------
            if wall1.collidepoint(ball.x,ball.y) == True or wall2.collidepoint(ball.x,ball.y):
                ball.xPos = -(ball.xPos)
            if wall3.collidepoint(ball.x,ball.y) == True:
                ball.yPos = -(ball.yPos)

            #check collision with bricks-------------------
            Break = False
            for x in range(dx):
                for y in range(dy):
                    if board[x][y] == 1:
                        block = pygame.Rect(30*x+bx-1,12*y+by-1,32,14)
                        if block.collidepoint(ball.x,ball.y) == True:
                            board[x][y] = 0
##                            if y*12+by+12 < ball.y: FIX THIS ITS THE BLOCK BUG
##                                ball.y = -(ball.y)
##                            elif x*30+bx+30 < 
                            ball.yPos = -ball.yPos #Cheat
                            if y == 4 or y == 5:
                                score += 1
                            elif y == 2 or y == 3:
                                score += 4
                                if colO == False:
                                    colO = True
                                    ball.speed+= 1
                            else:
                                score += 7
                                if colR == False:
                                    colR= True
                                    ball.speed+= 2
                            Break = True
                    if Break == True:
                        break
                if Break == True:
                    break
            if ball.y > 460:
                ball.alive = False
          
        #check if ball was lost
        if ball.alive == False:
            running = False
            ball.remaining -= 1
          
        #move paddle
        if paddle.direction == 'right':
            if paddle.x <= 561:
                paddle.x += 8
        elif paddle.direction == 'left':
            if paddle.x >= 79:
                paddle.x -= 8

        #get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEMOTION:
                mx,my = event.pos
            elif event.type == MOUSEBUTTONUP:
                mx,my = event.pos

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    paddle.direction = 'left'
                if event.key == K_RIGHT:
                    paddle.direction = 'right'
                if event.key == K_SPACE:
                    if ball.moving == False:
                        ball.moving = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    if paddle.direction == 'left':
                        paddle.direction = 'none'
                if event.key == K_RIGHT:
                    if paddle.direction == 'right':
                        paddle.direction = 'none'
          
        #update display
        pygame.display.update()
        fpsClock.tick(30)
    return score
def get_highscore(score):
    place = 20
    
    f = open('/Users/'+getpass.getuser()+'/Library/scores.txt','r')
    f.seek(0)
    r = f.readlines()
    count = 0
    evens = [0,2,4,6,8,10,12,14,16,18]
    for line in r:
        if count in evens:
            if score > int(line):
                place -= 2
        count += 1
    if place < 20:
        name = high_score_board()
        r = shove_row(name,place,r)

        f.close()
        f = open('/Users/'+getpass.getuser()+'/Library/scores.txt','w')
        f.writelines(r)

    f.close()

def shove_row(name,place,r):
    for line in range(len(r)):
        l = 19-line
        if place <= l-1:
            r[l] = str(r[l-2])
            r[l-1] = str(r[l-3])
        else:
            break

    r[place] = adjusted_score(score)
    r[place+1] = name + '\n'

    return r
    
def adjusted_score(score):
    if score < 10:
        a = '0'+'0'+'0'+'0' +  str(score)+'\n'
    elif score <100:
        a = '0'+'0'+'0'+str(score)+'\n'
    elif score < 1000:
        a = '0'+'0'+str(score)+'\n'
    elif score < 10000:
        a = '0'+str(score)+'\n'
    else:
        a = '99999'+'\n'
    return str(a)

def high_score_board():
    picked = False
    name = []
    loop = 0
    while picked == False:
        screen.fill(black)
        write(60,40,red,'New Highscore!')
        write(100,100,grey,'Name:')
        pygame.draw.line(screen,grey,(110,240),(140,240),2)
        pygame.draw.line(screen,grey,(150,240),(180,240),2)
        pygame.draw.line(screen,grey,(190,240),(220,240),2)
        
        if len(name) == 0:
            pygame.draw.rect(screen,grey,(110,200,3,36))
        elif len(name) == 1:
            pygame.draw.rect(screen,grey,(150,200,3,36))
            write(110,200,grey,name[0])
        elif len(name) == 2:
            pygame.draw.rect(screen,grey,(190,200,3,36))
            write(110,200,grey,name[0])
            write(150,200,grey,name[1])
        elif len(name) == 3:
            write(110,200,grey,name[0])
            write(150,200,grey,name[1])
            write(190,200,grey,name[2])

        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYDOWN:
                if len(name) < 3:
                    if event.key == K_a:
                        name.append('A')
                    if event.key == K_b:
                        name.append('B')
                    if event.key == K_c:
                        name.append('C')
                    if event.key == K_d:
                        name.append('D')
                    if event.key == K_e:
                        name.append('E')
                    if event.key == K_f:
                        name.append('F')
                    if event.key == K_g:
                        name.append('G')
                    if event.key == K_h:
                        name.append('H')
                    if event.key == K_i:
                        name.append('I')
                    if event.key == K_j:
                        name.append('J')
                    if event.key == K_k:
                        name.append('K')
                    if event.key == K_l:
                        name.append('L')
                    if event.key == K_m:
                        name.append('M')
                    if event.key == K_n:
                        name.append('N')
                    if event.key == K_o:
                        name.append('O')
                    if event.key == K_p:
                        name.append('P')
                    if event.key == K_q:
                        name.append('Q')
                    if event.key == K_r:
                        name.append('R')
                    if event.key == K_s:
                        name.append('S')
                    if event.key == K_t:
                        name.append('T')
                    if event.key == K_u:
                        name.append('U')
                    if event.key == K_v:
                        name.append('V')
                    if event.key == K_w:
                        name.append('W')
                    if event.key == K_x:
                        name.append('X')
                    if event.key == K_y:
                        name.append('Y')
                    if event.key == K_z:
                        name.append('Z')
                if event.key == K_BACKSPACE:
                        name.remove(name[len(name)-1])
                if event.key == K_RETURN:
                    if len(name) == 3:
                        picked = True
        pygame.display.update()
    name = str(name[0]+name[1]+name[2])
    
    return name
def print_highscore_board():
    try:
        f = open('/Users/'+getpass.getuser()+'/Library/scores.txt','r')
    except:    
        print 'create new highscores file'
        n = '00000\n---\n00000\n---\n00000\n---\n00000\n---\n00000\n---\n00000\n---\n00000\n---\n00000\n---\n00000\n---\n00000\n---\n'
        shutil.move('scores.txt','/Users/'+getpass.getuser()+'/Library')
        f = open('/Users/'+getpass.getuser()+'/Library','w')
        f.write(n)
        f.close()
        #shutil.move('scores.txt','/Library')
        f = open('/Users/'+getpass.getuser()+'/Library/scores.txt','r')
    r = f.readlines()
    yPos = 0
    evens = [0,2,4,6,8,10,12,14,16,18,20]
    for score in range(19):
        if score in evens:
            write(200,100+yPos,grey,str(r[score].replace('\n','')+" - "+r[score+1].replace('\n','')))
            yPos += 25

#-----------------------------------------------------
if __name__ == '__main__':
    replay = False
    loop = 0
    try:
        fontObj = pygame.font.Font('PressStart2P.ttf',24)
    except:
        fontObj = pygame.font.Font('freesansbold.ttf',24)
    while True:
        screen.fill(black)
        if replay == True:
            board = new_board()
            score = 0
            try:
                fontObj = pygame.font.Font('PressStart2P.ttf',36)
            except:
                fontObj = pygame.font.Font('freesansbold.ttf',36)
            paddle = Paddle()
            ball = Ball()
            while ball.remaining > 0:
                score = game(score,paddle,ball,board,wall1)
                if ball.remaining == 0:
                    for x in range(16):
                        for y in range(12):
                            pygame.draw.rect(screen,black,(x*40,y*40,40,40))
                            pygame.display.update()
                            pygame.time.wait(10)
                            boardcheck = 0
                    for x in range(len(board)):
                        for y in range(len(board[x])):
                            boardcheck += board[x][y]
                    if boardcheck == 0:
                        paddle = Paddle()
                        ball = Ball()
                        board = new_board()
                        while ball.remaining > 0:
                            score = game(score,paddle,ball,board,wall1)
                            if ball.remaining == 0:
                                for x in range(16):
                                    for y in range(12):
                                        pygame.draw.rect(screen,black,(x*40,y*40,40,40))
                                        pygame.display.update()
                                        pygame.time.wait(10)
                            
                    get_highscore(score)
                    replay = False
                    try:
                        fontObj = pygame.font.Font('PressStart2P.ttf',24)
                    except:
                        fontObj = pygame.font.Font('freesansbold.ttf',24)
        write(200,20,grey,'Highscores')
        print_highscore_board()
        if loop < 18:
            write(80,400,grey,'-Press Enter To Play-')
        elif loop == 30:
            loop = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    replay = True
        loop += 1
        pygame.display.update()

