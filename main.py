import pygame
import sys
import random
import time

pygame.init()

screen_width = pygame.display.Info().current_w//2.5
screen_height = screen_width//(4/3)
screen_center = (round(screen_width*0.5),round(screen_height*0.5))
font = pygame.font.Font('freesansbold.ttf', 32)
letters = [None,"E","D","C","B","A","S"]
element = [[(98,157,209),(172,203,249),(74,102,172)]]
mos_pos = []
card_objects = []
objects = []
true_deck = []
global cards_selected
cards_selected = 0
game_run = True

class TextBox:
    def __init__(self, width=round(screen_width//10), height=round(screen_height//10), name="Text", x=screen_width//2 ,y=screen_height//2):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.name = name
        self.rect = (self.center_x-self.width//2, self.center_y-self.height//2, self.width, self.height)
        self.colour_inner = (92, 125, 124) #(92, 125, 124) (51, 231, 247)
        self.colour_outer = (max(0,self.colour_inner[0]-40), max(0,self.colour_inner[1]-40), max(0,self.colour_inner[2]-40))
        self.colour = self.colour_inner
        self.selected = False

    def draw(self):
        text = pygame.font.Font('freesansbold.ttf', round(min(self.width//1.5,self.height//1.5))).render(self.name, True, self.colour_outer)
        textRect = text.get_rect()
        textRect.center = (self.center_x,self.center_y)
        screen.blit(text, textRect)

class Button:
    def __init__(self, width=round(screen_width//10), height=round(screen_height//10), name="Button", x=screen_width//2 ,y=screen_height//2):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.name = name
        self.rect = (self.center_x, self.center_y, self.width, self.height)
        self.colour_inner = (92, 125, 124) #(92, 125, 124) (51, 231, 247)
        self.colour_outer = (max(0,self.colour_inner[0]-40), max(0,self.colour_inner[1]-40), max(0,self.colour_inner[2]-40))
        self.colour = self.colour_inner
        self.selected = False

    def draw(self):
        pygame.draw.rect(screen, self.colour_inner, self.rect)
        text = pygame.font.Font('freesansbold.ttf', round(min(self.width//1.5,self.height//1.5))).render(self.name, True, self.colour_outer)
        textRect = text.get_rect()
        textRect.center = (self.center_x+self.width//2,self.center_y+self.height//2)
        screen.blit(text, textRect)

    def hover(self, hovering):
        if hovering:
            self.colour_inner = (min(255,self.colour[0]+40), min(255,self.colour[1]+40), min(255,self.colour[2]+40))
        elif self.selected:
            self.colour_inner = (self.colour[0], self.colour[1], self.colour[2])
        else:
            self.colour_inner = (self.colour[0], self.colour[1], self.colour[2])

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
        self.colour_inner = (92, 125, 124) #(92, 125, 124) (51, 231, 247)
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

    def select(self, cards_selected):
        print(cards_selected)
        if not self.selected and cards_selected < 3:
            self.selected = True
            return 1
        elif self.selected:
            self.selected = False
            return -1
        else:
            return 0

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

def start_menu():
    objects.append(Button(round(screen_width//4), round(screen_height//10),"Play", screen_width//2-round(screen_width//8), screen_width//2-round(screen_height//20)))
    objects.append(TextBox(round(screen_width//3), round(screen_height//5),"YarrLatro", screen_width//2, screen_height//4))


def play_game():
    objects.clear()
    deck = true_deck.copy()
    hand = []
    card_objects.clear()
    random.seed(0)
    for i in range(0,7):
        hand.append(random.choice(deck))
        deck.remove(hand[i])
        card_objects.append(hand[i])
    
    objects.append(Button(round(screen_width//6), round(screen_height//10),"Quit", screen_width-round(screen_width//6)-screen_width//20, screen_height-round(screen_height//10)-screen_height//20))

    display_hand(hand)

innit_screen(screen_width, screen_height)

start_menu()

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
                    cards_selected += card.select(cards_selected)
            else:
                card.hover(False)

        for thing in objects:
            try:
                if thing.rect[0] <= mos_pos[0] <= thing.rect[0]+thing.rect[2] and thing.rect[1] <= mos_pos[1] <= thing.rect[1]+thing.rect[3]:
                    thing.hover(True)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if thing.name == "Play":
                            play_game()
                        elif thing.name == "Quit":
                            game_run = False
                else:
                    thing.hover(False)
            except:
                pass

    screen.fill((200,200,200))
    for card in card_objects:
        card.draw()

        #pygame.draw.rect(screen, (255,0,0), card.rect)
        #pygame.draw.rect(screen, (0,0,255), card.hitbox)

    for thing in objects:
        thing.draw()

    pygame.display.flip()


pygame.quit()
sys.exit()
