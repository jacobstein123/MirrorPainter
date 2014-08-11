#Copyright Jacob Stein 2013

import pygame
from pygame.locals import *
import sys
import random
import os

def pick_color():

    DISPLAYSURF = pygame.Surface((600, 480))

    FPS = 30
    fpsClock = pygame.time.Clock()

    text16 = pygame.font.Font("freesansbold.ttf", 16)

    def show_palette(surface, color_dict):
            square_size = 20
            left = 0
            top = 0
            for color in color_dict:
                    pygame.draw.rect(surface, color_dict[color],(left, top, square_size, square_size))
                    left += square_size
                    if left + square_size > surface.get_width():
                            top += square_size
                            left = 0

    def color_picker():
            text_blits = []
            color_names = []
            while True:
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                    x, y = event.pos
                                    try:
                                        current_color = DISPLAYSURF.get_at((x-150, y-80))
                                    except IndexError:
                                        break
                                    color_names = []
                                    text_blits = []
                                    for key, value in pygame.color.THECOLORS.items():
                                            if value == current_color:
                                                    color_names.append(key)
                                                    return value

                    left = 0
                    top = 450
                    for name in color_names:
                            name_text = text16.render("{0}".format(name), True, Color("white"), Color("black"))
                            name_rect = name_text.get_rect(topleft = (left, top))
                            left = name_rect.right + 20
                            text_blits.append((name_text, name_rect))

                    DISPLAYSURF.fill(Color("black"))
                    show_palette(DISPLAYSURF, pygame.color.THECOLORS)
                    for elem in text_blits:
                            DISPLAYSURF.blit(elem[0], elem[1])
                    screen.blit(DISPLAYSURF,(150,80))
                    pygame.display.update()
                    fpsClock.tick(FPS)
    return color_picker()

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900,600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MirrorPainter")
HORIZONTAL = 1
VERTICAL = -1
draw = False
mousex = mousey = 0
previous_x = mousex
previous_y = mousey
screen.fill(pygame.Color('black'))
just_started_drawing = True
color = pygame.Color('white')
bar = pygame.image.load('bar.png').convert()
screen.blit(bar,(0,0))

erase = pygame.Rect(168,8,60,30)
pick_color_button = pygame.Rect(248,8,98,30)
undo = pygame.Rect(367,8,60,30)
redo = pygame.Rect(447,8,60,30)
switch_mirror = pygame.Rect(528,8,123,30)
save = pygame.Rect(673,8,60,30)
mirror = HORIZONTAL
moves = []
undo_index = 0
saved = False
#font = pygame.font.Font('fonts/Roboto-Light',50)
#saved_text =
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if event.pos[1] > 50:
                draw = True
                undo_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
                undo_surface.blit(screen,(0,0))
                moves.append(undo_surface)
                if len(moves) > 5:
                    moves = moves[1:]
                undo_index = 0
            else:
                if erase.collidepoint(mousex,mousey):
                    undo_surface.blit(screen,(0,0))
                    moves.append(undo_surface)
                    if len(moves) > 5:
                        moves = moves[1:]
                    undo_index = 0
                    screen.fill(pygame.Color('black'))
                if pick_color_button.collidepoint(mousex,mousey):
                    saved_drawing = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
                    saved_drawing.blit(screen,(0,0))
                    color =  pick_color()
                    screen.blit(saved_drawing,(0,0))
                if undo.collidepoint(mousex,mousey):
                    if undo_index == 0:
                        redo_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
                        redo_surface.blit(screen,(0,0))
                        redo_moves = moves[1:] + [redo_surface]
                    if undo_index > -len(moves):
                        undo_index -= 1
                        screen.blit(moves[undo_index],(0,0))
                if redo.collidepoint(mousex,mousey):
                    if undo_index < 0:
                        screen.blit(redo_moves[undo_index],(0,0))
                        undo_index += 1
                if switch_mirror.collidepoint(mousex,mousey):
                    mirror *= -1
                if save.collidepoint(mousex,mousey):
                    final_image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT-50))
                    final_image.blit(screen,(0,-50))
                    files = os.listdir('saves')
                    print files
                    i = 1
                    while any([str(i) in j for j in files]):
                        i += 1
                        #print [str(i) in j for j in files]
                    pygame.image.save(final_image,'.\saves\image%i.jpg'%i)

        if event.type == MOUSEBUTTONUP:
            draw = False
            just_started_drawing = True
        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            if mousex == mousey == 0:
                previous_x, previous_y = mousex, mousey
    if draw:
        if not just_started_drawing:
            pygame.draw.line(screen,color,(previous_x,previous_y), (mousex, mousey),6)
            if mirror == HORIZONTAL:
                pygame.draw.line(screen,color,(900-previous_x,previous_y), (900-mousex, mousey),6)
            else:
                pygame.draw.line(screen,color,(previous_x,650-previous_y), (mousex, 650-mousey),6)
        previous_x, previous_y = mousex, mousey
        just_started_drawing = False

    screen.blit(bar,(0,0))
    pygame.display.update()