#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <stdint.h>

typedef uint8_t BYTE;
int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: recover filename.raw\n");
        return 1;
    }
    string filename = argv[1];

    FILE *file = fopen(filename, "r");
    if (!file)
    {
        printf("Error with reading a file: %s", filename);
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    int i = 0;
    char jpgNameBuffer[8];
    FILE *jpgfile = NULL;

    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            sprintf(jpgNameBuffer, "%03i.jpg", i);
            jpgfile = fopen(jpgNameBuffer, "w");
            i++;
        }
        if (jpgfile)
        {
            fwrite(buffer, 1, BLOCK_SIZE, jpgfile);
        }
    }
}