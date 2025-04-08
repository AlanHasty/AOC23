
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

void add_node_to_maze(node_info_t *maze, node_info_t *n)
{
    if ( maze == NULL )
    {
        maze = n;
    }
    else
    {
        node_info_t * m = maze;
        while (m->next != NULL)
        {
            m = m->next;
        }
        m->next = n;
    }
}

int main(int argc, char ** argv)
{
    bool part_b_flag = false;
    char * fname; 

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
            char * instr = malloc(instruct_length+1);
            memcpy(instr, buffer, instruct_length);
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
            node_info_t * next_node = find_node_in_maze(maze_start, node_name);

            if ( next_node == NULL )
            {
                node_info_t * n = malloc(sizeof(node_info_t));
                // Create the node and add it to the maze
                memcpy(n->name, node_name, strlen(node_name));
                n->left = NULL;
                n->right = NULL;
                n->next = NULL;
                if ( maze_start == NULL )
                {
                    maze_start = n;
                }

                // Now we need to check if the left and right children exist

                // Now check if either of the children exist
                n->left = find_node_in_maze(maze_start, left_child_name);
                if ( n->left == NULL )
                {
                    // Create the left child node
                    n->left = malloc(sizeof(node_info_t));
                    memcpy(n->left->name, left_child_name, strlen(left_child_name));
                    n->next = n->left;
                    n->left->left = NULL;
                    n->left->right = NULL;
                    n->left->next = NULL;
                }

                n->right = find_node_in_maze(maze_start, right_child_name);
                if ( n->right == NULL )
                {
                    // Create the right child node
                    n->right = malloc(sizeof(node_info_t));
                    memcpy(n->right->name, right_child_name, strlen(right_child_name));
                    n->left->next = n->right;
                    n->right->left = NULL;
                    n->right->right = NULL;
                    n->right->next = NULL;
                }
            }
            else
            {
                printf("Node %s already exists\n", node_name);
                // We need to check if the left and right children exist
                // If they do, then set the pointers to them
                // If they don't, then create them
               
                if ( next_node->left == NULL )
                {

                    // Create the left child node
                    node_info_t * n = malloc(sizeof(node_info_t));
                    memcpy(n->name, left_child_name, strlen(left_child_name));

                    n->left = NULL;
                    n->right = NULL;
                    n->next = NULL;
                    next_node->left = n;   
                    
                    if ( next_node->next == NULL )
                    {
                        next_node->next = n;
                    }
                    else
                    {
                        node_info_t * m = next_node->next;
                        next_node->next = n;
                        n->next = m;
                    }
                }
                if ( next_node->right == NULL )
                {
                    // Create the right child node
                    node_info_t * n = malloc(sizeof(node_info_t));
                    memcpy(n->name, right_child_name, strlen(right_child_name));
                    n->left = NULL;
                    n->right = NULL;
                    n->next = NULL;
                    next_node->right = n;
                    if ( next_node->next == NULL )
                    {
                        next_node->next = n;
                    }
                    else
                    {
                        node_info_t * m = next_node->next;
                        next_node->next = n;
                        n->next = m;
                    }
                }
            }
        }

    }
    
    fclose(openme);
}