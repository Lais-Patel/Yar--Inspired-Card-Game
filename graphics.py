import pygame
import sys

pygame.init()

screen_width = 1000
screen_height = 750
screen_center = (round(screen_width*0.5),round(screen_height*0.5))
font = pygame.font.Font('freesansbold.ttf', 32)
letters = [None,"E","D","C","B","A","S"]
element = [[(98,157,209),(172,203,249),(74,102,172)]]
game_run = True

def innit_screen(width=500,height=500):
    global screen
    screen = pygame.display.set_mode((width, height))
    screen.fill((200,200,200))

def draw_rounded_rect(center_x,center_y,width,height,padding=20,colour_outer=(45, 69, 68),colour_inner=(92, 125, 124)):
    x = center_x - round(width*0.5)
    y = center_y - round(height*0.5)
    pygame.draw.rect(screen, colour_outer, (x,y, width, height), 0, round(padding*1.5), round(padding*1.5), round(padding*1.5), round(padding*1.5))
    pygame.draw.rect(screen, colour_inner, (x+round(padding*0.5),y+round(padding*0.5), width-padding, height-padding), 0, padding, padding, padding, padding)

def draw_card(center_x,center_y,width,height,padding=20,type_l=5,type_n=5,colour_inner=(92, 125, 124),colour_outer=(45, 69, 68)):
    draw_rounded_rect(center_x,center_y,width,height,padding,colour_outer,colour_inner)
    text = pygame.font.Font('freesansbold.ttf', padding*5).render(str(letters[type_l]), True, colour_outer)
    textRect = text.get_rect()
    textRect.center = (center_x-width//4,center_y-height//4)
    screen.blit(text, textRect)
    text = pygame.font.Font('freesansbold.ttf', padding*5).render(str(type_n), True, colour_outer)
    textRect = text.get_rect()
    textRect.center = (center_x+width//4,center_y+height//4)
    screen.blit(text, textRect)

innit_screen(screen_width, screen_height)

def display_hand(hand):
    width = 200
    height = 267
    draw_card(screen_center[0]-width*2-40,screen_center[1],width,height,20)
    draw_card(screen_center[0]-width-20,screen_center[1],width,height,20)
    draw_card(screen_center[0],screen_center[1],width,height,20)
    draw_card(screen_center[0]+width+20,screen_center[1],width,height,20)
    draw_card(screen_center[0]+width*2+40,screen_center[1],width,height,20)

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()
