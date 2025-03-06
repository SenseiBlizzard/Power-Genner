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

def roll_with_variance(base):
    variance_options = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    return round(base + random.choice(variance_options), 1)

def roll_abundance():
    return random.randint(1, 9)

# ===========================
# Power Level Generation
# ===========================

def generate_power_levels(abundance):
    base_levels = []
    total = 0

    if abundance == 9:
        first_roll = random.randint(5, 10)
        first_roll_with_variance = roll_with_variance(first_roll)
        base_levels.append(first_roll_with_variance)
        total += first_roll_with_variance

        while total < 9:
            roll = random.randint(1, 4)
            roll_with_variance_value = roll_with_variance(roll)
            base_levels.append(roll_with_variance_value)
            total += roll_with_variance_value
            if total >= abundance:
                break
    else:
        while total < abundance:
            roll = random.randint(1, 4)
            roll_with_variance_value = roll_with_variance(roll)
            base_levels.append(roll_with_variance_value)
            total += roll_with_variance_value
            if total >= abundance:
                break

    adjusted_total = sum(base_levels)
    print(f"Generated Power Levels for Abundance {abundance}: {base_levels}")
    print(f"Total after Variance: {adjusted_total}")
    
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
    decimal_part = decimal_level - int(decimal_level)
    if 0.0 <= decimal_part <= 0.1:
        return 0
    elif 0.2 <= decimal_part <= 0.3:
        return 1
    elif 0.4 <= decimal_part <= 0.5:
        return 2
    elif 0.6 <= decimal_part <= 0.7:
        return 3
    elif 0.8 <= decimal_part <= 0.9:
        return 4
    return 0

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
        total_points = min(base_points + extra_points, 50)  # Ensure max 50 points
        
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
