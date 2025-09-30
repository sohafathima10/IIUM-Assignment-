# License Plate Similarity Test Suite

This project provides automated tests for a string similarity function, focusing on Indian license plate formats. It uses `pytest` to ensure the similarity function correctly identifies valid and invalid license plate strings.

## Features

- Generates realistic Indian license plate numbers (e.g., KA01AB1234)
- Creates noisy versions of valid plates for positive tests
- Generates various invalid plate formats for negative tests
- Runs 1,000+ test cases using `pytest` parameterization
- Uses a 70% similarity threshold to determine matches

## How It Works

1. **Test Data Generation:**
   - Valid plates are generated in the format: `KA01AB1234`.
   - Noisy valid plates are created by altering the last 4 characters.
   - Invalid plates include all digits, all letters, wrong formats, short plates, and special characters.

2. **Testing:**
   - For each test case, the `compare_strings` function (from `q5.string_similarity`) is called.
   - If the pair should match, the similarity must be ≥ 70%.
   - If the pair should not match, the similarity must be < 70%.

## How to Run

1. Make sure you have Python 3 and `pytest` installed:
   ```
   pip install pytest
   ```

2. Place `test_license_plate_similarity.py` in your project folder.

3. Ensure `q5/string_similarity.py` exists and contains the `compare_strings` function.

4. Run the tests:
   ```
   pytest test_license_plate_similarity.py
   ```

## Files

- `test_license_plate_similarity.py` — Test suite
- `q5/string_similarity.py` — String similarity function

---

**Author:**  
IIUM Assignment  
September 2025