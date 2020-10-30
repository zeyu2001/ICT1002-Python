"""
Implementation of the Boyer-Moore substring search algorithm, as well as the naive algorithm for comparison.

Boyer-Moore's approach is to try to match the last character of the pattern instead of the first one with the 
assumption that if there's no match at the end, no need to try to match at the beginning. This allows for "big jumps" 
therefore BM works better when the pattern and the text you are searching resemble "natural text" (i.e. English)
"""


class last_occurrence(object):
    """Last occurrence functor."""

    def __init__(self, pattern, alphabet):
        """Generate a dictionary with the last occurrence of each alphabet
        letter inside the pattern.

        Note: This function uses str.rfind, which already is a pattern
        matching algorithm. There are more 'basic' ways to generate this
        dictionary."""
        self.occurrences = dict()
        for letter in alphabet:
            self.occurrences[letter] = pattern.rfind(letter)

    def __call__(self, letter):
        """Return last position of the specified letter inside the pattern.
        Return -1 if letter not found in pattern."""
        return self.occurrences[letter]


def boyer_moore_match(text, pattern):
    """
    Find occurrence of pattern in text. If pattern is not found in text, return -1.
    If pattern is found, returns the start of the index.

    Args:
        text (str): A string of text.
        pattern (str): A pattern to find within <text>.

    Returns: 
        Starting index of the pattern if pattern is found, else -1.
    """
    alphabet = set(text)
    last = last_occurrence(pattern, alphabet)
    m = len(pattern)
    n = len(text)
    i = m - 1  # text index
    j = m - 1  # pattern index
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            l = last(text[i])
            i = i + m - min(j, 1+l)
            j = m - 1
    return -1


def naive_match(text, pattern):
    """
    Naive implementation of a substring search algorithm. Time complexity is O(mn).
    Find occurrence of pattern in text. If pattern is not found in text, return -1.
    If pattern is found, returns the start of the index.

    Args:
        text (str): A string of text.
        pattern (str): A pattern to find within <text>.

    Returns: 
        Starting index of the pattern if pattern is found, else -1.
    """
    M = len(pattern)
    N = len(text)

    # A loop to slide pat[] one by one */
    for i in range(N - M + 1):
        j = 0

        # For current index i, check
        # for pattern match */
        while(j < M):
            if (text[i + j] != pattern[j]):
                break
            j += 1

        if (j == M):
            return i

    return -1


def tests():
    try:
        assert boyer_moore_match("abcd", "cd") == 2
        assert boyer_moore_match("abcd", "lol") == -1
        assert boyer_moore_match("ICT1002", "ICT") == 0
    except AssertionError:
        print("Something went wrong...")

    print('Test Cases Passed.')


if __name__ == '__main__':
    tests()
