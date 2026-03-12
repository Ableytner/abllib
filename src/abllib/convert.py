"""A module containing formatting functions"""

from abllib.error import WrongTypeError

PREFIXES = {
    "-30": "q",
    "-27": "r",
    "-24": "y",
    "-21": "z",
    "-18": "a",
    "-15": "f",
    "-12": "p",
    "-9": "n",
    "-6": "μ",
    "-3": "m",
    "0": "",
    "3": "k",
    "6": "M",
    "9": "G",
    "12": "T",
    "15": "P",
    "18": "E",
    "21": "Z",
    "24": "Y",
    "27": "R",
    "30": "Q"
}

def as_bytes(value: int | float) -> str:
    """Format the given number of bytes to a human-readable format"""

    if not isinstance(value, (int, float)):
        raise WrongTypeError.with_values(value, (int, float))

    return f"{_append_si_prefix(value)}B"

def get_bytes(text: str) -> int:
    """Undo any formatting and return the number of bytes"""

    if not isinstance(text, str):
        raise WrongTypeError.with_values(text, str)

    if text.isdigit():
        return int(text)

    if text[-1].lower() == "b":
        text = text[:-1]
        if text.isdigit():
            return int(text)

    number = float(text[:-1])
    multiplier = text[-1].upper()

    match multiplier:
        case "T":
            number *= 1000**4
        case "G":
            number *= 1000**3
        case "M":
            number *= 1000**2
        case "K":
            number *= 1000**1
        case _:
            raise ValueError(f"Unknown SI prefix {multiplier} in {text}")

    return int(number)

def _append_si_prefix(value: int | float) -> str:
    bases_changed = 0

    while value < 1 or value >= 1000:
        if value < 1:
            bases_changed -= 3
            value *= 1000
        else:
            bases_changed += 3
            value /= 1000

    return f"{value:.1f}{PREFIXES[str(bases_changed)]}"
