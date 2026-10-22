# =========================================
# A* SEARCH
# Nutritional Recommendation
# =========================================


# =========================================
# TARGET VALUES
# =========================================

def get_targets(goal):
    """
    Returns the target nutritional values
    for one meal based on the user's goal.

    These are project assumptions used
    for the A* prototype.
    """

    if goal == "weight_loss":

        return {
            "calories": 350,
            "protein": 20,
            "fiber": 8
        }

    elif goal == "weight_gain":

        return {
            "calories": 600,
            "protein": 25,
            "fiber": 6
        }

    else:

        # Maintenance

        return {
            "calories": 450,
            "protein": 20,
            "fiber": 7
        }


# =========================================
# HEURISTIC FUNCTION
# =========================================

def heuristic(food, goal):
    """
    Calculates the estimated cost h(n).

    The heuristic measures how far a food is
    from the nutritional target for the user's goal.

    Lower value = nutritionally closer.
    """

    targets = get_targets(goal)


    # -----------------------------------------
    # CALORIE DIFFERENCE
    # -----------------------------------------

    calorie_difference = abs(
        food["calories"] - targets["calories"]
    )

    calorie_score = calorie_difference / targets["calories"]


    # -----------------------------------------
    # PROTEIN DIFFERENCE
    # -----------------------------------------

    protein_difference = abs(
        food["protein"] - targets["protein"]
    )

    protein_score = (
        protein_difference / targets["protein"]
    )


    # -----------------------------------------
    # FIBER DIFFERENCE
    # -----------------------------------------

    fiber_difference = abs(
        food["fiber"] - targets["fiber"]
    )

    fiber_score = (
        fiber_difference / targets["fiber"]
    )


    # -----------------------------------------
    # WEIGHTED HEURISTIC
    # -----------------------------------------

    h = (
        0.50 * calorie_score
        + 0.30 * protein_score
        + 0.20 * fiber_score
    )


    return h


# =========================================
# PATH COST
# =========================================

def food_cost(food, goal):
    """
    Calculates g(n), the actual cost of
    selecting a food.

    Foods that are more suitable for the
    user's goal receive a lower cost.
    """

    targets = get_targets(goal)


    calorie_difference = abs(
        food["calories"] - targets["calories"]
    )

    protein_difference = abs(
        food["protein"] - targets["protein"]
    )

    fiber_difference = abs(
        food["fiber"] - targets["fiber"]
    )


    g = (
        0.50 * calorie_difference / targets["calories"]
        + 0.30 * protein_difference / targets["protein"]
        + 0.20 * fiber_difference / targets["fiber"]
    )


    return g


# =========================================
# A* SEARCH
# =========================================

def a_star_search(food_list, goal):
    """
    Performs A* search on suitable foods.

    f(n) = g(n) + h(n)

    Returns foods ordered according to
    their A* score.
    """

    if len(food_list) == 0:

        return []


    open_list = []


    # -----------------------------------------
    # CREATE A* NODES
    # -----------------------------------------

    for food in food_list:

        g_cost = food_cost(
            food,
            goal
        )

        h_cost = heuristic(
            food,
            goal
        )

        f_cost = g_cost + h_cost


        open_list.append({

            "food": food,

            "g": g_cost,

            "h": h_cost,

            "f": f_cost

        })


    # -----------------------------------------
    # LOWEST f(n) FIRST
    # -----------------------------------------

    open_list.sort(
        key=lambda node: node["f"]
    )


    # -----------------------------------------
    # RETURN FOOD ORDER
    # -----------------------------------------

    ordered_foods = []


    for node in open_list:

        ordered_foods.append(
            node["food"]
        )


    return ordered_foods