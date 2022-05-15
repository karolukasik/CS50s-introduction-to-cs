// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hashValue = hash(word);
    node *nodeInCurrentBucket = table[hashValue];
    if (nodeInCurrentBucket == NULL)
    {
        return false;
    }
    while (nodeInCurrentBucket->next)
    {

        if (strcasecmp(nodeInCurrentBucket->word, word) == 0)
        {

            return true;
        }
        nodeInCurrentBucket = nodeInCurrentBucket->next;
    }

    if (strcasecmp(nodeInCurrentBucket->word, word) == 0)
    {
        return true;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int hashValue = 8;
    int i = 0;
    while (word[i] != '\0')
    {
        hashValue = hashValue + (toupper(word[i]));
        i++;
    }
    return hashValue;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        return false;
    }
    char c;
    char wordTemp[LENGTH + 1];
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    int i = 0;

    while (fread(&c, sizeof(char), 1, file))
    {
        if (isalpha(c) || c == 39)
        {
            wordTemp[i] = c;
            i++;
            continue;
        }
        wordTemp[i] = '\0';
        unsigned int hashValue = hash(wordTemp);
        node *tmp = malloc(sizeof(node));
        strcpy(tmp->word, wordTemp);
        // printf("-> %s\n", tmp->word);
        tmp->next = NULL;

        if (table[hashValue] == NULL)
        {
            table[hashValue] = tmp;
        }
        else
        {
            node *firstNode = table[hashValue];
            tmp->next = firstNode;
            table[hashValue] = tmp;
        }
        i = 0;
    };

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int size = 0;
    for (int i = 0; i < N; i++)
    {
        node *currentNode = table[i];
        if (currentNode == NULL)
        {
            continue;
        }
        while (currentNode->next != NULL)
        {
            //  printf("Current node: %s\n", currentNode->word);
            size++;
            currentNode = currentNode->next;
        }
        size++;
    }
    return size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *nodeInCurrentBucket = table[i];
        while (nodeInCurrentBucket != NULL)
        {
            node *tmp = nodeInCurrentBucket->next;
            free(nodeInCurrentBucket);
            nodeInCurrentBucket = tmp;
        }
    }

    return true;
}
