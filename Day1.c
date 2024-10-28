
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>



char * buffer = NULL;
FILE *openme;


int main(int argc, char ** argv)
{
    char * fname; 
    if ( argc >= 2 )
    {
        fname = argv[1];
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

        printf("%s", buffer);

        // for each line = work your way across the line to find fist and last digit.
        // Once the line is parsed, then combine the two digits into a string and convert to int.
        // Add the result to the tally.

        int len = strlen(buffer);
        for ( int pos = 0; pos < len; pos++)
        {
            if ( is_digit((int)buffer[pos]) == true )
            {
                if ( first_dig_found == false )
                {
                    first_dig_found = true;
                    first_digit = buffer[pos];
                    printf("Found first digit %c", first_digit);
                    continue;
                }

                last_digit = buffer[pos];
                printf("Found first digit %c", first_digit);
            }
            if ( buffer[pos] == 0xa )
            {
                char line_sum[0];
                line_sum[0] = first_digit;
                line_sum[1] = last_digit;
                total += strtol(line_sum, NULL, 10);
                printf("Line number = %s : total %d", line_sum, total);
                break;
            }
        }

    }
}