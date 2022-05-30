# TODO

from cs50 import get_int

while(True):
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break

width = height * 2 + 2
for i in range(height):
    for j in range(width):
        if j < height-i-1:
            print(" ", end="")
        elif(j >= height - i-1 and j < height):
            print("#", end="")
        elif(j == height or j == height + 1):
            print(" ", end="")
        elif(j > height + 1 and j <= height + i+2):
            print("#", end="")
    print("")
