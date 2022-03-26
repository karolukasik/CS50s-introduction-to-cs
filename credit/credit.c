#include <cs50.h>
#include <stdio.h>

int length(long number);
bool isVisa(int array[], int length);
bool isAmericanExpress(int array[], int length);
bool isMasterCard(int array[], int length);

int main(void)
{
    long cardNumber = get_long("Number: ");
    int lengthOfNumber = length(cardNumber);
    int digits[lengthOfNumber];
    for (int i = 0; i < lengthOfNumber; i++)
    {
        digits[i] = cardNumber % 10;
        cardNumber = cardNumber / 10;
    }

    int controlSum = 0;
    for (int i = 0; i < lengthOfNumber; i++)
    {
        if (i % 2 == 0)
        {
            controlSum += digits[i];
        }
        else
        {
            int multipliedByTwo = digits[i] * 2;
            if (multipliedByTwo >= 10)
            {
                for (int j = 0; j < 2; j++)
                {
                    controlSum += multipliedByTwo % 10;
                    multipliedByTwo = multipliedByTwo / 10;
                }
            }
            else
            {
                controlSum += multipliedByTwo;
            }
        }
    }

    if (controlSum % 10 == 0)
    {
        if (isAmericanExpress(digits, lengthOfNumber))
        {
            printf("AMEX\n");
        }
        else if (isVisa(digits, lengthOfNumber))
        {
            printf("VISA\n");
        }
        else if (isMasterCard(digits, lengthOfNumber))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

int length(long number)
{
    int counter = 0;
    while (number > 0)
    {
        number = number / 10;
        counter++;
    }
    return counter;
}

bool isVisa(int array[], int length)
{
    if (length == 13 || length == 16)
    {
        int numberToCheck = array[length - 1];
        if (numberToCheck == 4)
        {
            return true;
        }
    }
    return false;
}

bool isAmericanExpress(int array[], int length)
{
    if (length == 15)
    {
        int numberToCheck = array[length - 1] * 10 + array[length - 2];
        if (numberToCheck == 34 || numberToCheck == 37)
        {
            return true;
        }
    }
    return false;
}

bool isMasterCard(int array[], int length)
{
    if (length == 16)
    {
        int numberToCheck = array[length - 1] * 10 + array[length - 2];
        if (numberToCheck >= 51 && numberToCheck <= 55)
        {
            return true;
        }
    }
    return false;
}
