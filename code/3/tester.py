from poker_hand import *
from cards import *
from birthday import *

def pretty_print(results, count, type=0):
    
    if type == 0:
        for i in results:
            print i, results[i]/(count + 0.0)
    if type == 1:
        print results/(count + 0.0)
    
def tester(f, trials, repetitions, sample_size, answer_type):
    count = 0
    results = dict()
    res = 0
    
    for i in xrange(repetitions):
        if answer_type == 'dict':
            results.update(f(trials, sample_size))
        else:
            res += f(trials, sample_size)
        count += 1

    if answer_type == 'dict':
        pretty_print(results, count)
    else:
        pretty_print(res, count, 1)
    
def poker_tester(trials, hand_size):
    odds = dict()

    for i in xrange(trials):
        deck = Deck()
        deck.shuffle()
        hand = PokerHand()
        deck.move_cards(hand, hand_size)
        b = hand.classify()
        if b in odds:
            odds[b] += 1
        else:
            odds[b] = 1
            
    return odds
        
def birthday_tester(trials, samples):
    count = 0
    
    for i in xrange(trials):
        bdays = gen_rand_birthday(samples)
        if has_duplicates(bdays):
            count += 1
    return count