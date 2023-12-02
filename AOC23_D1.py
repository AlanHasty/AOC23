import re


def find_first__and_last_spelled_digit(line, digit):
    word_one = re.compile(digit)
    index = word_one.search(line, 0)
    if index != None:
        first_instance = index.start()
        next = word_one.search(line, index.end())
        if next == None:
            result =  (first_instance, None)
        else:
            result = (first_instance, next.start())
    else: 
        result = (None, None)    
    #print(f'Digit: {digit}:: First: {result[0]} Last: {result[1]}')
    return result
        

spelled_digits = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
#spelled_digits = ["five"]




def find_spelled_digits(line):
    spelled_number_indecies = []
    for u in spelled_digits:
        spelled_number_indecies.append( (u, (find_first__and_last_spelled_digit(line, u))) )
    
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
    for index, info in enumerate(spelled_number_indecies):
        (number_t, num_i) = info
        (low_index, high_index) = num_i
        if low_index == None:
            continue
        else:
            if lowest_index == None:
                lowest_index = low_index
                low_value = (index, low_index)
            elif low_index < lowest_index:
                lowest_index = low_index
                low_value = (index, low_index)
    
    for index, info in enumerate(spelled_number_indecies):
        (number_t, num_i) = info
        (low_index, high_index) = num_i
        if low_index == None :
            continue
        else:
            if highest_index == None:
                highest_index = low_index
                high_value = (index, low_index)
            elif low_index > highest_index:
                highest_index = low_index
                high_value = (index, low_index)
    

    if low_value == None:
        low_value = (None, None)

   
    if high_value == None:
        high_value = (None, None)
    print(f'First word digit {low_value[0]}, index:{low_value[1]}:'\
          f' Last word digit {high_value[0]}, index:{high_value[1]}')
    return (low_value, high_value)

def find_digit_positions(input):
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
    print(f'First digit {low_value[0]}, index:{low_value[1]}: ' \
          f'Last digit {high_value[0]}, index:{high_value[1]}')
    return (low_value, high_value)            

def main():
    first_digit_found = False
    cs = ''
    total = 0 
    with open('d1b_test.data', 'r') as datafile:
    #with open('d1.data', 'r') as datafile:
        for index,line in enumerate(datafile):
            print(f'\nConsidering Line{index+1}: {line}')
            line.strip()

            (low_digit_info, high_digit_info) = find_digit_positions(line)

            # Find indexes of the any spelled numbers in the line.
            (low_word_info, high_word_info) = find_spelled_digits(line)

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
            print(f'\t\tLine Sum: {linesum = } New Total: {total = }')

def main2():

    with open('d1c_test.data', 'r') as datafile:
    #with open('d1b_test.data', 'r') as datafile:
        for index,line in enumerate(datafile):
            print(f'\nConsidering Line{index+1}: {line}')
            line.strip()

            # Find indexes of the any spelled numbers in the line.
            (low_word_info, high_word_info) = find_spelled_digits(line)


main()