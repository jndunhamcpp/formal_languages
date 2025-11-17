
import os

START = "START"

# Decimal
DEC_ZERO = "DEC_ZERO"
DEC_NONZERO = "DEC_NONZERO"
DEC_UND_AFTER_ZERO = "DEC_UND_AFTER_ZERO"
DEC_UND_AFTER_NONZERO = "DEC_UND_AFTER_NONZERO"

# Oct
OCT_PREFIX_O = "OCT_PREFIX_O"
OCT_DIGIT = "OCT_DIGIT"
OCT_UND = "OCT_UND"

# Hex
HEX_PREFIX_X = "HEX_PREFIX_X"
HEX_DIGIT = "HEX_DIGIT"
HEX_UND = "HEX_UND"

DEAD = "DEAD"

ACCEPTING_STATES = {
    DEC_ZERO,
    DEC_NONZERO,
    OCT_DIGIT,
    HEX_DIGIT,
}

# Character classifier
def classify(c):
    if c == "0":
        return "ZERO"
    if "1" <= c <= "7":
        return "OCT"
    if "8" <= c <= "9":
        return "DEC"
    if "a" <= c.lower() <= "f":
        return "HEX"
    if c == "_":
        return "UND"
    if c.lower() == "o":
        return "O"
    if c.lower() == "x":
        return "X"
    return "OTHER"

TRANSITIONS = {
    START: {
        "ZERO": DEC_ZERO,
        "OCT": DEC_NONZERO,
        "DEC": DEC_NONZERO,
    },

    # Dec
    DEC_ZERO: {
        "O": OCT_PREFIX_O,
        "X": HEX_PREFIX_X,
    },
    DEC_NONZERO: {
        "ZERO": DEC_NONZERO,
        "OCT": DEC_NONZERO,
        "DEC": DEC_NONZERO,
        "UND": DEC_UND_AFTER_NONZERO,
    },

    DEC_UND_AFTER_NONZERO: {
        "ZERO": DEC_NONZERO,
        "OCT": DEC_NONZERO,
        "DEC": DEC_NONZERO,
    },

    # Oct
    OCT_PREFIX_O: {
        "ZERO": OCT_DIGIT,
        "OCT": OCT_DIGIT,
    },

    OCT_DIGIT: {
        "ZERO": OCT_DIGIT,
        "OCT": OCT_DIGIT,
        "UND": OCT_UND,
    },

    OCT_UND: {
        "ZERO": OCT_DIGIT,
        "OCT": OCT_DIGIT,
    },

    # Hex
    HEX_PREFIX_X: {
        "ZERO": HEX_DIGIT,
        "OCT": HEX_DIGIT,
        "DEC": HEX_DIGIT,
        "HEX": HEX_DIGIT,
    },

    HEX_DIGIT: {
        "ZERO": HEX_DIGIT,
        "OCT": HEX_DIGIT,
        "DEC": HEX_DIGIT,
        "HEX": HEX_DIGIT,
        "UND": HEX_UND,
    },

    HEX_UND: {
        "ZERO": HEX_DIGIT,
        "OCT": HEX_DIGIT,
        "DEC": HEX_DIGIT,
        "HEX": HEX_DIGIT,
    },

    DEAD: {}
}

def step(state, c):
    return TRANSITIONS.get(state, {}).get(classify(c), DEAD)

def literal_test(s):
    state = START
    for c in s:
        state = step(state, c)
        if state == DEAD:
            return False
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

    print(f"Output saved to: {output_file}")
    return True

def interactive():
    while True:
        s = input("Enter a Python literal: ").strip()
        print("ACCEPT" if literal_test(s) else "REJECT")

if __name__ == "__main__":
    if not run_batch():
        interactive()
