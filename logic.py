import random
random.seed(0)

true_deck = []

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

for i in range(1,6):
    for j in range(1,6):
        true_deck.append(Card(i,j))

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

    print(values,dict_values)

    if 5 in dict_values:
        mult = 2
        print("Five of a Kind")
    elif [1,1,1,1,1] == dict_values:
        mult = 1.9
        print("Straight")
    elif 4 in dict_values:
        mult = 1.8
        print("Four of a Kind")
    elif 3 in dict_values and 2 in dict_values:
        mult = 1.6
        print("Full House")
    elif 2 in dict_values and dict_values.index(2) != (len(dict_values)-dict_values[::-1].index(2)-1):
        mult = 1.5
        print("Two Pair")
    elif 3 in dict_values:
        mult = 1.45
        print("Three of a Kind")
    elif 2 in dict_values:
        mult = 1.45
        print("Two of a Kind")
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
    for i in range(0,5):
        hand.append(random.choice(deck))
        deck.remove(hand[i])

    for card in hand:
        print(card)
    print(len(deck))

    print("score",score_hand(hand))

play_game()