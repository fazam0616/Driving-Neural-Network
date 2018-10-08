import pygame
import time
import math
import sys

pygame.init()

displayWidth = 600
displayHeight = 600

global screen
screen = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Math Testing')

original = pygame.transform.scale(pygame.image.load("Car.png"),(80,80))
rectangle = original

right = False
left = False

ogpoint1X = 40/2
ogpoint1Y = 80/2

ogpoint2X = -40/2
ogpoint2Y = 80/2

ogpoint3X = -40/2
ogpoint3Y = -80/2

ogpoint4X = 40/2
ogpoint4Y = -80/2

point1X = ogpoint1X
point1Y = ogpoint1Y

point2X = ogpoint2X
point2Y = ogpoint1Y

point3X = ogpoint3X
point3Y = ogpoint1Y

point4X = ogpoint4X
point4Y = ogpoint1Y

def mathToScreen(x,y):
    newY = -(y-(displayHeight / 2))
    newX = x + (displayWidth / 2)
    return (round(newX),round(newY))

def sin(angle):
    return math.sin(math.radians(angle))

def cos(angle):
    return math.cos(math.radians(angle))

angle = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right = True
            elif event.key == pygame.K_a:
                left = True

            if event.key == pygame.K_r:
                angle = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_a:
                left = False

    if right:
        angle -= .5
    elif left:
        angle += .5

    for i in range (1,5): 
        exec("""
x = ogpoint"""+str(i)+"""X
y = ogpoint"""+str(i)+"""Y

point"""+str(i)+"""X = x*cos(angle) - y*sin(angle)
point"""+str(i)+"""Y = x*cos(angle) + y*sin(angle)
    """)
    rectangle = pygame.transform.rotozoom(original,angle,1)

    screen.fill((0,0,0))
    screen.blit(rectangle,(300 - 20,300 - 40))
    for i in range(1,5):
        exec("""
pygame.draw.circle(screen,(0,"""+str(i)+"""*63,0),mathToScreen(point"""+str(i)+"""X,point"""+str(i)+"""Y),5,0)
""")
    pygame.draw.circle(screen,(255,0,0),(300,300),45,1)
    pygame.display.update()
