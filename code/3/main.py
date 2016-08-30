from birthday import has_duplicates
from cards import *
from poker_hand import *

a = [1, 2, 3, 4, 5, 6, 5, 6, 7]

#result = birthday.has_duplicates(a)
#print(result)

deck = Deck()
deck.shuffle()

hand = PokerHand()
deck.move_cards(hand, 5)
hand.classify()
print hand.label
print hand