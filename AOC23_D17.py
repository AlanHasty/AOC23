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




def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)


    with open(args.file, 'r') as datafile:
        for i,line in enumerate(datafile):
            score = 0


  
if __name__ == '__main__':
    main()