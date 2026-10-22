# =========================================
# INFERENCE ENGINE
# Forward Chaining
# =========================================


def rule_matches(rule_condition, facts):
    """
    Checks whether all conditions of a rule
    are satisfied by the current facts.
    """

    for key, value in rule_condition.items():

        # Check whether the fact exists
        if key not in facts:
            return False

        # Check whether the value matches
        if facts[key] != value:
            return False

    return True


def apply_rule(rule, facts):
    """
    Applies the conclusion of a rule
    and returns the newly derived facts.
    """

    new_facts = {}

    for key, value in rule["then"].items():

        # If the fact is new, add it
        if key not in facts:
            new_facts[key] = value

        # If the fact already exists,
        # handle multiple values separately
        elif isinstance(facts[key], list):

            if isinstance(value, list):

                for item in value:
                    if item not in facts[key]:
                        facts[key].append(item)

            else:

                if value not in facts[key]:
                    facts[key].append(value)

    return new_facts


def forward_chain(rules, initial_facts):

    """
    Performs forward chaining.

    Starts with initial facts and repeatedly
    applies rules until no new facts can be derived.
    """

    # Make a copy so the original user facts
    # are not changed
    facts = initial_facts.copy()

    fired_rules = []

    changed = True

    while changed:

        changed = False

        for rule in rules:

            # Check whether this rule can fire
            if rule_matches(rule["if"], facts):

                # Apply the rule
                new_facts = apply_rule(rule, facts)

                # Add newly derived facts
                for key, value in new_facts.items():

                    facts[key] = value
                    changed = True

                # Record the rule if it produced
                # something new
                if new_facts:
                    fired_rules.append(rule["id"])

    return facts, fired_rules