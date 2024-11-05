
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>



char * buffer = NULL;
FILE *openme;

typedef struct dig_info {
    char * name;
    int digit_first_idx;
    int name_first_idx;
    int digit_last_idx;
    int name_last_idx;
} dig_info_t ;

void clear_nums_array(dig_info_t *n)
{
    memset((void *)n, 0, sizeof(dig_info_t)*10);
}

void init_nums_array(dig_info_t *n)
{
    clear_nums_array(n);
    for (int loop = 0; loop < 10; loop++)
    {
        switch(loop)
        {
            case 0:
                n->name = "zero";
                break;
            case 1: 
                n->name = "one";
                break;
            case 2:
                n->name = "two";
                break;
            case 3: 
                n->name = "three";
                break;
            case 4:
                n->name = "four";
                break;
            case 5:
                n->name = "five";
                break;
            case 6:
                n->name = "six";
                break;
            case 7:
                n->name = "seven";
                break;
            case 8: 
                n->name = "eight";
                break;
            case 9:
                n->name = "nine";
            default: 
                n->name = "unknown";
        }
    }
}


int main(int argc, char ** argv)
{
    bool part_b_flag = false;
    char * fname; 
    dig_info_t nums[10]; 

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
}