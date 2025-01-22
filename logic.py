import random
random.seed(0)

deck = []

class Card:
    def __init__(self, type_l, type_n):
        self.type_l = type_l
        self.type_n = type_n
    
    def __str__(self):
        return f"Card is {self.number_to_letter()} {self.type_n}"
    
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
        deck.append(Card(i,j))

for card in deck:
    print(card)