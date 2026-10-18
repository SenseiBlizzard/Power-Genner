import random
import streamlit as st
from gen import generate_powers, generate_power_levels
from lib import CLASSES, TRAITS, CLASS_WEIGHTS, TRAIT_WEIGHTS

# ===========================
# Streamlit Configuration
# ===========================
st.set_page_config(page_title="Power Generator", layout="centered")
st.title("\U0001F300 Power Generator")

st.markdown("Welcome to the Power Generator! Click the button below to generate random power details.")

# ===========================
# Weight Debug Display
# ===========================
def display_weight_debug(generated_powers):
    """Show the weights that gen.py actually uses, after all generated powers."""
    st.subheader("⚖️ Weight Debug")
    st.caption(
        "These are relative weights loaded from lib.py and used by gen.py, "
        "not fixed percentages. A missing weight defaults to 100."
    )

    class_names = list(CLASSES)
    class_weights = {name: CLASS_WEIGHTS.get(name, 100) for name in class_names}
    class_weight_total = sum(class_weights.values())

    # Display every available class and the probability of choosing it.
    st.write("#### Class Weights")
    class_rows = [
        {
            "Class": name,
            "Weight": weight,
            "Chance (%)": round(100 * weight / class_weight_total, 2) if class_weight_total > 0 else 0,
        }
        for name, weight in class_weights.items()
    ]
    st.dataframe(class_rows, hide_index=True, use_container_width=True, height=475)

    # Display EVERY trait, with the exact same name-matching and fallback
    # logic as generate_character() in gen.py.
    st.write("#### Trait Weights")
    st.caption("Trait chances are calculated within their own class, after that class is selected.")
    trait_rows = []
    missing_weights = []
    for class_name in class_names:
        descriptions = TRAITS[class_name]
        defined_weights = TRAIT_WEIGHTS.get(class_name, {})
        names = [trait.split(":", 1)[0] for trait in descriptions]
        weights = [defined_weights.get(name, 100) for name in names]
        total = sum(weights)

        for trait_name, weight in zip(names, weights):
            if trait_name not in defined_weights:
                missing_weights.append(f"{class_name} → {trait_name}")
            trait_rows.append({
                "Class": class_name,
                "Trait": trait_name,
                "Weight": weight,
                "Chance within class (%)": round(100 * weight / total, 2) if total > 0 else 0,
            })

    st.dataframe(trait_rows, hide_index=True, use_container_width=True, height=425)

    # Make it easy to verify the actual weights of THIS generation's results.
    st.write("#### Weights Used for This Roll")
    generated_rows = []
    for power in generated_powers:
        class_name = power["class_name"]
        trait_name = power["trait_description"].split(":", 1)[0]
        generated_rows.append({
            "Class": class_name,
            "Class Weight": class_weights[class_name],
            "Trait": trait_name,
            "Trait Weight": TRAIT_WEIGHTS.get(class_name, {}).get(trait_name, 100),
        })
    st.dataframe(generated_rows, hide_index=True, use_container_width=True)

    # Validation: fallback is intentional, but flag it if an explicit entry is absent.
    missing_classes = [name for name in class_names if name not in CLASS_WEIGHTS]
    unused_classes = [name for name in CLASS_WEIGHTS if name not in CLASSES]
    unused_traits = [
        f"{class_name} → {trait_name}"
        for class_name, defined_weights in TRAIT_WEIGHTS.items()
        for trait_name in defined_weights
        if class_name not in TRAITS or trait_name not in {
            trait.split(":", 1)[0] for trait in TRAITS[class_name]
        }
    ]
    if missing_classes or missing_weights or unused_classes or unused_traits:
        st.warning("Some weight entries are missing or don't match the available classes/traits.")
        if missing_classes:
            st.write("Classes using default weight 100:", ", ".join(missing_classes))
        if missing_weights:
            st.write("Traits using default weight 100:", ", ".join(missing_weights))
        if unused_classes:
            st.write("Unused class weights:", ", ".join(unused_classes))
        if unused_traits:
            st.write("Unused trait weights:", ", ".join(unused_traits))
    else:
        st.success("All classes and traits have matching, explicitly configured weights.")


# ===========================
# Main Function for Streamlit
# ===========================
def main():
    """Roll abundance, generate powers, and display results and debugging."""
    if st.button("Generate Powers ⚡"):
        # Step 1: Roll for abundance
        abundance_roll = random.randint(1, 9)
        st.subheader(f"\U0001F3B2 Abundance Roll: {abundance_roll}")

        # Step 2: Generate initial power levels array based on abundance
        base_levels = generate_power_levels(abundance_roll)

        # Step 3: Generate powers based on the final abundance roll and power levels
        result = generate_powers(abundance_roll, base_levels)

        # Debugging: Ensure all keys exist in generated powers
        for power in result["powers"]:
            if "total_points" not in power:
                st.error(f"Error: Missing 'total_points' key in power: {power}")
                return

        # ===========================
        # Display Generated Powers
        # ===========================
        for idx, power in enumerate(result["powers"], start=1):
            theme = power.get("theme", "Unknown").upper()
            level = power.get("level", "N/A")
            points = min(power.get("total_points", 0), 50)
            cap = power.get("cap", "N/A")
            class_name = power.get("class_name", "Unknown")
            class_description = power.get("class_description", "No description available.")
            trait_description = power.get("trait_description", "No trait description.")

            st.write("# Distribute your points!")
            st.write("You have your THEME in caps, which is what the power will be based around, its (level) in brackets, and the points you have for distribution.")
            st.write(f"### {theme} ({level}) - {points} points")

            st.write("#### Stats")
            for stat in ["attack", "defense", "mobility", "range", "control", "endurance"]:
                base_stat = f"0/{cap}"
                st.write(f"- **{stat.capitalize()}:** {base_stat}")

            st.write("#### CLASSES")
            st.write(f"**{class_name}:** {class_description}")
            st.write("#### TRAITS")
            st.write(f"{trait_description}")
            st.write("-----")

        # ===========================
        # Display Weight Debug UNDER all generated powers
        # ===========================
        display_weight_debug(result["powers"])


# ===========================
# Run the Streamlit App
# ===========================
# To run: streamlit run main.py
if __name__ == "__main__":
    main()
