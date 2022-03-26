#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    while(true){
        height = get_int("Height: ");
        if(height > 0 && height <=8){
            break;
        }
    }
    int width = height *2 + 2;

    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            if (j < height-i-1){
                printf(" ");
            } else if (j >= height -i-1 && j < height){
                printf("#");
            } else if (j == height || j == height +1){
                printf(" ");
            } else if (j > height +1 && j <= height +i+2){
               printf("#");
            }
        }
        printf("\n");
    }

}