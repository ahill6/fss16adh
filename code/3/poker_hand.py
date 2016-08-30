"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from cards import *
import copy

class PokerHand(Hand):

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
			
    def value_hist(self):
        """Builds a histogram of the card values that appear in the hand.

        Stores the result in attribute vals.
        """
        self.vals = {}
        for card in self.cards:
            self.vals[card.rank] = self.vals.get(card.rank, 0) + 1
			
    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
		
    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.value_hist()
        for val in self.vals.values():
            if val >= 2:
                return True
        return False
		
    def has_two_pair(self):
	    """Returns True if the hand has two pair, False otherwise.
	    
	    Note that this works correctly for hands with more than 5 cards.
	    """
	    pair_count = 0
	    self.value_hist()
	    
	    for val in self.vals.values():
	        if val >= 2:
	            pair_count += 1
	            #a four of a kind is technically also two pair, but you would not have two different entries in the dictionary
	            if pair_count >= 2 or val>=4: 
	                return True
	   
	    return False
	   
    def has_three_of_a_kind(self):
        """Returns True if the hand has a three-of-a-kind, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.value_hist()
        for val in self.vals.values():
            if val >= 3:
                return True
        return False
		
    def has_straight(self):
        """Returns True if the hand has a straight, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        This also assumes that you are playing a variant of poker where the ace 
        be attached either to a 2 or a King for a straight
        
        Also note that this is the ugliest, most brute force way of doing this.
        TODO - Find a more elegant solution.
        """
        self.cards.sort()
        counter = self.cards[0].rank
        ctrl = copy.copy(self.cards[1:])
        
        if counter == 1:
            counter = self.cards[1].rank
            card = Card(self.cards[0].suit, 14)
            ctrl.pop(0)
            ctrl.append(card)
            
        for card in ctrl:
            if card.rank == counter + 1:
                counter += 1
            else:
                return False
        return True

    def has_full_house(self):
        """Returns True if the hand has a full house, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.value_hist()
        # NB - Alternate way to do this would be to see if he has two pair, then three-of-a-kind
        three = False
        pair = False 
        
        for val in self.vals.values():
            if val >= 3:
                three = True
            elif val == 2:
                pair = True
                
        return (three and pair)
		
    def has_four_of_a_kind(self):
        """Returns True if the hand has a four-of-a-kind, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.value_hist()
        for val in self.vals.values():
            if val >= 4:
                return True
        return False
		
    def has_straight_flush(self):
        """Returns True if the hand has a straight flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        straight = self.has_straight()
        flush = self.has_flush()
        
        return (straight and flush)
        
    def classify(self):
        if self.has_straight_flush():
            self.label = "straight flush"
        elif self.has_four_of_a_kind():
            self.label = "four of a kind"
        elif self.has_full_house():
            self.label = "full house"
        elif self.has_flush():
            self.label = "flush"
        elif self.has_straight():
            self.label = "straight"
        elif self.has_three_of_a_kind():
            self.label = "three of a kind"
        elif self.has_two_pair():
            self.label = "two pair"
        elif self.has_pair():
            self.label = "one pair"
        else:
            self.label = "nothing"
            #self.sort()
            #self.label = self[0] " high"
            
            
if __name__ == '__main__':
    # make a deck
    deck = Deck()
    deck.shuffle()

    # deal the cards and classify the hands
    for i in range(7):
        hand = PokerHand()
        deck.move_cards(hand, 7)
        hand.sort()
        print hand
        print hand.has_flush()
        print ''
