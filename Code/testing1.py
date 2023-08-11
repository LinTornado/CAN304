import hashlib
import random

import MD5

'''
This is testing class for the correctness of MD5 implementation.
The results will be compared with hashlib. 
'''


def generateRandomStrings(string_length, count):
    random_strings = []
    base_string = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    base_length = len(base_string) - 1
    for i in range(0, count):
        random_string = ''
        for j in range(0, string_length):
            random_string += base_string[random.randint(0, base_length)]
        random_strings.append(random_string)
    return random_strings


def checkCorrectness():
    correctness = True
    for x in range(0, 10):  # 10 loops in total
        # for each loop, generate 100 random strings with length of 64.
        random_strings = generateRandomStrings(64, 100)
        for y in range(0, len(random_strings)):
            this_string = random_strings[y]
            # get hashlib md5 result
            hashlib_md5 = hashlib.md5()
            hashlib_md5.update(this_string.encode('utf-8'))
            hashlib_result = hashlib_md5.hexdigest()
            # get homemade md5 result
            impl_md5 = MD5.MD5(this_string)
            impl_result = impl_md5.getStringResult()
            # compare the MD5 result
            if hashlib_result != impl_result:
                correctness = False
        print("Round {} finished".format(x + 1))
    return correctness


if __name__ == '__main__':
    result = checkCorrectness()
    print("Correctness: {}".format(result))
