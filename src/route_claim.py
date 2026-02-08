def determine_route(fields, missing_fields):

    # Rule 1: Missing fields → Manual Review
    if len(missing_fields) > 0:

        return {
            "recommendedRoute": "Manual Review",
            "reasoning": "Mandatory fields missing: " + ", ".join(missing_fields)
        }

    # Rule 2: Fraud keywords
    description = fields.get("description", "").lower()

    fraud_keywords = ["fraud", "staged", "inconsistent"]

    for keyword in fraud_keywords:

        if keyword in description:

            return {
                "recommendedRoute": "Investigation",
                "reasoning": f"Fraud keyword detected: {keyword}"
            }

    # Rule 3: Injury claims
    if fields.get("claimType") == "injury":

        return {
            "recommendedRoute": "Specialist Queue",
            "reasoning": "Injury claim requires specialist"
        }

    # Rule 4: Fast-track
    damage = fields.get("estimatedDamage")

    if damage:

        try:

            damage_amount = int(damage.replace(",", ""))

            if damage_amount < 25000:

                return {
                    "recommendedRoute": "Fast-track",
                    "reasoning": "Damage below fast-track threshold"
                }

        except:
            pass

    return {
        "recommendedRoute": "Manual Review",
        "reasoning": "Default routing applied"
    }
