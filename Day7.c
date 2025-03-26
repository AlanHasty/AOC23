#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>


typedef enum card { 
    TWO = 2,
    THREE = 3,
    FOUR = 4,
    FIVE = 5,
    SIX = 6,
    SEVEN = 7,
    EIGHT = 8,
    NINE = 9,
    TEN = 10,
    JACK = 11,
    QUEEN = 12,
    KING = 13,
    ACE = 14
} Cards_t;

enum hand_rank {
    HIGH_CARD = 0,
    PAIR = 1,
    TWO_PAIR = 2,
    THREE_OF_A_KIND = 3,
    FULL_HOUSE = 4,
    FOUR_OF_A_KIND = 5,
    FIVE_OF_A_KIND = 6
};

#define MAX_CARDS 5
typedef struct  hand{
    Cards_t cards[MAX_CARDS];
    enum hand_rank rank;
    int bid;
} Hand_t;

