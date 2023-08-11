import copy
import random
import time

import MD5
import MD5Pro


def getFileMD5New(file):
    with open(file, "rb") as f:
        content = list(f.read())
    return MD5Pro.MD5Pro(content).getFileResult()


def getFileMD5Old(file):
    with open(file, "rb") as f:
        content = list(f.read())
    return MD5.MD5(content).getFileResult()


def getStringMD5New(string):
    # get a shallow copy of input string
    string_copy = copy.copy(string)
    return MD5Pro.MD5Pro(string_copy).getStringResult()


def getStringMD5Old(string):
    # get a shallow copy of input string
    string_copy = copy.copy(string)
    return MD5.MD5(string_copy).getStringResult()


def getRepeatRate(str1, str2):
    dict1 = {}
    dict2 = {}
    repeat = 0
    for char in str1:
        if char not in dict1:
            dict1[char] = 1
        else:
            dict1[char] += 1
    for char in str2:
        if char not in dict2:
            dict2[char] = 1
        else:
            dict2[char] += 1
    for key1 in dict1:
        for key2 in dict2:
            if key1 == key2:
                repeat += min(dict1[key1], dict2[key2])
    rate = repeat / len(str2)
    return rate


def getAverageRate(listA, listB):
    totalRate = 0
    for i in range(100):
        dict_1 = {}
        dict_2 = {}
        for char in listA[i]:
            if char not in dict_1:
                dict_1[char] = 1
            else:
                dict_1[char] += 1

        for char in listB[i]:
            if char not in dict_2:
                dict_2[char] = 1
            else:
                dict_2[char] += 1

        repeatNumber = 0
        for key1 in dict_1:
            for key2 in dict_2:
                if key1 == key2:
                    repeatNumber += min(dict_1[key1], dict_2[key2])

        totalRate += repeatNumber / len(listB[i])

    averageRate = totalRate / 100
    return averageRate


def getAverageAvalanche(listA, listB):
    totalAvalanche = 0
    for i in range(100):
        count = 0
        for j, char in enumerate(listA[i]):
            if char == listB[i][j]:
                count += 1

        totalAvalanche += 1 - count / len(listB[i])

    averageAvalanche = totalAvalanche / 100
    return averageAvalanche


def getAvalanche(str1, str2):
    count = 0
    for i, char in enumerate(str1):
        if char == str2[i]:
            count += 1
    avalanche = 1 - count / len(str2)
    return avalanche


def getStringPair():
    # generate a random string and its pair where only 1 digit is changed
    # get 100 pairs of those strings
    alphabet = {}
    for i in range(1, 27):
        alphabet[str(i)] = chr(i + 96)

    listA = []
    listB = []

    for i in range(1, 6):
        for j in range(20):
            stringA = ''
            for k in range(20 * i):
                stringA += alphabet[str(random.randint(1, 26))]

            stringB = stringA
            while stringB == stringA:
                replace_index = random.randint(0, len(stringA) - 1)
                new_letter = alphabet[str(random.randint(1, 26))]
                stringB = stringA[:replace_index] + new_letter + stringA[replace_index + 1:]

            listA.append(stringA)
            listB.append(stringB)

    return listA, listB


def collisionTest(file1, file2):
    file1_old = getFileMD5Old(file1)
    file2_old = getFileMD5Old(file2)

    file1_new = getFileMD5New(file1)
    file2_new = getFileMD5New(file2)

    print("###### MD5 collision for 2 files ######")
    print("File directory: ")
    print("file 1: {}".format(file1))
    print("file 2: {}".format(file2))
    print("For original MD5: ")
    print("file 1: {}".format(file1_old))
    print("file 2: {}".format(file2_old))
    print("Is collided? {}".format(file1_old == file2_old))
    print("For improved MD5Pro: ")
    print("file 1: {}".format(file1_new))
    print("file 2: {}".format(file2_new))
    print("Is collided? {}".format(file1_new == file2_new))


def rateComparison(string1, string2):
    string1_new = getStringMD5New(string1)
    string2_new = getStringMD5New(string2)
    rate_new = getRepeatRate(string1_new, string2_new)

    string1_old = getStringMD5Old(string1)
    string2_old = getStringMD5Old(string2)
    rate_old = getRepeatRate(string1_old, string2_old)

    print("###### Repeat rate comparison for 2 strings ######")
    print("String 1: {}".format(string1))
    print("String 2: {}".format(string2))
    print("Old ciphertext of string 1: {}".format(string1_old))
    print("Old ciphertext of string 2: {}".format(string2_old))
    print("Original MD5 repeat rate: {}".format(rate_old))
    print("New ciphertext of string 1: {}".format(string1_new))
    print("New ciphertext of string 2: {}".format(string2_new))
    print("Improved MD5Pro repeat rate: {}".format(rate_new))


def avalancheComparison(string1, string2):
    string1_new = getStringMD5New(string1)
    string2_new = getStringMD5New(string2)
    avalanche_new = getAvalanche(string1_new, string2_new)

    string1_old = getStringMD5Old(string1)
    string2_old = getStringMD5Old(string2)
    avalanche_old = getAvalanche(string1_old, string2_old)

    print("###### Avalanche effect comparison for 2 strings ######")
    print("String 1: {}".format(string1))
    print("String 2: {}".format(string2))
    print("Original MD5 avalanche: {}".format(avalanche_old))
    print("Improved MD5Pro avalanche: {}".format(avalanche_new))


def averageTimeComparison():
    listA, listB = getStringPair()
    process_time_new = 0
    process_time_old = 0

    for stringA in listA:
        start_time_new = time.time()
        getStringMD5New(stringA)
        end_time_new = time.time()
        process_time_new += end_time_new - start_time_new

        start_time_old = time.time()
        getStringMD5Old(stringA)
        end_time_old = time.time()
        process_time_old += end_time_old - start_time_old

    average_time_new = process_time_new / 100
    average_time_old = process_time_old / 100

    print("###### Average processing time for 100 randomly generated strings ######")
    print("Original MD5 average processing time: {:.8f}".format(average_time_old))
    print("Improved MD5Pro average processing time: {:.8f}".format(average_time_new))
    print("Time gap (old - new): {:.8f}".format(average_time_old - average_time_new))


def averageRateAndAvalancheComparison():
    listA, listB = getStringPair()
    listA_new = []
    listB_new = []
    listA_old = []
    listB_old = []

    for stringA in listA:
        stringA_new = getStringMD5New(stringA)
        listA_new.append(stringA_new)
        stringA_old = getStringMD5Old(stringA)
        listA_old.append(stringA_old)

    for stringB in listB:
        stringB_new = getStringMD5New(stringB)
        listB_new.append(stringB_new)
        stringB_old = getStringMD5Old(stringB)
        listB_old.append(stringB_old)

    average_rate_new = getAverageRate(listA_new, listB_new)
    average_rate_old = getAverageRate(listA_old, listB_old)
    print("###### Average repeat rate for 100 randomly generated strings ######")
    print("Original MD5 average repeat rate: {}".format(average_rate_old))
    print("Improved MD5Pro average repeat rate: {}".format(average_rate_new))

    average_avalanche_new = getAverageAvalanche(listA_new, listB_new)
    average_avalanche_old = getAverageAvalanche(listA_old, listB_old)
    print("###### Average avalanche for 100 randomly generated strings ######")
    print("Original MD5 average avalanche: {}".format(average_avalanche_old))
    print("Improved MD5Pro average avalanche: {}".format(average_avalanche_new))


def runAllTest(file_1, file_2, string_1, string_2):
    collisionTest(file_1, file_2)
    print()
    # repeat rate comparison
    rateComparison(string_1, string_2)
    print()
    # avalanche comparison
    avalancheComparison(string_1, string_2)
    print()
    # average processing time
    averageTimeComparison()
    print()
    # average repeat rate and avalanche
    averageRateAndAvalancheComparison()
