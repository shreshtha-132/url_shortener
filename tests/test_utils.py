import string
from utils import generate_short_code

def test_generate_short_code_length():
    code = generate_short_code(8)
    assert len(code) == 8

def test_generate_short_code_charset():
    code = generate_short_code(10)
    for char in code:
        assert char in (string.ascii_letters + string.digits)