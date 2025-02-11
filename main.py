import pygame
import sys
import random
import time

pygame.init()
random.seed(0)

screen_width = pygame.display.Info().current_w//1.5
screen_height = screen_width//(4/3)
screen_center = (round(screen_width*0.5),round(screen_height*0.5))
font = pygame.font.Font('freesansbold.ttf', 32)
letters = [None,"E","D","C","B","A","S"]
element = [[(98,157,209),(172,203,249),(74,102,172)]]
mos_pos = []
card_objects = []
true_deck = []
game_run = True

def innit_screen(width=500,height=500):
    global screen
    screen = pygame.display.set_mode((width, height))
    screen.fill((200,200,200))

def display_hand(hand):
    for i,card in enumerate(hand):
        card.center_x = screen_center[0]+(card.width+20)*(i-len(hand)//2)
        card.center_y = screen_center[1]+(screen_width//6)
        card.update_rect(screen_center[0]+(card.width+card.padding)*(i-len(hand)//2),screen_center[1]+(screen_width//6))
        card.draw()

class Card:
    def __init__(self, type_l=1, type_n=1):
        self.type_l = type_l
        self.type_n = type_n
        self.center_x = 0
        self.center_y = 0
        self.width = round(screen_width//10)
        self.height = round(self.width*(4/3))
        self.padding = round(self.width//7)
        self.rect = (self.center_x-self.width//2, self.center_y-self.height//2, self.width, self.height)
        self.hitbox = self.rect
        self.colour_inner = (51, 231, 247) #(92, 125, 124) (51, 231, 247)
        self.colour_outer = (max(0,self.colour_inner[0]-40), max(0,self.colour_inner[1]-40), max(0,self.colour_inner[2]-40))
        self.colour = self.colour_inner
        self.selected = False
    
    def __str__(self):
        return f"Card is {self.number_to_letter()}:{self.type_n}"
    
    def update_rect(self, x, y):
        self.center_x = x
        self.center_y = y
        self.rect = (self.center_x-self.width//2, self.center_y-self.height//2, self.width, self.height)
        self.hitbox = self.rect

    def hover(self, hovering):
        if hovering:
            self.rect = (self.hitbox[0], self.hitbox[1]-self.padding*3, self.hitbox[2], self.hitbox[3])
            self.colour_inner = (min(255,self.colour[0]+40), min(255,self.colour[1]+40), min(255,self.colour[2]+40))
        elif self.selected:
            self.rect = (self.hitbox[0], self.hitbox[1]-self.padding*3, self.hitbox[2], self.hitbox[3])
            self.colour_inner = (self.colour[0], self.colour[1], self.colour[2])
        else:
            self.rect = (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3])
            self.colour_inner = (self.colour[0], self.colour[1], self.colour[2])

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
            
    def draw_rounded_rect(self):
        pygame.draw.rect(screen, self.colour_outer, self.rect, 0, round(self.padding*1.5), round(self.padding*1.5), round(self.padding*1.5), round(self.padding*1.5))
        pygame.draw.rect(screen, self.colour_inner, (self.rect[0]+round(self.padding*0.5),self.rect[1]+round(self.padding*0.5), round(self.rect[2]-self.padding), round(self.rect[3]-self.padding)), 0, self.padding, self.padding, self.padding, self.padding)

    def draw(self):
        self.draw_rounded_rect()
        text = pygame.font.Font('freesansbold.ttf', self.width//2).render(str(letters[self.type_l]), True, self.colour_outer)
        textRect = text.get_rect()
        textRect.center = (self.rect[0]+self.rect[2]//4,self.rect[1]+self.rect[3]//4)
        screen.blit(text, textRect)
        text = pygame.font.Font('freesansbold.ttf', self.width//2).render(str(self.type_n), True, self.colour_outer)
        textRect = text.get_rect()
        textRect.center = (self.rect[0]+round(3/4*self.rect[2]),self.rect[1]+round(3/4*self.rect[3]))
        screen.blit(text, textRect)

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
    card_objects.clear()
    for i in range(0,7):
        hand.append(random.choice(deck))
        deck.remove(hand[i])
        card_objects.append(hand[i])

    display_hand(hand)

innit_screen(screen_width, screen_height)

for i in range(1,6):
    for j in range(1,6):
        true_deck.append(Card(i,j))

while game_run:

    for event in pygame.event.get():
        key_pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            game_run = False
        if key_pressed[pygame.K_r]:
            play_game()

        mos_pos = pygame.mouse.get_pos()

        for card in card_objects:
            if card.hitbox[0] <= mos_pos[0] <= card.hitbox[0]+card.hitbox[2] and card.hitbox[1] <= mos_pos[1] <= card.hitbox[1]+card.hitbox[3]:
                card.hover(True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    card.selected = not card.selected
            else:
                card.hover(False)

    screen.fill((200,200,200))
    for card in card_objects:
        card.draw()

        #pygame.draw.rect(screen, (255,0,0), card.rect)
        #pygame.draw.rect(screen, (0,0,255), card.hitbox)

    pygame.display.flip()


pygame.quit()
sys.exit()
