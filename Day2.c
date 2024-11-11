
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

#define SIZE_WORD_NUMS 10

char * buffer = NULL;
FILE *openme;

typedef enum cube_color {
    RED = 1,
    BLUE = 2, 
    GREEN = 3
} cube_color_t;

typedef struct bag {
    int blue_cubes;
    int red_cubes;
    int green_cubes;
} bag_t ;


void start_game(bag_t *bag)
{
    bag->blue_cubes = 14;
    bag->red_cubes = 12;
    bag->green_cubes = 13; 
}

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
    bag_t game_bag;

    while(1)
    {
        if ((fgets((char *)buffer, 1024, openme)) == NULL)
        {
            break;
        }

        printf("%s\n", buffer);
        start_game(&game_bag);

        /** Split the line into multiple grabs */

        // Game 11: 6 blue, 3 green, 8 red; 6 blue, 4 green; 1 red, 3 green, 4 blue
    } 

    fclose(openme);
}