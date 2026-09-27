def calculate_priority(camp):

    health = camp["Health Risk"]
    vulnerable = camp["Vulnerable"]

    # Convert hours without aid to a 0-100 score.
    time_without_aid = min(
        (camp["Time Without Aid"] / 24) * 100,
        100
    )

    isolation = camp["Isolation"]

    priority = (
        0.35 * health +
        0.25 * vulnerable +
        0.25 * time_without_aid +
        0.15 * isolation
    )

    return round(priority, 1)


def add_priority_scores(camps):

    camps = camps.copy()

    camps["Priority Score"] = camps.apply(
        calculate_priority,
        axis=1
    )

    camps["Priority Level"] = camps["Priority Score"].apply(
        get_priority_level
    )

    return camps


def get_priority_level(score):

    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"
