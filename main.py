import random
import streamlit as st
from gen import generate_powers, generate_power_levels

# ===========================
# Streamlit Configuration
# ===========================
st.set_page_config(page_title="Power Generator", layout="centered")
st.title("🌀 Power Generator")

st.markdown("Welcome to the Power Generator! Click the button below to generate random power details.")

# ===========================
# Main Function for Streamlit
# ===========================
def main():
    """
    Main function to handle the entire process of:
    1. Rolling for abundance.
    2. Generating power levels based on abundance.
    3. Displaying the final power details.
    """
    if st.button("Generate Powers ⚡"):
        # Step 1: Roll for abundance
        abundance_roll = random.randint(1, 9)  # Directly rolls for abundance without reroll option
        st.subheader(f"🎲 Abundance Roll: {abundance_roll}")

        # Step 2: Generate initial power levels array based on abundance
        base_levels = generate_power_levels(abundance_roll)

        # Step 3: Generate powers based on the final abundance roll and power levels
        result = generate_powers(abundance_roll, base_levels)

        # Debugging: Ensure all keys exist in generated powers
        for power in result['powers']:
            if 'total_points' not in power:
                st.error(f"Error: Missing 'total_points' key in power: {power}")
                return  # Stop execution if points key is missing

        # ===========================
        # Display Generated Powers
        # ===========================
        for idx, power in enumerate(result['powers'], start=1):
            theme = power.get('theme', 'Unknown').upper()
            level = power.get('level', 'N/A')
            points = power.get('total_points', 0)  # Use 'total_points' instead
            cap = power.get('cap', 'N/A')
            class_name = power.get('class_name', 'Unknown')
            class_description = power.get('class_description', 'No description available.')
            trait_description = power.get('trait_description', 'No trait description.')

            # Extract trait stats if applicable
            trait_stats = {}
            if "Stats:" in trait_description:
                stats_part = trait_description.split("Stats:")[1].strip()
                for stat in stats_part.split(","):
                    parts = stat.strip().split()
                    stat_value = int(parts[0].replace("+", "").replace("-", "-"))
                    stat_name = parts[1].strip().lower()
                    trait_stats[stat_name] = stat_value

            # Display power details
            st.write("# Distribute your points!")
            st.write("You have your THEME in caps, which is what the power will be based around, its (level) in brackets, and the points you have for distribution.")
            st.write(f"### {theme} ({level}) - {points} points")
            
            # Print stats with +Trait if applicable
            st.write("#### Stats")
            for stat in ["attack", "defense", "mobility", "range", "control", "endurance"]:
                base_stat = f"0/{cap}"
                if stat in trait_stats and trait_stats[stat] != 0:
                    base_stat += " +Trait"
                st.write(f"- **{stat.capitalize()}:** {base_stat}")

            # Print class and trait details
            st.write("#### CLASSES")
            st.write(f"**{class_name}:** {class_description}")
            st.write("#### TRAITS")
            st.write(f"{trait_description}")

            # Separator between powers
            st.write("-----")

# ===========================
# Run the Streamlit App
# ===========================
if __name__ == "__main__":
    main()
