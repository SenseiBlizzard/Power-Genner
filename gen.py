import random
from lib import CLASSES, TRAITS, WORDS

# ===========================
# Character Generation
# ===========================

def generate_character():
    """
    Randomly selects and returns a theme (word), main class, and subclass.
    - Word: Represents a theme for the character.
    - Class: Main category (e.g., Warrior, Mage).
    - Subclass: Specialization within the main class.
    """
    word = random.choice(WORDS)
    char_class = random.choice(list(CLASSES.keys()))
    subclass = random.choice(TRAITS[char_class])
    return word, char_class, subclass

# ===========================
# Variance and Abundance Rolls
# ===========================

def roll_with_variance(base):
    """
    Rolls a number between base and base + 0.9 to add a small variance.
    Used to make power levels less predictable.
    """
    return round(random.uniform(base, base + 0.9), 1)

def roll_abundance():
    """
    Rolls a random abundance level between 1 and 9.
    Higher abundance means more potential power levels.
    """
    return random.randint(1, 9)

# ===========================
# Power Level Generation
# ===========================

def generate_power_levels(abundance):
    """
    Generates power levels based on the given abundance.
    - Abundance 9: Starts with a roll between 5–10, then rolls 1–4 if needed.
    - Other Abundances: Rolls 1–4 until total ≥ abundance.
    - Applies variance (0.0–0.9) to each roll for more dynamic levels.
    """
    base_levels = []  # Stores the raw rolls before applying variance
    total = 0         # Tracks the sum of all rolls

    if abundance == 9:
        # Special handling for abundance 9
        first_roll = random.randint(5, 10)
        first_roll_with_variance = round(first_roll + random.uniform(0.0, 0.9), 1)  # Apply variance to the first roll
        base_levels.append(first_roll_with_variance)
        total += first_roll_with_variance

        # If the first roll is less than 9, continue rolling 1-4 until total is ≥ 9
        if total < 9:
            while total < 9:
                roll = random.randint(1, 4)
                roll_with_variance = round(roll + random.uniform(0.0, 0.9), 1)  # Apply variance to each roll
                base_levels.append(roll_with_variance)
                total += roll_with_variance

                if total >= abundance:
                   break

    else:
        # For other abundances, roll 1–4 until total ≥ abundance
        while total < abundance:
            roll = random.randint(1, 4)
            roll_with_variance = round(roll + random.uniform(0.0, 0.9), 1)  # Apply variance to each roll
            base_levels.append(roll_with_variance)
            total += roll_with_variance

            # Stop adding more rolls if we've reached or exceeded the abundance value
            if total >= abundance:
                break

    # Recalculate total after variance is applied
    adjusted_total = sum(base_levels)

    # Print final adjusted values and total
    print(f"Generated Power Levels for Abundance {abundance}: {base_levels}")
    print(f"Total after Variance: {adjusted_total}")

    # If the adjusted total is greater than or equal to the abundance, return the adjusted levels
    if adjusted_total >= abundance:
        return base_levels
    else:
        print(f"Warning: Adjusted total ({adjusted_total}) is still less than the target abundance ({abundance})")
        return base_levels  # Or handle the case differently, e.g., retry or adjust further


# ===========================
# Stat Cap and Points Calculation
# ===========================

def get_stat_cap_and_points(level):
    """
    Returns the stat cap and base points available for a given whole level.
    Caps limit individual stat maximums.
    Points are used to distribute among stats.
    """
    return {
        1: (3, 5), 2: (4, 10), 3: (5, 15), 4: (6, 20),
        5: (7, 25), 6: (8, 30), 7: (9, 35), 8: (10, 40),
        9: (11, 45), 10: (12, 50)
    }.get(level, (3, 5))

def calculate_extra_stat_points(decimal_level):
    """
    Given a decimal power level, calculate extra stat points based on the 0.2 scaling system.
    - Every 0.2 increase in power level = 1 additional stat point.
    """
    base_level = int(decimal_level)  # Extract integer part
    decimal_part = decimal_level - base_level  # Extract decimal part
    extra_points = int((decimal_part // 0.2) * 1)  # Every 0.2 grants 1 extra point
    return extra_points

# ===========================
# Power Details Generation
# ===========================

def generate_powers(abundance, base_levels):
    """
    Generates detailed power information based on abundance and power levels.
    - Includes theme, class, subclass, and stat caps/points.
    - Applies extra stat points based on the decimal system.
    """
    power_details = []
    for level in base_levels:
        word, char_class, subclass = generate_character()
        class_desc = CLASSES[char_class]
        
        whole_level = int(level)  # Extract integer level
        cap, base_points = get_stat_cap_and_points(whole_level)
        
        # Calculate extra points based on decimal value
        extra_points = calculate_extra_stat_points(level)
        total_points = base_points + extra_points  # Total stat points available

        power_details.append({
            "level": level,  # Decimal level
            "whole_level": whole_level,  # Whole number level
            "theme": word,
            "class_name": char_class,
            "class_description": class_desc,
            "trait_description": subclass,
            "cap": cap,
            "base_points": base_points,  # Base stat points before decimal scaling
            "extra_points": extra_points,  # Bonus stat points from decimal scaling
            "total_points": total_points  # Final total stat points
        })

    return {
        "roll": abundance,
        "powers": power_details
    }
