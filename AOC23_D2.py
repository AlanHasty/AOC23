import re
import argparse
from rich import print


debug = True

def split_game_data(line, debug):
    game_data = re.compile("Game (\d+): (.*)")
    m = game_data.match(line)
    if m != None:
        game_num = m.group(1)
        round_data = m.group(2).split(';')
        if debug:
            print(f'G: {game_num}',
                f'round_data:',
                f'{round_data}',
                sep='\n')
    return (game_num, round_data)

def game_powers(g_data, debug):
    (id, rounds) = g_data
    red = re.compile(r"(\d+)red")
    blue = re.compile(r"(\d+)blue")
    green = re.compile(r"(\d+)green")
    red_tot = blue_tot = green_tot = 0

    for indx, rd in enumerate(rounds):
        red_cnt = 0
        blue_cnt = 0
        green_cnt = 0
        colors = rd.split(",")

        for cl in colors:
            c = cl.replace(" ", "")
            if c != None:
                if "red" in c:
                    m = red.match(c)
                    if m != None:
                        red_cnt = int(m.group(1))
                elif "blue" in c:
                    m = blue.match(c)
                    if m != None:
                        blue_cnt = int(m.group(1))
                elif "green" in c:
                    m = green.match(c)
                    if m != None:
                        green_cnt = int(m.group(1))
        
        if red_cnt > red_tot:
            red_tot = red_cnt

        if blue_cnt > blue_tot:
            blue_tot = blue_cnt

        if green_cnt > green_tot:
            green_tot = green_cnt
    
    if debug:
        print(f'Game {id = }: {(red_tot * blue_tot * green_tot) =} {red_tot = }, {blue_tot = }, {green_tot = }')
        

    return red_tot * blue_tot * green_tot


def game_validate(g_data, legal_game, debug):
    (id, rounds) = g_data
    red = re.compile(r"(\d+)red")
    blue = re.compile(r"(\d+)blue")
    green = re.compile(r"(\d+)green")
    (red_tot, blue_tot, green_tot) = legal_game

    for indx, rd in enumerate(rounds):
        red_cnt = 0
        blue_cnt = 0
        green_cnt = 0
        colors = rd.split(",")

        for cl in colors:
            c = cl.replace(" ", "")
            if c != None:
                if "red" in c:
                    m = red.match(c)
                    if m != None:
                        red_cnt = int(m.group(1))
                elif "blue" in c:
                    m = blue.match(c)
                    if m != None:
                        blue_cnt = int(m.group(1))
                elif "green" in c:
                    m = green.match(c)
                    if m != None:
                        green_cnt = int(m.group(1))
        if debug:
                print(f'Round {indx}: {rd = }:: {red_cnt = }, {blue_cnt = }, {green_cnt = }')
        
        if red_cnt > red_tot or \
           blue_cnt > blue_tot or \
           green_cnt > green_tot :
            if debug:
                print(f'[bold red]Game {id = } Round {indx = } has invalid data',
                       f'{red_cnt = }, {blue_cnt = }, {green_cnt = }')
            return 0

    return int(id)

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

def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)
    game_sum = 0
    power_sum = 0
    #
    # Legal game is  red, bleu, green
    # only 12 red cubes, 13 green cubes, and 14 blue cubes
    lgame = [12, 14, 13]
    with open(args.file, 'r') as datafile:
        for index,line in enumerate(datafile):

            print(f'\nConsidering Line{index+1}: [bold yellow]{line}[bold yellow]')
            line.strip()
            game = split_game_data(line, debug)

#            game_sum += game_validate(game, lgame, False)
#            print(f'Game ID Sum: {game_sum = }')

            power_sum += game_powers(game, debug)
            print(f'Game Power Sum: {power_sum = }')

  
if __name__ == '__main__':
    main()