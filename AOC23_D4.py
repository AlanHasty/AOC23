import re
import argparse
from rich import print

debug = True

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


def get_winning_numbers(card):
    win = re.compile(r"Card *([0-9]+): (.+) \|")
    m = win.match(card)
    if m != None:
        win_list = m.group(2).replace("  ", " ").split(" ")
        print(f'{win_list}')
    return win_list

def get_played_numbers(card):
    numbers = re.compile(r"Card *([0-9]+): (.+) \| (.+)")
    m = numbers.match(card)
    if m != None:
        num_list = m.group(3).replace("  ", " ").split(" ")
        print(f'{num_list}')
    return num_list

def get_card_score(win, play):
    score = 0
    card_scoring = 0
    for i,winner in enumerate(win):
        if winner in play:
            card_scoring += 1
            print(f'[bold Blue]{winner = } scores')
            if score == 0:
                score = 1
            else:
                score *= 2

    return (card_scoring, score)
    #return score

def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)
    point_tot = 0
    win_list = []
    numb_list = []
    new_deck = []
    bonus_round = True

    with open(args.file, 'r') as datafile:
        for i,line in enumerate(datafile):
            score = 0
            l = line.strip()
            print(f'{l = }')
            win_list = get_winning_numbers(l)
            numb_list = get_played_numbers(l)
            (num_card_scoring, score) = get_card_score(win_list, numb_list)
            (num_card_scoring, score) = get_card_score(win_list, numb_list)
            if num_card_scoring > 0 and bonus_round == True:
                new_deck.append( (num_card_scoring, l))
            else:
                bonus_round = False
            point_tot += score
            if debug:
                print(f'Card {score = } making {point_tot =}')

    print(f'Total score = {point_tot = }')

    for i, card_entry in enumerate(new_deck):
        (bonus, card) = card_entry 
        print(f'bonus cards = {bonus} for game {i = }',
              f'Adding cards {(i+1)}-{(i+1+bonus)}')

  
if __name__ == '__main__':
    main()