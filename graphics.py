import pygame
import sys

pygame.init()

screen_width = 500
screen_height = 500
screen_center = (round(screen_width*0.5),round(screen_height*0.5))
game_run = True

def innit_screen(width=500,height=500):
    global screen
    screen = pygame.display.set_mode((width, height))
    screen.fill((200,200,200))

def draw_rounded_rect(center_x,center_y,width,height,colour_outer=(45, 69, 68),colour_inner=(92, 125, 124),padding=10):
    x = center_x - round(width*0.5)
    y = center_y - round(height*0.5)
    pygame.draw.rect(screen, colour_outer, (x,y, width, height), 0, round(padding*1.5), round(padding*1.5), round(padding*1.5), round(padding*1.5))
    pygame.draw.rect(screen, colour_inner, (x+round(padding*0.5),y+round(padding*0.5), width-padding, height-padding), 0, padding, padding, padding, padding)

innit_screen(screen_width, screen_height)

draw_rounded_rect(screen_center[0],screen_center[1], 63, 88)

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    pygame.display.flip()

pygame.quit()
sys.exit()
