import argparse
from rich import print
from dataclasses import dataclass
from typing import List
from enum import IntEnum, Enum, unique

    # Five of a kind, where all five cards have the same label: AAAAA
    # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    # High card, where all cards' labels are distinct: 23456

@unique
class HandType(Enum):
    HIGH = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OK = 4
    FULL_HOUSE = 5
    FOUR_OK = 6
    FIVE_OK = 7
    NONE = 0

@unique
class Scores(IntEnum):
    HIGH = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OK = 4
    FULL_HOUSE = 5
    FOUR_OK = 6
    FIVE_OK = 7
    NONE = 0

debug = False

Cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1']

def parse_args(arg_list: list[str] | None):
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, default='none',
                        nargs='?', help='any data file for program')

    parser.add_argument('-d', '--debug', action='store_true',
                        help=argparse.SUPPRESS)
    
    # parser.add_argument('-r', type=int, help='number of red cubes for the game',
    #                     nargs='1')

    args = parser.parse_args(arg_list)

    if args.debug:  # pragma: no cover
        print('--- debug output ---')
        print(f'  {args=}')
        print(f'  {args.file=}')
        print('')
    return args
            
def flatten_list(list_to_flatten):
    flat_list = []
    for row in list_to_flatten:
        for tup in row:
            flat_list.append(tup)
    return flat_list 

@dataclass
class CamelCardHand():
    bid: int
    rank: int
    hand: str
    htype: HandType

hands: List[CamelCardHand] = []


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def check_card(crd, hand):
    run = ''
    cards_left = ''
    m = find(hand, crd)
    mlen = len(m)
    if mlen > 1:
        for i in m:
            run += hand[i]
        cards_left = hand.replace(crd, "")
        if mlen == 5: 
            htype = HandType.FIVE_OK
        elif mlen == 4:
            htype = HandType.FOUR_OK
        elif mlen == 3:
            htype = HandType.THREE_OK
        else:
            htype = HandType.ONE_PAIR
        
    else:
        run = crd
        cards_left = hand
        htype = HandType.HIGH
    return (run, cards_left, htype )

def score_hand(h:CamelCardHand, debug):
    each_card_analysis = []
    for i, c in enumerate(h.hand):
        (run, cleft, htype) = check_card(c, h.hand)
        results = (c, htype, cleft)
        
        each_card_analysis.append( results )
        if htype == HandType.FIVE_OK or htype == HandType.FOUR_OK:            
            break
        if debug:
            print(f'{c = }::{htype = }, {run = }: {cleft = }')

    if len(each_card_analysis) == 1: 
        return htype
    else:
        # this is the case where there might be a three of kind, 
        # full house, two pairs or one pair.
        # So how do we figure that out. 
        pair_half_full_house = False
        tok_half_full_house = False
        first_pair_seen = False
        card_first_pair = None
        card_tok = None

        for result  in each_card_analysis:
            (c, htype, cleft) = result
            if htype == HandType.THREE_OK and tok_half_full_house == False:
                # See if there is a pair 
                tok_half_full_house = True
                card_tok = c
                
            elif htype == HandType.ONE_PAIR and tok_half_full_house == True and card_first_pair == None:
                return HandType.FULL_HOUSE
            
            elif htype == HandType.ONE_PAIR and card_first_pair == None:
                card_first_pair = c
                first_pair_seen = True  
                pair_half_full_house = True              
            
            elif htype == HandType.ONE_PAIR and card_first_pair != None and card_first_pair != c:
                return HandType.TWO_PAIR
            
            elif htype == HandType.THREE_OK and pair_half_full_house == True and card_tok != None:
                return HandType.FULL_HOUSE
            
    if tok_half_full_house == True and card_first_pair == None and card_tok != None \
        and pair_half_full_house == False: 
        return HandType.THREE_OK
    elif card_first_pair != None:
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH
    

def convert_score(c: CamelCardHand):
    if c.htype == HandType.FIVE_OK:
        c.rank = Scores.FIVE_OK
    elif c.htype == HandType.FOUR_OK :
        c.rank = Scores.FOUR_OK
    elif c.htype == HandType.THREE_OK :
        c.rank = Scores.THREE_OK
    elif c.htype == HandType.FULL_HOUSE :
        c.rank = Scores.FULL_HOUSE
    elif c.htype == HandType.TWO_PAIR :
        c.rank = Scores.TWO_PAIR
    elif c.htype == HandType.ONE_PAIR :
        c.rank = Scores.ONE_PAIR
    else:
        c.rank = Scores.HIGH
    
def print_my_hands(h: List[CamelCardHand]):
    for c in h:
        print(f'{c.hand = }: {c.bid:4d}: Rank:{c.rank.value} {c.htype.name = }')
        
def order_hands(hands: List[CamelCardHand]):
    print('[bold blue]Ranking hands:')
    return sorted(hands, key=lambda c: c.rank, reverse=False)


def order_highest_ranked(hands: List[CamelCardHand]):
    ranked_hands = []
    final_ranking = []
    if len(hands) == 1:
        return hands
    else:
        # TODO - figure out how to rank the 
        # hands of the same score.
        # Compares just the first card
        starting_hand = hands

        for index in range(5):
            for card in Cards:
                print(f'Checking {card = } at {index = }')
                for h in hands:
                    if card ==  h.hand[index]:
                        print(f'Found in {h = }')
                        ranked_hands.append(h)

                len_ranked_hands = len(ranked_hands)

                if len_ranked_hands == 1:
                    final_ranking.append(ranked_hands[0])
                    ranked_hands = []
                
                elif len_ranked_hands >= 2:
                    break
                elif len(final_ranking) == len(hands):
                    print(f'{final_ranking}')
                    return final_ranking



def score_hands(hands: List[CamelCardHand]):
    score_list: List[CamelCardHand] = []

    # Get a list of the unique ranks
    ranks = [ r.rank for r in hands ]
    unique_ranks = set(ranks)
    ranks_pres = list(unique_ranks)

    for r in ranks_pres:

        hrh = [ hr for hr in hands if r == hr.rank ]

        if len(hrh) > 1:
            order_hrh = order_highest_ranked(hrh)
        else:
            order_hrh = hrh

        score_list += order_hrh

    score = 0
    for i, hand in enumerate(score_list):
        score_hand = hand.bid * (i+1)
        score += score_hand
        print(f'{i+1:3d} * {hand.bid:5d} = {score_hand:10d}: Score now {score = }')

def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)


    with open(args.file, 'r') as datafile:
        for i,line in enumerate(datafile):
            l = line.strip()
            
            (hand, bid) = l.split()
            print(f':-- HAND --> {hand}')
            c = CamelCardHand(int(bid), 0, hand, HandType.NONE)
            best = score_hand(c, debug)
            c.htype = best 
            convert_score(c)
            print(f'Hand Score: [bold red]{best}[/bold red] : {c.rank = }')
            hands.append(c)

        hand_order = order_hands(hands)



    print_my_hands(hands)
    print(f'[bold red] - Ranked ------')
    print_my_hands(hand_order)
    score_hands(hand_order)

  
if __name__ == '__main__':
    main()