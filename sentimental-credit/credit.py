# TODOint length(long number);
from cs50 import get_int


def main():
    cardNumber = input("Number: ")
    lengthOfNumber = len(cardNumber)
    digits = []
    for i in range(0, lengthOfNumber):
        digits.append(int(cardNumber) % 10)
        cardNumber = int(cardNumber) // 10

    controlSum = 0
    for i in range(0, lengthOfNumber):
        if i % 2 == 0:
            controlSum += digits[i]
        else:
            multipliedByTwo = digits[i] * 2
            if multipliedByTwo >= 10:
                controlSum += 1 + multipliedByTwo % 10
            else:
                controlSum += multipliedByTwo

    if controlSum % 10 == 0:
        if isAmericanExpress(digits, lengthOfNumber):
            print("AMEX")
        elif isVisa(digits, lengthOfNumber):
            print("VISA")
        elif isMasterCard(digits, lengthOfNumber):
            print("MASTERCARD")
        else:
            print("INVALID")
    else:
        print("INVALID")


def isVisa(array, length):
    if length == 13 or length == 16:
        numberToCheck = array[length - 1]
        if numberToCheck == 4:
            return True
    return False


def isAmericanExpress(array, length):
    if length == 15:
        numberToCheck = array[length - 1] * 10 + array[length - 2]
        if numberToCheck == 34 or numberToCheck == 37:
            return True
    return False


def isMasterCard(array, length):

    if length == 16:
        numberToCheck = array[length - 1] * 10 + array[length - 2]
        if numberToCheck >= 51 and numberToCheck <= 55:
            return True
    return False


main()
