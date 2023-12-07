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


def possible_winning_times(time: int, distance: int):
    count = 0

    for t in range(1,time+1):
        speed = t
        remaining_time = time - t
        travel = speed * remaining_time
        if distance < travel:
            #print(f'Winner:{t = }: {travel = }')
            count += 1
        else:
            continue

    return count

def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)

    times = []
    distances = []
    with open(args.file, 'r') as datafile:
        for i,line in enumerate(datafile):
            score = 0

            if "Time:" in line:
                l = line.strip().replace("Time: ", "").replace(" ","")

                ltimes = l.split()
                for time in ltimes:
                    t = time.strip()
                    times.append(int(t))

            if "Distance:" in line:
                l = line.strip().replace("Distance: ", "").replace(" ","")
                ldistances = l.split()
                for d in ldistances:
                    distances.append(int(d))

        game_data = zip(times, distances)

        print(f'{game_data = }')

    total = 1
    for g in game_data:
            (t, d) = g
            count = possible_winning_times(t,d)
            total = total * count
            print(f'{t = },{d = } :{count =} : { total = }')
  
if __name__ == '__main__':
    main()