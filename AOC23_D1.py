import re
from rich import print


debug_positions = False

def find_first__and_last_spelled_digit(line, digit, debug):
    word_one = re.compile(digit)
    index = word_one.search(line, 0)
    if index != None:
        first_instance = index.start()
        pattern_end_pos = index.end()
        result = (first_instance, None)
        while True:
            next = word_one.search(line, pattern_end_pos)
            if next == None: 
                break
            else:
                result = (first_instance, next.start())
                pattern_end_pos = next.end()
    else: 
        result = (None, None)    
    
    if debug:
        print(f'Digit: {digit}:: First: {result[0]} Last: {result[1]}')
    return result
        

spelled_digits = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
#spelled_digits = ["zero","five"]


def return_dig_value(str):
    if str == 'zero':
        return 0
    if str == "one":
        return 1
    if str == "two":
        return 2
    if str == "three":
        return 3
    if str == "four":
        return 4
    if str == 'five':
        return 5    
    if str == "six":
        return 6
    if str == "seven":
        return 7
    if str == "eight":
        return 8
    if str == "nine":
        return 9


def find_spelled_digits(line, debug):
    spelled_number_indecies = []
    for u in spelled_digits:
        spelled_number_indecies.append( (u, (find_first__and_last_spelled_digit(line, u, debug))) )
    
    # Now look for the lowest starting index , and the highest ending index.

    # First see if there are any word numbers that occur twice. 
    first_digit_word = []
    multi_inst = False
    for index, info in enumerate(spelled_number_indecies):
        (number_t, num_i) = info
        (low_index, high_index) = num_i
        if  high_index == None:
            continue
        else:
            # There is one entry that has multiple instances in the line.
            multi_inst = True

    lowest_index = None
    low_value = None
    highest_index = None
    high_value = None
    # Assumption IF ALL the number are in the spelled list, the index works for the 
    # low_value to be returned. 
    for spn_idx, info in enumerate(spelled_number_indecies):
        (number_t, num_i) = info
        (low_index, high_index) = num_i
        if low_index == None:
            continue
        else:
            if lowest_index == None:
                lowest_index = low_index
                low_value = (return_dig_value(number_t), low_index)
            elif low_index < lowest_index:
                lowest_index = low_index
                low_value = (return_dig_value(number_t), low_index)
    if multi_inst == False:
        for spn_idx, info in enumerate(spelled_number_indecies):
            (number_t, num_i) = info
            (low_index, high_index) = num_i
            if low_index == None :
                continue
            else:
                if highest_index == None:
                    highest_index = low_index
                    high_value = (return_dig_value(number_t), low_index)
                elif low_index > highest_index:
                    highest_index = low_index
                    high_value = (return_dig_value(number_t), low_index)
    else:
        #print(f'\n\t\t\t****> Warning     {multi_inst = }:\n')
        for spn_idx, info in enumerate(spelled_number_indecies):
            (number_t, num_i) = info
            (low_index, high_index) = num_i
            if high_index == None :
                continue
            else:
                if highest_index == None:
                    highest_index = high_index
                    high_value = (return_dig_value(number_t), high_index)
                elif high_index > highest_index:
                    highest_index = high_index
                    high_value = (return_dig_value(number_t), high_index)

        # HOWEVER, there could be a different digit with a higher First position 
        # Which would make it the last word number. 
        # So check those....
        for spn_idx, info in enumerate(spelled_number_indecies):
            (number_t, num_i) = info 
            (low_index, high_index) = num_i

            if low_index != None and high_value[1] < low_index: 
                high_value = ( return_dig_value(number_t), low_index)
            

    if low_value == None:
        low_value = (None, None)

   
    if high_value == None:
        high_value = (None, None)

    if debug:
        print(f'First word digit {low_value[0]}, index:{low_value[1]}:'\
            f' Last word digit {high_value[0]}, index:{high_value[1]}')
    return (low_value, high_value)

def find_digit_positions(input, debug):
    first_digit_found = False
    last_digit = None
    first_digit = None
    first_digit_index = None
    last_digit_index = None
    for index,char in enumerate(input): 
        char_val = ord(char) - ord('0')
        if  char_val <= 9 and char_val >= 0 :
            if not first_digit_found: 
                first_digit_index = index
                first_digit = char_val
                first_digit_found = True
            #print(f'{char_val}')
            last_digit = char_val
            last_digit_index = index
    low_value = ( first_digit, first_digit_index)
    high_value = (last_digit, last_digit_index) 
    if debug:
        print(f'First digit {low_value[0]}, index:{low_value[1]}: ' \
            f'Last digit {high_value[0]}, index:{high_value[1]}')
    return (low_value, high_value)            

def main():
    first_digit_found = False
    cs = ''
    total = 0 
    #with open('d1b_test.data', 'r') as datafile:
    with open('d1.data', 'r') as datafile:
        for index,line in enumerate(datafile):

            print(f'\nConsidering Line{index+1}: [bold yellow]{line}[bold yellow]')
            line.strip()

            (low_digit_info, high_digit_info) = find_digit_positions(line, debug_positions)

            # Find indexes of the any spelled numbers in the line.
            (low_word_info, high_word_info) = find_spelled_digits(line, debug_positions)

            # print(f'\n****\n\tDigits Low: {low_digit_info = }',
            #       f'Digits High: {high_digit_info   = }',
            #       f'Words Low: {low_word_info = }',
            #       f'Words High {high_word_info = }',
            #       sep='',
            #       )

            # Now compare the lowest index of digits and words
            # and save that value. 

            if low_digit_info[1] == None:
                value1 = low_word_info[0]
            elif low_word_info[1] == None:
                value1 = low_digit_info[0]
            elif low_digit_info[1] < low_word_info[1]:
                value1 = low_digit_info[0]
            else: 
                value1 = low_word_info[0]

            # Now compare the higest index of digits and words
            # and save that value. 
            if high_digit_info[1] == None:
                value2 = high_word_info[0]
            elif high_word_info[1] == None:
                value2 = high_digit_info[0]
            elif high_digit_info[1] > high_word_info[1]:
                value2 = high_digit_info[0]
            else: 
                value2 = high_word_info[0]
            print(f'\n\tFirst number {value1 = }, Second number {value2 = }')
            linesum = value1 * 10 + value2
            total += linesum
            print(f'\tLine Sum: [bold red]{linesum = }[/bold red] New Total: {total = }')

def main2():

    with open('d1c_test.data', 'r') as datafile:
    #with open('d1b_test.data', 'r') as datafile:
        for index,line in enumerate(datafile):
            print(f'\nConsidering Line{index+1}: {line}')
            line.strip()

            # Find indexes of the any spelled numbers in the line.
            (low_word_info, high_word_info) = find_spelled_digits(line)

main()