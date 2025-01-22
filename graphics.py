import pygame
import sys

pygame.init()

screen_width = 500
screen_height = 500
screen_center = (round(screen_width*0.5),round(screen_height*0.5))
game_run = True

def innit_screen(w,h):
    global screen
    screen = pygame.display.set_mode((w, h))
    screen.fill((200,200,200))

def draw_rounded_rect(center_x,center_y,width,height,padding,colour_outer,colour_inner):
    x = center_x - round(width*0.5)
    y = center_y - round(height*0.5)
    pygame.draw.rect(screen, colour_outer, (x,y, width, height), 0, round(padding*1.5), round(padding*1.5), round(padding*1.5), round(padding*1.5))
    pygame.draw.rect(screen, colour_inner, (x+round(padding*0.5),y+round(padding*0.5), width-padding, height-padding), 0, padding, padding, padding, padding)

innit_screen(screen_width, screen_height)
draw_rounded_rect(screen_height/2, screen_width/2, 100, 150, 20, (50,50,50), (150,150,150))
pygame.draw.circle(screen, (255,0,0),screen_center,5)

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    pygame.display.flip()

pygame.quit()
sys.exit()
