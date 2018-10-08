import math
import sys
import pygame
import time

pygame.init()

displayWidth = 600
displayHeight = 600

global screen
screen = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Neural Network: Driving')

pygame.font.init()
basicfont = pygame.font.SysFont(None, 30)

backgroundLeft = pygame.image.load("Training Course Left.png")
backgroundRight = pygame.image.load("Training Course Right.png")

class Pos():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def screenToMath(self,x,y):
        newY = -(y-(displayHeight / 2))
        newX = x - (displayWidth / 2)
        return (newX,newY)
    
    def mathToScreen(self,x,y):
        newY = -(y-(displayHeight / 2))
        newX = x + (displayWidth / 2)
        return (round(newX),round(newY))

class Car():
    def __init__(self):
        self.pos = Pos(880,520)
        self.speed = 0
        self.angle = -90
        
        self.point1 = Pos(-10,20)
        self.point2 = Pos(10,20)
        self.point3 = Pos(-10,-20)
        self.point4 = Pos(10,-20)

        self.OGpoint1 = Pos(-10,20)
        self.OGpoint2 = Pos(10,20)
        self.OGpoint3 = Pos(-10,-20)
        self.OGpoint4 = Pos(10,-20)

        self.colour = (0,255,0)

    def rotatePoint(self,angle):
        angle += 90
        for i in range(1,5):
            exec("""
xold = player.point"""+str(i)+""".x
yold = player.point"""+str(i)+""".y

OGx = player.OGpoint"""+str(i)+""".x
OGy = player.OGpoint"""+str(i)+""".y

xold = round(OGx*cos(angle) - OGy*sin(angle))
yold = round(OGx*sin(angle) + OGy*cos(angle))

player.point"""+str(i)+""" = Pos(xold,yold)
""")
        
def drawLines(car):
    pygame.draw.line(screen,car.colour,Pos.mathToScreen(Pos,car.point1.x,car.point1.y),Pos.mathToScreen(Pos,car.point2.x,car.point2.y),5)
    pygame.draw.line(screen,car.colour,Pos.mathToScreen(Pos,car.point2.x,car.point2.y),Pos.mathToScreen(Pos,car.point4.x,car.point4.y),5)
    pygame.draw.line(screen,car.colour,Pos.mathToScreen(Pos,car.point3.x,car.point3.y),Pos.mathToScreen(Pos,car.point1.x,car.point1.y),5)
    pygame.draw.line(screen,car.colour,Pos.mathToScreen(Pos,car.point4.x,car.point4.y),Pos.mathToScreen(Pos,car.point3.x,car.point3.y),5)
        
def cos(angle):
    return(math.cos(math.radians(angle)))

def sin(angle):
    return(math.sin(math.radians(angle)))

def collision(point):
    global screen
    if screen.get_at(Pos.mathToScreen(Pos,point.x,point.y)) == (1, 1, 1, 255):
        print((point.x,point.y))
        return True
    else:
        return False

player = Car()

forward = 0
turn = 0



while True:
    startTime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                forward = 0.05
            if event.key == pygame.K_s:
                forward = -0.05

            if event.key == pygame.K_d:
                turn = 0.3
            if event.key == pygame.K_a:
                turn = -0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                forward = 0
           
            if event.key == pygame.K_d or event.key == pygame.K_a:
                turn = 0

    screen.fill((255,255,255))
    screen.blit(backgroundLeft,(player.pos.mathToScreen(-player.pos.x,player.pos.y)[0],-player.pos.mathToScreen(player.pos.x,player.pos.y)[1]))
    screen.blit(backgroundRight,(player.pos.mathToScreen(-player.pos.x,player.pos.y)[0],-player.pos.mathToScreen(player.pos.x,player.pos.y)[1]))
    
    if forward != 0:
        player.speed += forward
    player.speed *= 0.995
    
    
    if player.angle > 360:
        player.angle -= 360
    if turn !=0 and player.speed != 0:
        player.angle -= turn / (1/player.speed)
        change = -turn / (1/player.speed)
        player.speed *= 0.997

    
    player.rotatePoint(player.angle)
    player.pos.x += math.cos(math.radians(player.angle)) * player.speed
    player.pos.y += math.sin(math.radians(player.angle)) * player.speed
    
    if collision(player.point1) or collision(player.point2) or collision(player.point3) or collision(player.point4):
        
        player.pos = Pos(880,520)
        player.speed = 0
        player.angle = -90
        forward = 0
        turn = 0
                
    for i in range(1,5):
        exec("""
pygame.draw.circle(screen,player.colour,((Pos.mathToScreen(Pos,player.point"""+str(i)+""".x,player.point"""+str(i)+""".y))),2,0)
""")
    drawLines(player)
    
    endTime = time.time()
    if (endTime - startTime > 0):
        fps = round(1/(endTime - startTime),2)
    else:
        fps = "Infinity"
    informationScreen = basicfont.render("FPS: "+str(fps), True, (255, 0, 0))
    screen.blit(informationScreen,(0,0))
    pygame.display.update()
    
