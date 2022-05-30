# TODO
import string


def main():
    text = input("Text: ")

    grade = calculateTextGrade(text)

    if grade < 1:
        print("Before Grade 1")
    elif grade in range(1, 15):
        print(f"Grade {grade}")
    else:
        print("Grade 16+")


def calculateNumberOfLetters(text):
    counter = 0
    for i in text:
        if i in list(string.ascii_lowercase) or i in list(string.ascii_uppercase):
            counter += 1
    return counter


def calculateNumberOfWords(text):
    listOfWords = text.split()
    return len(listOfWords)


def calculateNumberOfSentences(text):
    counter = 0
    for i in text:
        if i in [".", "!", "?"]:
            counter += 1
    return counter


def calculateTextGrade(text):

    averageNumberOfLetters = averagePerHundredWords(
        calculateNumberOfLetters(text), text)
    averageNumberOfSentences = averagePerHundredWords(
        calculateNumberOfSentences(text), text)
    grade = 0.0588*averageNumberOfLetters - 0.296*averageNumberOfSentences - 15.8
    return round(grade)


def averagePerHundredWords(number, text):
    return 100*number / calculateNumberOfWords(text)


main()
