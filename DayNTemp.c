
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

#define SIZE_WORD_NUMS 10

char * buffer = NULL;
FILE *openme;



int main(int argc, char ** argv)
{
    bool part_b_flag = false;
    char * fname; 

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

    while(1)
    {
        if ((fgets((char *)buffer, 1024, openme)) == NULL)
        {
            break;
        }

        printf("%s\n", buffer);
    }
    
    fclose(openme);
}