import os

# States
START = "START"

# Dec
DEC_ZERO = "DEC_ZERO"
DEC_NONZERO = "DEC_NONZERO"
DEC_UND_AFTER_ZERO = "DEC_UND_AFTER_ZERO"
DEC_UND_AFTER_NONZERO = "DEC_UND_AFTER_NONZERO"

# Oct
OCT_PREFIX_O = "OCT_PREFIX_O"
OCT_DIGIT = "OCT_DIGIT"
OCT_UND = "OCT_UND"

# Hex
HEX_PREFIX_0 = "HEX_PREFIX_0"
HEX_PREFIX_X = "HEX_PREFIX_X"
HEX_DIGIT = "HEX_DIGIT"
HEX_UND = "HEX_UND"

# Float States - Point Notation
FLOAT_POINT_AFTER_DEC = "FLOAT_POINT_AFTER_DEC"
FLOAT_FRAC = "FLOAT_FRAC"
FLOAT_FRAC_UND = "FLOAT_FRAC_UND"
FLOAT_POINT_ONLY = "FLOAT_POINT_ONLY"

DEAD = "DEAD"

ACCEPTING_STATES = {
    DEC_ZERO,
    DEC_NONZERO,
    OCT_DIGIT,
    HEX_DIGIT,
    FLOAT_POINT_AFTER_DEC,
    FLOAT_FRAC
}

# Classify Characters
def classify(char):
    if char == "0":
        return "ZERO"
    if "1" <= char <= "7":
        return "OCT_DIG"
    if "8" <= char <= "9":
        return "DEC_ONLY_DIG"
    if "a" <= char.lower() <= "f":
        return "HEX_DIG"
    if char == "_":
        return "UND"
    if char.lower() == "x":
        return "X"
    if char.lower() == "o":
        return "O"
    if char.lower() == "e":
        return "E"
    if char == ".":
        return "DOT"
    if char == "+":
        return "PLUS"
    if char == "-":
        return "MINUS"
    return "OTHER"


TRANSITIONS = {

    START: {
        "ZERO": DEC_ZERO,
        "OCT_DIG": DEC_NONZERO,
        "DEC_ONLY_DIG": DEC_NONZERO,
        "DOT": FLOAT_POINT_ONLY,
    },

    # Dec
    DEC_ZERO: {
        "O": OCT_PREFIX_O,
        "X": HEX_PREFIX_X,
        "DOT": FLOAT_POINT_AFTER_DEC,
    },
    DEC_NONZERO: {
        "ZERO": DEC_NONZERO,
        "OCT_DIG": DEC_NONZERO,
        "DEC_ONLY_DIG": DEC_NONZERO,
        "UND": DEC_UND_AFTER_NONZERO,
        "DOT": FLOAT_POINT_AFTER_DEC,
    },
    DEC_UND_AFTER_NONZERO: {
        "ZERO": DEC_NONZERO,
        "OCT_DIG": DEC_NONZERO,
        "DEC_ONLY_DIG": DEC_NONZERO,
    },

    # Oct
    OCT_PREFIX_O: {
        "OCT_DIG": OCT_DIGIT,
        "ZERO": OCT_DIGIT,
    },
    OCT_DIGIT: {
        "OCT_DIG": OCT_DIGIT,
        "ZERO": OCT_DIGIT,
        "UND": OCT_UND,
    },
    OCT_UND: {
        "OCT_DIG": OCT_DIGIT,
        "ZERO": OCT_DIGIT,
    },

    # Hex
    HEX_PREFIX_X: {
        "ZERO": HEX_DIGIT,
        "OCT_DIG": HEX_DIGIT,
        "DEC_ONLY_DIG": HEX_DIGIT,
        "HEX_DIG": HEX_DIGIT,
    },
    HEX_DIGIT: {
        "ZERO": HEX_DIGIT,
        "OCT_DIG": HEX_DIGIT,
        "DEC_ONLY_DIG": HEX_DIGIT,
        "HEX_DIG": HEX_DIGIT,
        "UND": HEX_UND,
    },
    HEX_UND: {
        "ZERO": HEX_DIGIT,
        "OCT_DIG": HEX_DIGIT,
        "DEC_ONLY_DIG": HEX_DIGIT,
        "HEX_DIG": HEX_DIGIT,
    },

    # Float
    FLOAT_POINT_AFTER_DEC: {
        "ZERO": FLOAT_FRAC,
        "OCT_DIG": FLOAT_FRAC,
        "DEC_ONLY_DIG": FLOAT_FRAC,
        "UND": FLOAT_FRAC_UND,
    },
    FLOAT_POINT_ONLY: {
        "ZERO": FLOAT_FRAC,
        "OCT_DIG": FLOAT_FRAC,
        "DEC_ONLY_DIG": FLOAT_FRAC,
    },
    FLOAT_FRAC: {
        "ZERO": FLOAT_FRAC,
        "OCT_DIG": FLOAT_FRAC,
        "DEC_ONLY_DIG": FLOAT_FRAC,
        "UND": FLOAT_FRAC_UND,
    },
    FLOAT_FRAC_UND: {
        "ZERO": FLOAT_FRAC,
        "OCT_DIG": FLOAT_FRAC,
        "DEC_ONLY_DIG": FLOAT_FRAC,
    },
    DEAD: {}
}

def step(state, char):
    c = classify(char)
    return TRANSITIONS.get(state, {}).get(c, DEAD)

def literal_test(s):
    if not s:
        return False

    state = START
    for char in s:
        state = step(state, char)
        if state == DEAD:
            break
    return state in ACCEPTING_STATES

def run_batch(input_file="in_ans.txt", output_file="out.txt"):
    if not os.path.exists(input_file):
        return False

    tests = []

    with open(input_file, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) < 2:
                continue
            lit = p[0]
            exp = p[1].upper()
            if exp not in ("ACCEPT", "REJECT", "ACCEPTED", "REJECTED"):
                continue
            exp = "ACCEPT" if exp.startswith("ACCEPT") else "REJECT"
            tests.append((lit, exp))

    results = []
    for lit, exp in tests:
        actual = "ACCEPT" if literal_test(lit) else "REJECT"
        result = "PASS" if actual == exp else "FAIL"
        results.append((lit, exp, actual, result))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("literal\texpected\tactual\tresult\n")
        for r in results:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n")
    print(f"Results saved to: {output_file}")

    return True

def interactive():
    print("Python Number Literal Recognizer")
    print("Supports: decimal, octal, hexadecimal integers and floating point numbers")
    print("Enter 'quit' to exit\n")

    while True:
        s = input("Enter a Python number literal: ").strip()
        if s.lower() == 'quit':
            break
        if not s:
            continue

        if literal_test(s):
            print("Accept")
        else:
            print("Reject")
        print()


if __name__ == "__main__":
    if not run_batch():
        interactive()
