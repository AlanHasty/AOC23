

use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
//use itertools::Itertools;

Struct NumData {
    Value(u32),
    StartI(i32),
    EndI(i32),
}

fn main() {
    let mut nums = Vec::<NumData>::new();
    if let Ok(lines) = read_lines("../../Data/d3_test.data"){
        for line in lines {
            if let Ok(pzl_data_line) = line {
                println!("{}", pzl_data_line);
                let mut num = 0;
                let mut start_index: i32 = -1;
                for (_i,c) in pzl_data_line.chars().enumerate() {
                    match c.to_digit(10)
                    {
                        Some(new_d) => { 
                            if start_index < 0
                            {
                                start_index = _i as i32;
                            }
                            num = (num * 10) + new_d
                        },
                        None => { 
                           if c.is_ascii_punctuation() 
                            {
                                if num != 0 {
                                    let ent = NumData(Value::num, StartI::start_index, EndI::i32(0));
                                    nums.push(ent) ; 
                                    num = 0 ;
                                    start_index = -1;
                                }

                            }
                        }
                                
                    }
                }
            }
        }
        print_input(nums)
    }
}

fn print_input(_v: Vec<NumData>) -> ()
{
    //println!("{}", v.iter().format("\n"));
    ()
}
// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
