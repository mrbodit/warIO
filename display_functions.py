import pygame
import math
from src.global_variables import *
def display_hero(hero,screen):
    pygame.draw.circle(screen, hero.color, (round(hero.position_x), round(hero.position_y)), hero.radius, 0)
    pygame.draw.circle(screen, (0, 0, 0), (round(hero.position_x) + round(7 * math.cos(hero.angle)), round(hero.position_y) + round(7 * math.sin(hero.angle))),3, 0)

def display_bullet(bullet,screen):
    if bullet != None:
        pygame.draw.circle(screen, (200, 55, 75), (round(bullet.position_x), round(bullet.position_y)), BULLET_RADIUS, 0)

def display_text(screen,x,y,text,r,g,b,f):
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('freesansbold.ttf', f)
    textsurface = myfont.render(text, True, (r, g, b))
    text_rect = textsurface.get_rect(center=(x, y))
    screen.blit(textsurface, text_rect)

def display_network(screen,x,y,network,output):
    pygame.init()
    pygame.font.init()
    max_length = 0
    color = [0,0,0]
    space = 55 # odleglosc miedzy neuronami
    for i in range(len(network.all_layers)):
        if len(network.all_layers[i]) > max_length:
            max_length = len(network.all_layers[i])
    middleY = y + max_length * space / 2

    for i in range(len(network.all_layers)):
        drawing_point = round(middleY - (len(network.all_layers[i]) * space / 2))
        for j in range(len(network.all_layers[i])):
            if output[i][j] > 0.5:
                color = [0,255,0]
            else:
                color = [0,0,0]
            pygame.draw.circle(screen, color, (x + i * space * 2, drawing_point + j * space), 25, 2)
            display_text(screen,x + i *space *2,drawing_point + j *space,str(round(output[i][j],2)),0,0,0,20)

def display_magazine(screen,x,y,magazine,reload):
    pygame.init()
    pygame.font.init()
    color = [149,55,255]
    for i in range(magazine + 1):
        if i == 3:
            break
        if i >= magazine:
            if magazine == 3:
                pygame.draw.rect(screen, color, [x + 51 * i - 40, y, 50, 10], 0)
            else:
                pygame.draw.rect(screen, color, [x + 51 * i - 40,y,round((reload/60) * 50),10],0)
        else:
            pygame.draw.rect(screen, color, [x + 51 * i - 40, y, 50, 10], 0)
    display_text(screen, x,y - 5,"Magazynek: ",149,55,255,20)
