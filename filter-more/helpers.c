#include "helpers.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int calculatePixelValue(int sumGx, int sumGy);
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            RGBTRIPLE *currentPixel = &image[r][c];
            int average = round((currentPixel->rgbtRed + currentPixel->rgbtGreen + currentPixel->rgbtBlue) / 3.0);
            currentPixel->rgbtRed = average;
            currentPixel->rgbtGreen = average;
            currentPixel->rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width / 2; c++)
        {
            RGBTRIPLE tempPointer = image[r][c];
            image[r][c] = image[r][width - 1 - c];
            image[r][width - 1 - c] = tempPointer;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*blurredImage)
    [width] = malloc(height * width * sizeof(RGBTRIPLE));
    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            int sumR = 0;
            int sumG = 0;
            int sumB = 0;
            double pixelCounter = 0;
            // box 3x3
            for (int br = r - 1; br <= r + 1; br++)
            {
                for (int bc = c - 1; bc <= c + 1; bc++)
                {
                    if (br >= 0 && br < height && bc >= 0 && bc < width)
                    {
                        sumR += image[br][bc].rgbtRed;
                        sumG += image[br][bc].rgbtGreen;
                        sumB += image[br][bc].rgbtBlue;
                        pixelCounter++;
                    }
                }
            }
            RGBTRIPLE blurredPixel = {.rgbtRed = round(sumR / pixelCounter),
                                      .rgbtGreen = round(sumG / pixelCounter),
                                      .rgbtBlue = round(sumB / pixelCounter)};
            blurredImage[r][c] = blurredPixel;
        }
    }

    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            image[r][c] = blurredImage[r][c];
        }
    }

    free(blurredImage);
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*processedImage)
    [width] = malloc(height * width * sizeof(RGBTRIPLE));

    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            int sumRGx = 0;
            int sumGGx = 0;
            int sumBGx = 0;
            int sumRGy = 0;
            int sumGGy = 0;
            int sumBGy = 0;

            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    int br = r - 1 + i;
                    int bc = c - 1 + j;
                    if (br >= 0 && br < height && bc >= 0 && bc < width)
                    {
                        sumRGx += image[br][bc].rgbtRed * Gx[i][j];
                        sumGGx += image[br][bc].rgbtGreen * Gx[i][j];
                        sumBGx += image[br][bc].rgbtBlue * Gx[i][j];
                        sumRGy += image[br][bc].rgbtRed * Gy[i][j];
                        sumGGy += image[br][bc].rgbtGreen * Gy[i][j];
                        sumBGy += image[br][bc].rgbtBlue * Gy[i][j];
                    }
                }
            }

            RGBTRIPLE processedPixel = {.rgbtRed = calculatePixelValue(sumRGx, sumRGy),
                                        .rgbtGreen = calculatePixelValue(sumGGx, sumGGy),
                                        .rgbtBlue = calculatePixelValue(sumBGx, sumBGy)};
            processedImage[r][c] = processedPixel;
        }
    }

    for (int r = 0; r < height; r++)
    {
        for (int c = 0; c < width; c++)
        {
            image[r][c] = processedImage[r][c];
        }
    }

    free(*processedImage);
    return;
}

int calculatePixelValue(int sumGx, int sumGy)
{
    int sum = round(sqrt(pow(sumGx, 2) + pow(sumGy, 2)));
    if (sum > 255)
    {
        return 255;
    }
    else
    {
        return sum;
    }
}
