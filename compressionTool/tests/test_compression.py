import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from compression import read_file

def test_read_file() :
    assert read_file("abcd")
    assert read_file("abcd",123)