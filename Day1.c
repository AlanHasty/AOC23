
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

#define SIZE_WORD_NUMS 10

char * buffer = NULL;
FILE *openme;

typedef struct dig_info {
    char * name;
    char digit;
} dig_info_t ;

void clear_nums_array(dig_info_t *n)
{
    memset((void *)n, 0, sizeof(dig_info_t)*SIZE_WORD_NUMS);
}

void init_nums_array(dig_info_t *i)
{
    clear_nums_array(i);
    dig_info_t *n ;
    for (int loop = 0; loop < SIZE_WORD_NUMS; loop++)
    {
        n = &i[loop];
        switch(loop)
        {
            case 0:
                n->name = "zero";
                n->digit = '0';
                break;
            case 1: 
                n->name = "one";
                n->digit = '1';
                break;
            case 2:
                n->name = "two";
                n->digit = '2';
                break;
            case 3: 
                n->name = "three";
                n->digit = '3';
                break;
            case 4:
                n->name = "four";
                n->digit = '4';
                break;
            case 5:
                n->name = "five";
                n->digit = '5';
                break;
            case 6:
                n->name = "six";
                n->digit = '6';
                break;
            case 7:
                n->name = "seven";
                n->digit = '7';
                break;
            case 8: 
                n->name = "eight";
                n->digit = '8';
                break;
            case 9:
                n->name = "nine";
                n->digit = '9';
        }
    }
}


int main(int argc, char ** argv)
{
    bool part_b_flag = false;
    char * fname; 
    dig_info_t nums[SIZE_WORD_NUMS]; 

    if ( argc >= 2 )
    {
        fname = argv[1];

        if (argc >= 3)
        {
            part_b_flag = true;
            init_nums_array(nums);
        }

    }
    else 
    {
        printf("You need to specify the input file\n");
        return(-1);
    }
    buffer = malloc(10*1024);
    printf("Opening file %s\n", fname);
    openme = fopen(fname, "r");

    char first_digit;
    char last_digit;
    int32_t total = 0;
    bool first_dig_found;

    while(1)
    {
        if ((fgets((char *)buffer, 1024, openme)) == NULL)
        {
            break;
        }

        printf("%s\n", buffer);

        // for each line = work your way across the line to find fist and last digit.
        // Once the line is parsed, then combine the two digits into a string and convert to int.
        // Add the result to the tally.

        int len = strlen(buffer);
        for ( int pos = 0; pos < len; pos++)
        {
            if ( isdigit((int)buffer[pos]) == true )
            {
                if ( first_dig_found == false )
                {
                    first_dig_found = true;
                    first_digit = buffer[pos];
                    printf("Found first digit %c\n", first_digit);
                }

                last_digit = buffer[pos];
                printf("Found last digit %c\n", last_digit);
            }
            else 
            {
                /** Search for digits in line that are represented by words. */
                for ( int loop = 0; loop < SIZE_WORD_NUMS; loop++)
                {
                    if ( strncmp(&buffer[pos], nums[loop].name, strlen(nums[loop].name)) == 0 )
                    {
                        if (first_dig_found == false)
                        {
                            first_digit = nums[loop].digit;
                            first_dig_found = true;
                            printf("Found first digit %c\n", first_digit);
                        }
                        last_digit = nums[loop].digit;
                        printf("Found last digit %c\n", last_digit);
                        break;
                    }
                }
                
            }


            if ( buffer[pos] == 0xa )
            {
                first_dig_found = false;
                char line_sum[0];
                line_sum[0] = first_digit;
                line_sum[1] = last_digit;
                total += strtol(line_sum, NULL, 10);
                printf("Line number = %s : total %d\n", line_sum, total);
                break;
            }

        }

        if (first_dig_found) {
            char line_sum[0];
            line_sum[0] = first_digit;
            line_sum[1] = last_digit;
            total += strtol(line_sum, NULL, 10);
            printf("Line number = %s : total %d\n", line_sum, total);
        }

    }
    fclose(openme);
}