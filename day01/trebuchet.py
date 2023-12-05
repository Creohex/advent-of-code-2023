import re
from string import digits


with open("./input", "r") as f:
    lines = [l.strip() for l in f.readlines()]

digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
complex_pattern = r"(?=(\d{1}|" + "|".join(digit_map.keys()) + "))"


def fetch_calibration(s):
    x, y = 0, len(s) - 1
    while s[x] not in digits:
        x += 1
    while s[y] not in digits:
        y -= 1
    return int(s[x] + s[y])


def fetch_calibration_complex(s):
    tokens = re.findall(complex_pattern, s)
    return int(
        "".join(
            (tokens[idx] if tokens[idx] in digits else digit_map[tokens[idx]])
            for idx in (0, -1)
        )
    )


# part 1:
print(sum(map(fetch_calibration, lines)))

# part 2:
print(sum(map(fetch_calibration_complex, lines)))
