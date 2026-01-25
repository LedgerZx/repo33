import random

def generate_ascii_art():
    patterns = {
        'tree': [
            "    *    ",
            "   ***   ",
            "  *****  ",
            " ******* ",
            "*********",
            "    |    "
        ],
        'face': [
            "  .-.   ",
            " (o o)  ",
            " |  |  ",
            " '-'   "
        ],
        'house': [
            "  /\\    ",
            " /  \\   ",
            "/____\\  ",
            "|    |  ",
            "|____|  "
        ]
    }
    
    choice = random.choice(list(patterns.keys()))
    for line in patterns[choice]:
        print(line)

generate_ascii_art()
