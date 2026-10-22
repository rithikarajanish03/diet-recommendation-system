import json
import streamlit as st

from Inference_engine import forward_chain
from A_star import a_star_search


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Diet Recommendation System",
    page_icon="🥗",
    layout="wide"
)


# =========================================
# LOAD DATABASES
# =========================================

@st.cache_data
def load_food_data():
    with open("Data/Food_data.json", "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_rules():
    with open("Data/Rules.json", "r", encoding="utf-8") as file:
        return json.load(file)


# =========================================
# BMI CALCULATION
# =========================================

def calculate_bmi(height, weight):
    height_m = height / 100
    return weight / (height_m ** 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    return "obesity"


# =========================================
# FILTER SUITABLE FOODS
# =========================================

def filter_food(food_data, meal, diet_type, allergens):

    suitable_foods = []

    for food in food_data:

        # Check selected meal
        if food["meal"] != meal:
            continue

        # Check dietary preference
        if diet_type == "vegan":
            if food["diet_type"] != "vegan":
                continue

        elif diet_type == "vegetarian":
            if food["diet_type"] == "non_vegetarian":
                continue

        # Exclude foods matching any selected allergen
        food_allergens = {
            allergen.lower()
            for allergen in food.get("allergens", [])
        }

        if any(
            allergen.lower() in food_allergens
            for allergen in allergens
        ):
            continue

        suitable_foods.append(food)

    return suitable_foods


# =========================================
# DISPLAY FOOD CARD
# =========================================

def display_food(food, rank):

    with st.container(border=True):

        st.subheader(f"{rank}. {food['name']}")

        st.caption(
            f"Serving size: {food['serving_size']}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Calories",
            f"{food['calories']} kcal"
        )

        col2.metric(
            "Protein",
            f"{food['protein']} g"
        )

        col3.metric(
            "Fiber",
            f"{food['fiber']} g"
        )

        col1, col2 = st.columns(2)

        col1.write(f"**Carbs:** {food['carbs']} g")
        col2.write(f"**Fat:** {food['fat']} g")

        food_allergens = food.get("allergens", [])

        if food_allergens:
            st.caption(
                "Listed allergens: "
                + ", ".join(food_allergens)
            )
        else:
            st.caption("Listed allergens: None")


# =========================================
# PAGE TITLE
# =========================================

st.title("🥗 Diet Recommendation System")

st.write(
    "Find food options based on your meal preference, "
    "dietary requirements, and nutritional goals."
)

st.info(
    "This tool provides general food suggestions, "
    "not medical or personalized dietary advice."
)


# =========================================
# USER INPUT FORM
# =========================================

with st.form("user_details_form"):

    st.header("👤 Your Details")

    name = st.text_input("Name")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=20
        )

    with col2:
        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=170.0
        )

    with col3:
        weight = st.number_input(
            "Weight (kg)",
            min_value=10.0,
            max_value=300.0,
            value=60.0
        )

    st.header("🏃 Activity Level")

    activity = st.selectbox(
        "Select your activity level",
        ["Sedentary", "Moderate", "High"]
    )

    st.header("🎯 Your Goal")

    goal = st.selectbox(
        "What is your goal?",
        ["Weight Loss", "Weight Gain", "Maintenance"]
    )

    st.header("🥗 Diet Type")

    diet_type = st.selectbox(
        "Select your diet type",
        ["Vegetarian", "Vegan", "Non-vegetarian"]
    )

    st.header("⚠️ Allergies / Food Restrictions")

    allergens = st.multiselect(
        "Select all that apply",
        [
            "Dairy",
            "Gluten",
            "Seafood",
            "Peanut",
            "Sesame",
            "Egg",
            "Soy",
            "Nuts"
        ]
    )

    st.header("🍽️ Meal Preference")

    meal = st.selectbox(
        "Which meal would you like recommendations for?",
        ["Breakfast", "Lunch", "Dinner", "Snack"]
    )

    submitted = st.form_submit_button(
        "🔍 Get Recommendations",
        use_container_width=True
    )


# =========================================
# PROCESS INPUT AND GENERATE RESULTS
# =========================================

if submitted:

    if not name.strip():
        st.error("Please enter your name.")

    else:

        try:
            food_data = load_food_data()
            rules = load_rules()

        except (OSError, json.JSONDecodeError) as error:
            st.error(
                "Could not load the food database or rule base. "
                "Check that both JSON files exist and contain valid JSON."
            )
            st.stop()

        # Convert selections to the values used by the backend
        goal_map = {
            "Weight Loss": "weight_loss",
            "Weight Gain": "weight_gain",
            "Maintenance": "maintenance"
        }

        diet_map = {
            "Vegetarian": "vegetarian",
            "Vegan": "vegan",
            "Non-vegetarian": "non_vegetarian"
        }

        activity_map = {
            "Sedentary": "sedentary",
            "Moderate": "moderate",
            "High": "high"
        }

        meal_value = meal.lower()
        goal_value = goal_map[goal]
        diet_value = diet_map[diet_type]
        activity_value = activity_map[activity]
        allergen_values = [item.lower() for item in allergens]

        # Calculate BMI
        bmi = calculate_bmi(height, weight)
        bmi_category = get_bmi_category(bmi)

        st.divider()
        st.header(f"Hello, {name.strip()}! 👋")

        st.subheader("Your BMI")

        col1, col2 = st.columns(2)

        col1.metric("BMI", f"{bmi:.1f}")
        col2.metric("BMI Category", bmi_category.title())

        # Create initial facts for Forward Chaining
        user_facts = {
            "goal": goal_value,
            "diet": diet_value,
            "activity": activity_value,
            "bmi_category": bmi_category
        }

        # Run the inference engine
        try:
            derived_facts, fired_rules = forward_chain(
                rules,
                user_facts
            )

        except (KeyError, TypeError, AttributeError) as error:
            st.error(
                "The inference engine encountered a problem. "
                "Please check Inference_engine.py and Rules.json."
            )
            st.stop()

        # Show safety warning if a rule derives one
        warning = derived_facts.get("warning")

        if warning:
            st.warning(warning)

            st.info(
                "Food options will still be shown, "
                "filtered by your selected meal, diet, and restrictions."
            )

        # Filter foods
        suitable_foods = filter_food(
            food_data,
            meal_value,
            diet_value,
            allergen_values
        )

        st.divider()
        st.header(f"🍽️ {meal} Recommendations")

        # Run A* search
        try:
            ranked_foods = a_star_search(
                suitable_foods,
                goal_value
            )

        except (KeyError, TypeError, ZeroDivisionError) as error:
            st.error(
                "The food ranking algorithm encountered a problem. "
                "Please check A_star.py and the food data."
            )
            st.stop()

        if not ranked_foods:

            st.warning(
                "No matching foods were found. "
                "Try changing your meal or dietary restrictions."
            )

        else:

            st.success(
                f"Found {len(ranked_foods)} suitable food option(s)."
            )

            st.caption(
                "Foods are ranked using the current nutritional "
                "scoring implementation."
            )

            for rank, food in enumerate(ranked_foods, start=1):
                display_food(food, rank)