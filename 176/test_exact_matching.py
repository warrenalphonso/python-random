"""

"""
from hypothesis import given, strategies as st
import string

from exact_matching import naive_match, Z_match

alphabet = string.ascii_letters

"""
Test naive_match
"""
@given(st.text(alphabet=alphabet), st.text(alphabet=alphabet))
def test_naive_random_patterns_texts(pattern, text): 
    try: 
        found = text.index(pattern)
    except: 
        found = None
    assert naive_match(pattern, text) == found

"""
Test Z_match
"""
@given(st.text(alphabet=alphabet), st.text(alphabet=alphabet))
def test_Z_random_patterns_texts(pattern, text): 
    try: 
        found = text.index(pattern)
    except: 
        found = None
    assert Z_match(pattern, text) == found


