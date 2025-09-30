def get_valid_string(prompt):
    while True:
        s = input(prompt).strip()
        if 6 <= len(s) <= 10:
            return s
        else:
            print("Error: Enter a string between 6 and 10 characters.")

def align_strings(s1, s2):
    max_len = max(len(s1), len(s2))
    return s1.ljust(max_len), s2.ljust(max_len)

def compare_strings(s1, s2):
    s1, s2 = align_strings(s1, s2)
    match_line = ""
    matches = 0

    for a, b in zip(s1, s2):
        if a == b:
            match_line += "*"
            matches += 1
        else:
            match_line += "x"

    similarity = (matches / len(s1)) * 100
    return s1, s2, match_line, matches, similarity

def main():
    print("🔤 String Similarity Checker (6–10 characters)")
    str1 = get_valid_string("Enter first string: ")
    str2 = get_valid_string("Enter second string: ")

    aligned1, aligned2, match_line, matches, similarity = compare_strings(str1, str2)

    print("\nComparison Result:")
    print(f"String 1 : {aligned1}")
    print(f"String 2 : {aligned2}")
    print(f"Match    : {match_line}")
    print(f"Matches  : {matches} / {len(aligned1)}")
    print(f"Similarity: {similarity:.2f}%")

if __name__ == "__main__":
    main()
