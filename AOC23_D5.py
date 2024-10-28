import re
import argparse
from rich import print
from dataclasses import dataclass
from typing import List

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


@dataclass
class Range_map_entry():
    src_cat: int
    dst_cat: int
    range: int

@dataclass
class Seed_t_Soil_map():
    seed_t_soil: List[Range_map_entry]

@dataclass
class Soil_t_Fertilizer_map():
    soil_t_fert: List[Range_map_entry]

@dataclass
class Fertilizer_t_Water_map():
    fert_t_water: List[Range_map_entry]

@dataclass
class Water_t_Light_map():
    water_t_light: List[Range_map_entry]

@dataclass
class Ligth_t_Temp_map():
    light_t_temp: List[Range_map_entry]

@dataclass
class Temp_t_Humidity_map():
    temp_t_hum: List[Range_map_entry]

@dataclass
class Humidity_t_Loc_map():
    hum_t_loc: List[Range_map_entry]


def read_seeds(file_data):
    seeds_list = []
    for line in file_data:
        l = line.strip()
        if len(l) == 0:
            break

        for word in l.split():
            if "seeds:" in word:
                continue
            else:
                seed_num = int(word)
                seeds_list.append(seed_num)

    print(f'{seeds_list}')    
    return seeds_list

def read_seed_to_soil_map(file_data):
    capture = False
    ss = Seed_t_Soil_map([])
    for line in file_data:
        if "seed-to-soil" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                ss.seed_t_soil.append(r)
        else:
            continue

    print(f'{ss = }')
    return ss

def read_soil_to_fert_map(file_data):
    capture = False
    ss = Soil_t_Fertilizer_map([])
    for line in file_data:
        if "soil-to-fertilizer" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                ss.soil_t_fert.append(r)
        else:
            continue

    print(f'{ss = }')
    return ss

def read_fert_to_water_map(file_data):
    capture = False
    m = Fertilizer_t_Water_map([])
    for line in file_data:
        if "fertilizer-to-water" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                m.fert_t_water.append(r)
        else:
            continue

    print(f'{m = }')
    return m

def read_water_to_light_map(file_data):
    capture = False
    m = Water_t_Light_map([])
    for line in file_data:
        if "water-to-light" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                m.water_t_light.append(r)
        else:
            continue

    print(f'{m = }')
    return m

def read_light_to_temp_map(file_data):
    capture = False
    m = Ligth_t_Temp_map([])
    for line in file_data:
        if "light-to-temperature" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                m.light_t_temp.append(r)
        else:
            continue

    print(f'{m = }')
    return m

def read_temp_to_humidity_map(file_data):
    capture = False
    m = Temp_t_Humidity_map([])
    for line in file_data:
        if "temperature-to-humidity" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                m.temp_t_hum.append(r)
        else:
            continue

    print(f'{m = }')
    return m

def read_humidity_to_location(file_data):
    capture = False
    m = Humidity_t_Loc_map([])
    for line in file_data:
        if "humidity-to-location" in line and capture == False:
            capture = True
            continue
        elif capture == True:
            if len(line) == 1:
                capture = False
                break
            else:
                l = line.strip()
                (src, dst, rng) = l.split()
                r = Range_map_entry(int(src), int(dst), int(rng))
                #print(f'{r = }')
                m.hum_t_loc.append(r)
        else:
            continue

    print(f'{m = }')
    return m

def search_range(value: int, r: Range_map_entry):
    r_low = r.src_cat
    r_high = r.src_cat + r.range
    offset = r.src_cat - r.dst_cat
    found = False

    if value >= r_low and \
       value <= r_high:
        new_value = value + offset
        found = True
    else:
        new_value = None

    return (found, new_value)

def find_seed_soil_trans(seed: int, ssm: Seed_t_Soil_map):
    for r in ssm.seed_t_soil:
        (result, new_val) =search_range(seed, r)
        if result == True:
            break

    if result == False:
        new_val = seed

    return new_val

def find_soil_fert_trans(soil: int, sfm: Soil_t_Fertilizer_map):
    for r in sfm.soil_t_fert:
        (result, new_val) =search_range(soil, r)
        if result == True:
            break

    if result == False:
        new_val = soil

    return new_val    

def find_fert_water_trans(fert: int, fwm: Fertilizer_t_Water_map):
    for r in fwm.fert_t_water:
        (result, new_val) =search_range(fert, r)
        if result == True:
            break

    if result == False:
        new_val = fert

    return new_val

def find_water_light_trans(water: int, wlm: Water_t_Light_map):
    for r in wlm.water_t_light:
        (result, new_val) =search_range(water, r)
        if result == True:
            break

    if result == False:
        new_val = water

    return new_val

def find_light_temp_trans(light: int, ltm:Ligth_t_Temp_map):
    for r in ltm.light_t_temp:
        (result, new_val) =search_range(light, r)
        if result == True:
            break

    if result == False:
        new_val = light

    return new_val

def find_temp_hum_trans(temp: int, thm:Temp_t_Humidity_map):
    for r in thm.temp_t_hum:
        (result, new_val) =search_range(temp, r)
        if result == True:
            break

    if result == False:
        new_val = temp

    return new_val

def find_hum_loc_trans(hum: int, hlm:Humidity_t_Loc_map):
    for r in hlm.hum_t_loc:
        (result, new_val) =search_range(hum, r)
        if result == True:
            break

    if result == False:
        new_val = hum

    return new_val

def main(arg_list: list[str] | None = None):
    args = parse_args(arg_list)


    with open(args.file, 'r') as datafile:
        seeds_list = read_seeds(datafile)
        ssm = read_seed_to_soil_map(datafile)
        sfm = read_soil_to_fert_map(datafile)
        fwm = read_fert_to_water_map(datafile)
        wlm = read_water_to_light_map(datafile)
        ltm = read_light_to_temp_map(datafile)
        thm = read_temp_to_humidity_map(datafile)
        hlm = read_humidity_to_location(datafile)

    locs = []

    for seed in seeds_list:
        soil_num = find_seed_soil_trans(seed, ssm)
        fert_num = find_soil_fert_trans(soil_num, sfm)
        water_num = find_fert_water_trans(fert_num, fwm)
        light_num = find_water_light_trans(water_num, wlm)
        temp_num = find_light_temp_trans(light_num, ltm)
        hum_num = find_temp_hum_trans(temp_num, thm)
        loc_num = find_hum_loc_trans(hum_num, hlm)

        print(f'{seed = }',
              f'{soil_num = }',
              f'{fert_num = }',
              f'{water_num = }',
              f'{light_num = }',
              f'{temp_num = }',
              f'{hum_num = }',
              f'{loc_num = }\n',
              sep='\n')
        
        locs.append(loc_num)
        
if __name__ == '__main__':
    main()