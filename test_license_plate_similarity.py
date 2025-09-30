# test_license_plate_similarity.py

import re
import random
import string
import pytest
from q5.string_similarity import compare_strings

# --------- License Plate Generator ---------

def generate_valid_plate():
    state_codes = ['KA', 'MH', 'DL', 'TN', 'UP', 'RJ', 'GJ']
    state = random.choice(state_codes)
    rto = str(random.randint(1, 99)).zfill(2)
    series = ''.join(random.choices(string.ascii_uppercase, k=2))
    number = str(random.randint(0, 9999)).zfill(4)
    return f"{state}{rto}{series}{number}"  # Format: KA01AB1234

def generate_invalid_plate():
    formats = [
        lambda: ''.join(random.choices(string.digits, k=10)),       # All digits
        lambda: ''.join(random.choices(string.ascii_letters, k=10)),# All letters
        lambda: 'XX' + str(random.randint(100000, 999999)),         # Wrong format
        lambda: '12345678',                                         # Too short
        lambda: 'INVALID!!',                                        # Special characters
    ]
    return random.choice(formats)()

# --------- Generate Test Data (Paired Strings) ---------

test_cases = []
for _ in range(500):
    valid = generate_valid_plate()
    noisy_valid = valid[:6] + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    test_cases.append((valid, noisy_valid, True))

for _ in range(500):
    invalid = generate_invalid_plate()
    test_cases.append((generate_valid_plate(), invalid, False))

# --------- Test Function Using compare_strings ---------

@pytest.mark.parametrize("str1,str2,should_match", test_cases)
def test_plate_similarity(str1, str2, should_match):
    aligned1, aligned2, match_line, matches, similarity = compare_strings(str1, str2)

    # Define threshold: above 70% similarity = good match
    passed = similarity >= 70

    if should_match:
        assert passed, f"Expected match, got similarity {similarity:.2f}%\n{str1} vs {str2}"
    else:
        assert not passed, f"Expected mismatch, got similarity {similarity:.2f}%\n{str1} vs {str2}"
