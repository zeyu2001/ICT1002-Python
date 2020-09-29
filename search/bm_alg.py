"""
WHY BOYER-MOORE ALGORITHM?

Boyer-Moore's approach is to try to match the last character of the pattern instead of the first one with the 
assumption that if there's not match at the end no need to try to match at the beginning. This allows for "big jumps" 
therefore BM works better when the pattern and the text you are searching resemble "natural text" (i.e. English)

Knuth-Morris-Pratt searches for occurrences of a "word" W within a main "text string" S by employing the observation 
that when a mismatch occurs, the word itself embodies sufficient information to determine where the next match could 
begin, thus bypassing re-examination of previously matched characters. This means KMP is better suited for small sets 
like DNA (ACTG)
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


    
"""To search for any pattern in text, if pattern is not found in text, return -1, if pattern is found, returns the start of the index"""
def boyer_moore_match(text, pattern):
    """Find occurrence of pattern in text."""
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


assert boyer_moore_match("abcd", "cd") == 2
assert boyer_moore_match("abcd", "lol") == -1
assert boyer_moore_match("ICT1002", "ICT") == 0
