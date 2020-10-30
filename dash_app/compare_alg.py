"""
Comparison between the efficiency of the Boyer-Moore algorithm and the naive substring search algorithm.
The runtimes for both algorithms are plotted on the same axes.
"""

import matplotlib.pyplot as plt
import numpy as np
import string
import time
import random
from bm_alg import boyer_moore_match, naive_match

# number of test cases for each iteration
TEST_CASES = 100

# test cases generated based on this pattern (vary_n)
PATTERN = 'ICT1002 is a really great module!'

# test cases generated based on this text    (vary_m)
TEXT = PATTERN * 50


def generate_test_cases(pattern, length, k):
    """
    Generates <k> test cases with text of length <length> containing <pattern>

    Args:
        pattern (str): A pattern within the text.
        length (int): The length of the pattern
        k (int): The number of test cases

    Returns:
        A list of test cases, i.e. strings that contain <pattern>
    """
    result = []
    for _ in range(k):
        text = pattern
        while len(text) < length:
            direction = random.choice((0, 1))

            # 0 --> Left
            if direction == 0:
                text = random.choice(string.ascii_lowercase) + text

            # 1 --> Right
            else:
                text = text + random.choice(string.ascii_lowercase)

        result.append(text)

    return result


def vary_n(max_n):
    x = [n for n in range(1, max_n + 1)]
    y_bm = []
    y_naive = []

    for n in x:
        print('n =', n)
        bm_result = []
        naive_result = []

        if n >= len(PATTERN):
            # generate test cases of length n, which contain PATTERN
            test_cases = generate_test_cases(PATTERN, n, TEST_CASES)
        else:
            # generate test cases of length n, which do not (and can not possibly) contain PATTERN
            test_cases = generate_test_cases('', n, TEST_CASES)

        for test_case in test_cases:
            start = time.time()
            naive_match(test_case, PATTERN)
            naive_result.append(time.time() - start)

            start = time.time()
            boyer_moore_match(test_case, PATTERN)
            bm_result.append(time.time() - start)

        # obtain median runtime (mean is affected by outliers)
        y_naive.append(sorted(naive_result)[TEST_CASES // 2])
        y_bm.append(sorted(bm_result)[TEST_CASES // 2])

    plt.plot(x, y_naive, label="Naive Algorithm")
    plt.plot(x, y_bm, label="Boyer-Moore Algorithm")
    plt.xlabel("n")
    plt.ylabel("Runtime")
    plt.title("Substring Search Algorithm Efficiency")
    plt.legend()
    plt.show()


def vary_m(max_m):
    x = [m for m in range(1, max_m + 1)]
    y_bm = []
    y_naive = []

    for m in x:
        print('m =', m)
        bm_result = []
        naive_result = []

        # generate test cases of length n
        test_cases = generate_test_cases('', m, TEST_CASES)

        for test_case in test_cases:
            start = time.time()
            naive_match(TEXT, test_case)
            naive_result.append(time.time() - start)

            start = time.time()
            boyer_moore_match(TEXT, test_case)
            bm_result.append(time.time() - start)

        # obtain median runtime (mean is affected by outliers)
        y_naive.append(sorted(naive_result)[TEST_CASES // 2])
        y_bm.append(sorted(bm_result)[TEST_CASES // 2])

    plt.plot(x, y_naive, label="Naive Algorithm")
    plt.plot(x, y_bm, label="Boyer-Moore Algorithm")
    plt.xlabel("m")
    plt.ylabel("Runtime")
    plt.title("Substring Search Algorithm Efficiency")
    plt.legend()
    plt.show()


def main():
    done = False
    print("m = Length of pattern\nn = Length of text\n")
    print("1. Constant m, vary n")
    print("2. Constant n, vary m")
    print("3. Quit\n")

    while not done:
        choice = input("Your choice: ")

        if choice == '1':
            max_n = input("Upper limit of n: ")
            while not (max_n.isnumeric() and int(max_n) > 1):
                print("That is not a valid number.")
                max_n = input("Upper limit of n: ")
            vary_n(int(max_n))

        elif choice == '2':
            max_m = input("Upper limit of m: ")
            while not (max_m.isnumeric() and int(max_m) > 1):
                print("That is not a valid number.")
                max_m = input("Upper limit of m: ")
            vary_m(int(max_m))

        elif choice == '3':
            done = True

        else:
            print("That is not a valid option.")


if __name__ == '__main__':
    main()
