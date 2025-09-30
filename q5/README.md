
This Python program compares two strings (each 6–10 characters long) and calculates their similarity. It shows which characters match and provides a similarity percentage.

## Features

- Prompts user for two strings (6–10 characters)
- Aligns strings for comparison
- Displays matching and non-matching characters
- Shows total matches and similarity percentage

## How It Works

1. The program asks you to enter two strings, each between 6 and 10 characters.
2. It aligns both strings to the same length.
3. It compares each character:
   - `*` means the characters match
   - `x` means they do not match
4. It calculates and displays the similarity percentage.

## Example Output

```
🔤 String Similarity Checker (6–10 characters)
Enter first string: ABC123
Enter second string: ABD124

Comparison Result:
String 1 : ABC123
String 2 : ABD124
Match    : **x**x*
Matches  : 4 / 6
Similarity: 66.67%
```

## How to Run

1. Make sure you have Python 3 installed.
2. Open a terminal in the folder containing `string_similarity.py`.
3. Run the script:
   ```
   python string_similarity.py
   ```

## Files

- `string_similarity.py` — Main program file

---

**Author:**  
IIUM Assignment  
September 2025