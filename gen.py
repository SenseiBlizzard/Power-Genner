import random
from lib import CLASSES, TRAITS, WORDS

# ===========================
# Character Generation
# ===========================

def generate_character():
    word = random.choice(WORDS)
    char_class = random.choice(list(CLASSES.keys()))
    subclass = random.choice(TRAITS[char_class])
    return word, char_class, subclass

# ===========================
# Variance and Abundance Rolls
# ===========================

def roll_abundance():
    return random.randint(1, 9)

# ===========================
# Power Level Generation
# ===========================

def generate_power_levels(abundance):
    base_levels = []  # Stores the rolls with variance
    total = 0         # Tracks the sum of all rolls

    if abundance == 9:
        first_roll = random.randint(5, 10) + random.uniform(0.0, 0.9)
        first_roll = round(first_roll, 1)
        base_levels.append(first_roll)
        total += int(first_roll)

        if total < 9:
            while total < 9:
                roll = random.randint(1, 4) + random.uniform(0.0, 0.9)
                roll = round(roll, 1)
                base_levels.append(roll)
                total += int(roll)
    else:
        while total < abundance:
            roll = random.randint(1, 4) + random.uniform(0.0, 0.9)
            roll = round(roll, 1)
            base_levels.append(roll)
            total += int(roll)

    print(f"Generated Power Levels for Abundance {abundance}: {base_levels}")
    return base_levels

# ===========================
# Stat Cap and Points Calculation
# ===========================

def get_stat_cap_and_points(level):
    return {
        1: (3, 5), 2: (4, 10), 3: (5, 15), 4: (6, 20),
        5: (7, 25), 6: (8, 30), 7: (9, 35), 8: (10, 40),
        9: (11, 45), 10: (12, 50)
    }.get(level, (3, 5))

def calculate_extra_stat_points(decimal_level):
    base_level = int(decimal_level)
    decimal_part = decimal_level - base_level
    extra_points = int(decimal_part // 0.2)
    return extra_points

# ===========================
# Power Details Generation
# ===========================

def generate_powers(abundance, base_levels):
    power_details = []
    for level in base_levels:
        word, char_class, subclass = generate_character()
        class_desc = CLASSES[char_class]

        whole_level = int(level)
        cap, base_points = get_stat_cap_and_points(whole_level)
        extra_points = calculate_extra_stat_points(level)
        total_points = base_points + extra_points

        power_details.append({
            "level": level,
            "whole_level": whole_level,
            "theme": word,
            "class_name": char_class,
            "class_description": class_desc,
            "trait_description": subclass,
            "cap": cap,
            "base_points": base_points,
            "extra_points": extra_points,
            "total_points": total_points
        })

    return {
        "roll": abundance,
        "powers": power_details
    }
