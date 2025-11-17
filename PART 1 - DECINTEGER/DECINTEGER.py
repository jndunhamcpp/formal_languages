import os

START = "START"
ZERO_DIGIT = "ZERO_DIGIT"
NONZERO_DIGIT = "NONZERO_DIGIT"
UNDERSCORE_AFTER_ZERO = "UNDERSCORE_AFTER_ZERO"
UNDERSCORE_AFTER_NONZERO = "UNDERSCORE_AFTER_NONZERO"
DEAD = "DEAD"

ACCEPTING_STATES = {
    ZERO_DIGIT,
    NONZERO_DIGIT
}

CHAR_ZERO = "ZERO"
CHAR_NONZERO_DIGIT = "NONZERO_DIGIT"
CHAR_UNDERSCORE = "UNDERSCORE"
CHAR_OTHER = "OTHER"

def parse_char(ch):
    if ch == "0":
        return CHAR_ZERO
    elif "1" <= ch <= "9":
        return CHAR_NONZERO_DIGIT
    elif ch == "_":
        return CHAR_UNDERSCORE
    else:
        return CHAR_OTHER

TRANSITIONS = {
    START: {
        CHAR_ZERO: ZERO_DIGIT,
        CHAR_NONZERO_DIGIT: NONZERO_DIGIT,
    },
    ZERO_DIGIT: { },
    NONZERO_DIGIT: {
        CHAR_ZERO: NONZERO_DIGIT,
        CHAR_NONZERO_DIGIT: NONZERO_DIGIT,
        CHAR_UNDERSCORE: UNDERSCORE_AFTER_NONZERO,
    },
    UNDERSCORE_AFTER_NONZERO: {
        CHAR_ZERO: NONZERO_DIGIT,
        CHAR_NONZERO_DIGIT: NONZERO_DIGIT,
    },
    DEAD: {},
}

def step(state, ch):
    char_class = parse_char(ch)
    return TRANSITIONS.get(state, {}).get(char_class, DEAD)

def literal_test(s):
    state = START
    for ch in s:
        state = step(state, ch)
        if state == DEAD:
            break

    return state in ACCEPTING_STATES

def run_batch_tests(input_filename="in_ans.txt", output_filename="out.txt"):
    if not os.path.exists(input_filename):
        return False

    lines = []
    with open(input_filename, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            literal = parts[0]
            expected = parts[1].upper()
            if expected not in ("ACCEPTED", "REJECTED"):
                continue
            lines.append((literal, expected))

    results = []
    for literal, expected in lines:
        actual_bool = literal_test(literal)
        actual = "ACCEPTED" if actual_bool else "REJECTED"
        result = "PASS" if actual == expected else "FAIL"
        results.append((literal, expected, actual, result))

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("literal\texpected\tactual\tresult\n")
        for literal, expected, actual, result in results:
            f.write(f"{literal}\t{expected}\t{actual}\t{result}\n")

    print(f"Output saved to: {output_filename}.")
    return True

def interactive():
    while True:
        s = input("Enter a Python decinteger literal: ").strip()
        if literal_test(s):
            print("Accepted")
        else:
            print("Rejected")


if __name__ == "__main__":
    ran_batch = run_batch_tests()
    if not ran_batch:
        interactive()
