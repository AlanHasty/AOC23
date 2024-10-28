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

def process_numbers(row, line, debug):
    num = 0
    add_flag = True
    start_i = None
    finish_i = None
    nums_in_line = []
    for idx, c in enumerate(line):
        if c.isdigit():
            num =  (num * 10) +int(c)
            if start_i == None:
                start_i = idx
            
            finish_i = idx

        elif not c.isdigit() and num != 0:
            nums_in_line.append( (row, start_i, finish_i, num))
            num = 0
            start_i = None
            if debug:
                print(f'{nums_in_line = }')

    return nums_in_line

def process_symbols(row, line, debug):
    s_in_line = []
    for idx, c in enumerate(line):
        if c.isdigit():
            pass

        elif c != '.':
            s_in_line.append( (row, idx, c))
            if debug:
                print(f'{s_in_line = }')

    return s_in_line

def find_adjacent_numbers(row, col, numbers, debug):
    if debug:
        print(f'Finding adjacent numbers to {row = }, {col =}')

    sum = 0
    for i,row_nums in enumerate(numbers):
        (nrow, start, finish, value) = row_nums
        if False == True and row < 2: 
            print(f'{value = } at {nrow = }: {start = }: {finish =}')
        
        #
        # This is the case for the numbers in the same Row as the symbol.
        #      RC-1, RC, RC+1
        if nrow == row:
            if finish + 1 == col:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
            elif start - 1 == col:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
        #
        # This is the case for the numbers in the Row above the symbol.
        #      R-1 C-1, R-1C, R-1 C+1                                        
        if nrow + 1 == row:
            if finish + 1 == col or finish == col:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
            elif start == col or start - 1 == col:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
            elif start < col and col < finish:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value

        #
        # This is the case for the numbers in the Row below the symbol.
        #      R+1 C-1, R+1C, R+1 C+1     
        # PLUS there is a case where the number spans the column where the symbol
        # is located.                                   
        if nrow - 1 == row:
            if finish + 1 == col or finish == col:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
            elif start == col or start - 1 == col:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
            elif start < col and col < finish:
                if debug:
                    print(f'Must Add in : {value}')
                sum += value
    return sum

def find_gear_ratios(row, col, nums, debug):
    ratio = []
    for i,row_nums in enumerate(nums):
        (nrow, start, finish, value) = row_nums
        if False == True and row < 2: 
            print(f'{value = } at {nrow = }: {start = }: {finish =}')
        
        #
        # This is the case for the numbers in the same Row as the symbol.
        #      RC-1, RC, RC+1
        if nrow == row:
            if finish + 1 == col:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
            elif start - 1 == col:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
        #
        # This is the case for the numbers in the Row above the symbol.
        #      R-1 C-1, R-1C, R-1 C+1                                        
        if nrow + 1 == row:
            if finish + 1 == col or finish == col:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
            elif start == col or start - 1 == col:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
            elif start < col and col < finish:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)

        #
        # This is the case for the numbers in the Row below the symbol.
        #      R+1 C-1, R+1C, R+1 C+1     
        # PLUS there is a case where the number spans the column where the symbol
        # is located.                                   
        if nrow - 1 == row:
            if finish + 1 == col or finish == col:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
            elif start == col or start - 1 == col:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
            elif start < col and col < finish:
                if debug:
                    print(f'Gear : {value}')
                ratio.append(value)
    print(f'Gear Ratio parts: {ratio = }')
    if len(ratio) == 2:
        cal_ratio = ratio[0] * ratio[1]
    elif len(ratio) == 1:
        print('[bold blue]Note: Not a gear')
        cal_ratio = 0
    else:
        print('[bold red]Warning - more than two gears found')
        cal_ratio = 0 

    return cal_ratio

def find_part_num(nums, symbols, debug):
    gear_r_sum = part_number = 0
    for i, symbol in enumerate(symbols): 
        (row, index, char) = symbol
        if debug:
            print(f'Finding adjacent numbers for symbol {char = }: {row}, {index}')
        part_number += find_adjacent_numbers(row, index, nums, debug)
        if char == '*':
            gear_r_sum += find_gear_ratios(row, index, nums, debug)

    print(f'Part number sum = {part_number}')
    print(f'Gear Ratio sum = {gear_r_sum}')
            
def flatten_list(list_to_flatten):
    flat_list = []
    for row in list_to_flatten:
        for tup in row:
            flat_list.append(tup)
    return flat_list 

def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)

    num_list = []
    symbol_list = []
    columns = 0
    rows = 0
    with open(args.file, 'r') as datafile:
        for i,line in enumerate(datafile):
            l = line.strip()
            print(f'{l = }')

            # first find the numbers in a line, along with the index that the number 
            # and finishes and row number
            nums_in_row = process_numbers(i, l, False)
            if len(nums_in_row) != 0:
                num_list.append(nums_in_row)
            # Then find the symbols in the map and their  row number and index

            symb_in_row = process_symbols(i, l, False)
            if len(symb_in_row) != 0:
                symbol_list.append(symb_in_row)

    sym_list = flatten_list(symbol_list)
    nums_list = flatten_list(num_list)

    if True == True:
        print(f'{num_list = }')
        print(f'{symbol_list = }')
        
    find_part_num(nums_list, sym_list, True)


  
if __name__ == '__main__':
    main()