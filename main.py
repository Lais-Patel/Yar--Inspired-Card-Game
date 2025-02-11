import pygame
import sys
import random

pygame.init()
random.seed(0)

screen_width = 1500
screen_height = 1125
screen_center = (round(screen_width*0.5),round(screen_height*0.5))
font = pygame.font.Font('freesansbold.ttf', 32)
letters = [None,"E","D","C","B","A","S"]
element = [[(98,157,209),(172,203,249),(74,102,172)]]
true_deck = []
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
    text = pygame.font.Font('freesansbold.ttf', width//2).render(str(letters[type_l]), True, colour_outer)
    textRect = text.get_rect()
    textRect.center = (center_x-width//4,center_y-height//4)
    screen.blit(text, textRect)
    text = pygame.font.Font('freesansbold.ttf', width//2).render(str(type_n), True, colour_outer)
    textRect = text.get_rect()
    textRect.center = (center_x+width//4,center_y+height//4)
    screen.blit(text, textRect)

def display_hand(hand):
    width = 150
    height = 200
    for i,card in enumerate(hand):
        draw_card(screen_center[0]+(width+20)*(i-len(hand)//2),screen_center[1]+250,width,height,20,card.type_l,card.type_n)
    pygame.Rect(hand[2]).move(20,20)

class Card:
    def __init__(self, type_l, type_n):
        self.type_l = type_l
        self.type_n = type_n
    
    def __str__(self):
        return f"Card is {self.number_to_letter()}:{self.type_n}"
    
    def number_to_letter(self):
        match self.type_l:
            case 1:
                return "E"
            case 2:
                return "D"
            case 3:
                return "C"
            case 4:
                return "B"
            case 5:
                return "A"
            case 6:
                return "S"

def hand_check(values):
    mult = 0
    score = 0
    value_dict = {1:0,2:0,3:0,4:0,5:0}
    dict_values = []

    for value in values:
        value_dict[value] += 1
        score += value
    for key in value_dict:
        dict_values.append(value_dict[key])

    if 5 in dict_values:
        mult = 2
        #print("Five of a Kind")
    elif [1,1,1,1,1] == dict_values:
        mult = 1.9
        #print("Straight")
    elif 4 in dict_values:
        mult = 1.8
        #print("Four of a Kind")
    elif 3 in dict_values and 2 in dict_values:
        mult = 1.6
        #print("Full House")
    elif 2 in dict_values and dict_values.index(2) != (len(dict_values)-dict_values[::-1].index(2)-1):
        mult = 1.5
        #print("Two Pair")
    elif 3 in dict_values:
        mult = 1.45
        #print("Three of a Kind")
    elif 2 in dict_values:
        mult = 1.45
        #print("Two of a Kind")
    else:
        mult = 1
    
    return score*mult

def score_hand(played_hand):
    score_l = 0
    score_n = 0
    letters = []
    numbers = []

    for card in played_hand:
        letters.append(card.type_l)
        numbers.append(card.type_n)

    score_l = hand_check(letters)
    score_n = hand_check(numbers)
    return score_l + score_n

def play_game():
    deck = true_deck.copy()
    hand = []
    for i in range(0,7):
        hand.append(random.choice(deck))
        deck.remove(hand[i])

    display_hand(hand)

innit_screen(screen_width, screen_height)

for i in range(1,6):
    for j in range(1,6):
        true_deck.append(Card(i,j))

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_game()
    pygame.display.flip()


pygame.quit()
sys.exit()
