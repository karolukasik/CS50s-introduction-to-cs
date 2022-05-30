import csv
import sys
from sys import argv


def main():

    # TODO: Check for command-line usage

    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable

    database = argv[1]
    nameAndSubsequences = []
    databaseOfSTRs = []
    with open(database, "r") as file:
        reader = csv.reader(file)
        header = True
        for row in reader:
            if header == True:
                for j in range(0, len(row)):
                    nameAndSubsequences.append(row[j])
                header = False
            else:
                tempDict = createDict(nameAndSubsequences, row)
                databaseOfSTRs.append(tempDict)

    # TODO: Read DNA sequence file into a variable

    sequenceFileName = argv[2]
    sequenceFile = open(sequenceFileName, "r")
    for line in sequenceFile:
        sequence = line.rstrip()
    sequenceFile.close()

    # TODO: Find longest match of each STR in DNA sequence

    currentlyCheckedSequence = {}
    for i in range(1, len(nameAndSubsequences)):
        currentSTR = nameAndSubsequences[i]
        numberOfSTRs = longest_match(sequence, currentSTR)
        currentlyCheckedSequence[currentSTR] = numberOfSTRs

    # TODO: Check database for matching profiles
    for record in databaseOfSTRs:
        numberOfMatches = 0
        listOfSubsequences = currentlyCheckedSequence.keys()

        for subsequence in listOfSubsequences:
            occurencesInRecord = record.get(subsequence)
            occurencesInCheckedSequence = currentlyCheckedSequence.get(
                subsequence)
            # print(numberOfSTRsInCheckedSequence)
            if int(occurencesInRecord) == occurencesInCheckedSequence:
                numberOfMatches = numberOfMatches + 1
            if numberOfMatches == len(listOfSubsequences):
                print(record.get("name"))
                return(0)
    print("No match")


def createDict(keys, values):
    dict = {}
    for i in range(0, len(values)):
        dict[keys[i]] = values[i]
    return dict


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
