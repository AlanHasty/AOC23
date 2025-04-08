
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

#define SIZE_WORD_NUMS 10

char * buffer = NULL;
FILE *openme;

typedef struct node_info {
    char name [5];
    char lchild_name[5];
    char rchild_name[5];
    struct node_info * left;
    struct node_info * right;
    struct node_info * next;
} node_info_t ; 

node_info_t * find_node_in_maze(node_info_t *maze, char * name)
{
    if ( maze == NULL )
    {
        return NULL;
    }
    else
    {
        node_info_t * n = maze;
        while (n != NULL)
        {
            if (strncmp(n->name, name, 3) == 0)
            {
                return n;
            }
            n = n->next;
        }
    }
    return NULL;
}

void add_node_to_maze(node_info_t **maze, node_info_t *n)
{
    if ( *maze == NULL )
    {
        *maze = n;
    }
    else
    {
        node_info_t * m = *maze;
        while (m->next != NULL)
        {
            m = m->next;
        }
        m->next = n;
    }
}

node_info_t * create_new_node(char * name, char * left_child_name, char * right_child_name)
{
    node_info_t * n = malloc(sizeof(node_info_t));
    memcpy(n->name, name, strlen(name));
    memcpy(n->lchild_name, left_child_name, strlen(left_child_name));
    memcpy(n->rchild_name, right_child_name, strlen(right_child_name));
    n->left = NULL;
    n->right = NULL;
    n->next = NULL;
    return n;
}

bool isEndNode(node_info_t * n)
{
    if (n == NULL)
    {
        return false;
    }
    if (strncmp(n->name, "ZZZ", 3) == 0)
    {
        return true;
    }
    return false;
}   

int follow_instructions(node_info_t *maze, char *instr)
{
    int num_turns = 0;

    char * p = instr;

    if (maze == NULL)
    {
        return 0;
    }
    node_info_t * n = maze;
    while (1)
    {
        printf("Current node %s, left child %s, right child %s\n", n->name, n->lchild_name, n->rchild_name);
        if (isEndNode(n))
        {
            break;
        }
        char dir = *p;
        if (dir == 'L')
        {
            n = n->left;
            num_turns++;
        }
        else if (dir == 'R')
        {
            n = n->right;
            num_turns++;
        }
        else 
        {
            // reset the instruction pointer
            p = instr;
        }
        p++;
    }

    return num_turns;
}

void connect_nodes_by_name(node_info_t *maze)
{
    node_info_t * n = maze;
    while (n != NULL)
    {
        if (n->lchild_name[0] != '\0')
        {
            n->left = find_node_in_maze(maze, n->lchild_name);
        }
        if (n->rchild_name[0] != '\0')
        {
            n->right = find_node_in_maze(maze, n->rchild_name);
        }
        n = n->next;
    }
}

void print_node_list(node_info_t *maze)
{
    node_info_t * n = maze;
    while (n != NULL)
    {
        printf("Node %s, left child %s, right child %s\n", n->name, n->lchild_name, n->rchild_name);
        n = n->next;
    }
}

int main(int argc, char ** argv)
{
    bool part_b_flag = false;
    char * fname; 
    int node_count = 0;

    node_info_t * maze_start = NULL;

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

    bool instructions_found = false;
    char * instr = NULL;

    while(1)
    {
        if ((fgets((char *)buffer, 1024, openme)) == NULL)
        {
            break;
        }
        // Capture the direction instructions first 
        if ( !instructions_found)
        {
            int instruct_length = strlen(buffer);
            instr = malloc(instruct_length+1);
            memset(instr, 0, instruct_length+1);
            memcpy(instr, buffer, instruct_length-1); // remove trailing \n
            instructions_found = true;
        }
        else
        {
            // Now build the maze 
            int node_len = strlen(buffer);
            if ( node_len == 1 )
            {
                continue;
            }

            // AAA = (BBB, CCC) This is the format of the maze nodes.
            // Need to parse the string to get the node name and left/right children.
            // If we don't have a left or right child, then set to NULL.
            // If we have not created the left or right child, then create it.
            // If we have already created the left or right child, then set the pointer to it.
            char left_child_name[10];
            char right_child_name [10];
            char node_name [10];

            printf("%s", buffer);

            int num_names = sscanf(buffer, "%s = (%[^,], %[^)])", node_name, left_child_name, right_child_name);
            if ( num_names != 3 )
            {
                printf("Error parsing node %s\n", buffer);
                continue;
            }
            node_info_t * next_node = create_new_node(node_name, left_child_name, right_child_name);
            add_node_to_maze(&maze_start, next_node);
            node_count++;
        }
    }
    printf("Maze has %d nodes\n", node_count);
    print_node_list(maze_start);

    connect_nodes_by_name(maze_start);
    
    int number_of_turns = follow_instructions(maze_start, instr);
    printf("Number of turns = %d\n", number_of_turns);

    
    fclose(openme);
}