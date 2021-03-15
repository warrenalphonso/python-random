"""
Find the start index of an instance of `pattern` in `text`.
"""
import string
from typing import List, Optional

def naive_match(pattern: str, text: str) -> Optional[int]:
    """
    Return the start index of pattern in text, or None if not found. 
    Time: O(|P||T|)    Space: O(1)

    >>> naive_match("Hello", "Hello world")
    0
    >>> naive_match("world", "Hello world")
    6
    >>> naive_match("needle", "haynestaneedlstaneedlestack")
    16
    >>> naive_match("", "123")
    0
    >>> naive_match("12", "")
    >>> naive_match("", "")
    0
    """
    for i in range(len(text) - len(pattern) + 1): 
        for j, c in enumerate(pattern): 
            if c != text[i + j]: 
                break 
        else: 
            return i 
    return None 

def prefix_match_len(s1: str, s2: str) -> int: 
    """
    Return the length of the longest prepfix match of s1 and s2. 

    >>> prefix_match_len("Hello there", "Hello ")
    6
    >>> prefix_match_len("Hello there", "Hello there")
    11
    >>> prefix_match_len("Hello there", "Bye")
    0
    >>> prefix_match_len("", "")
    0
    """
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2: 
            return i
    return min( len(s1), len(s2) )

def Z_match(pattern: str, text: str) -> Optional[int]:
    """
    Compute Z-values for each index in text until we find a Z-value |P|, which 
    means we found the pattern in the text. (0th Z-value is set to 0, because
    technically it's |P|.) 
    Time: O(|P| + |T|)    Space: O(|P|) (See "Caveats" section.) 

    Returns: 
        int if pattern was found in text, else None. 

    Raises: 
        ValueError: pattern and text must have at least one unused ascii 
            character or the space character to act as a divider. 


    Terminology: 
    A Z-value Z_i (S) is the length of the longest prefix of S starting at 
        index i. 
    A Z-box for Z_i (S) > 0 is the substring of S from i to i + Z_i (S) - 1, 
        ie a prefix of S. 


    Algorithm: 
    Track the left and right indices (l, r) of the rightmost Z-box after each 
    iteration. 

    First, manually compute Z_1 via character comparison. 

    Notice r tells us the farthest we've "seen" (since we break if a character 
    doesn't match). If we're checking the Z-value of an index i > r, we have 
    no information so we've got to do it manually via character comparison. 

    Otherwise, we need to use the information we have. 
    Compute beta = r - i + 1, which is the amount of rightmost Z-box that is 
    still remaining. This is how many more characters we've seen. 

    Here's the core trick of the algorithm. We know the substring from l to r 
    is a prefix. Now compute j = i - l, which is the start index near the 
    beginning of the entire string. It's very close to the beginning and we 
    know it matches i because i is part of a prefix. 

    Case 1: Z_j < beta. That means Z_i = Z_j because we know up to beta is a 
    prefix, but Z_j tells us that its prefix doesn't go that far. 

    Case 2: Z_j > beta. That means Z_i = beta because Z_j matches a lot more, 
    but we know our match can only go up to beta because past that isn't a 
    prefix. 

    Case 3: Z_j = beta. That means Z_i >= Z_j, so we've got to do the rest by 
    character comparison. 

    Finally, update l and r if there's a new rightmost Z-box. 


    Caveats:  
    This algorithm technically works for any string, but we'll write it to only 
    work with strings of the form P$T, where P is a pattern, T is the text to 
    search for the pattern, and $ is a character unused in P and T. 
    With this constraint, notice that we only need to track the Z-values for 
    the first |P| values, because j = i - l + 1 <= |P| because no string can 
    match $. This is what allow our space complexity to be O(|P|) instead of 
    O(|P| + |T|). 

    >>> Z_match("Hello", "Hello world")
    0
    >>> Z_match("world", "Hello world")
    6
    >>> Z_match("needle", "haynestaneedlstaneedlestack")
    16
    >>> Z_match("", "123")
    0
    >>> Z_match("12", "")
    >>> Z_match("", "")
    0
    """
    # Assume non-zero pattern when computing Z_1 
    if not pattern: 
        return 0
    if len(pattern) > len(text): 
        return None

    # Choose a divider that isn't in pattern or text 
    possible_chars = string.ascii_letters + string.digits + " "
    unused_chars = set(possible_chars) - set(pattern) - set(text)
    if unused_chars: 
        divider = unused_chars.pop()
    else: 
        raise ValueError("Pattern and text must have at least one unused ascii \
                character or space to act as a divider.")    

    # This is crucial for linear behavior in Python because we need to do a 
    # bit of string slicing when computing prefixes by character comparison. 
    # Python typically copies the strings, which *dramatically* slows down 
    # the algorithm. memoryview bypasses copying the data and allows functions 
    # that use it to directly modify it. (We won't be modifying anything; we're 
    # only reading the characters to do character comparisons.)
    s = memoryview( bytes(pattern + divider + text, encoding='utf-8') )

    l = r = 0
    Z_values = [0]

    for i in range(1, len(s)): 
        if i > r: 
            # No information so use character comparison 
            Z_i = prefix_match_len(s[i:], s)
        else: 
            beta = r - i + 1
            j = i - l

            if Z_values[j] < beta: 
                Z_i = Z_values[j]
            elif Z_values[j] > beta: 
                Z_i = beta 
            else: 
                Z_i = beta # or Z_scores[j] since they're equivalent
                Z_i += prefix_match_len(s[i + Z_i:], s[Z_i:])

        # Are we done? 
        if Z_i == len(pattern):
            return i - len(pattern) - 1

        # Only store if in prefix to have O(|P|) space        
        if i < len(pattern):
            Z_values.append(Z_i)

        if i + Z_i - 1 > r: 
            l, r = i, i + Z_i - 1
    return None


if __name__ == "__main__":
    from doctest import testmod 
    testmod()
