def classify_soil_health(data):
    """
    Returns:
    soil_class (int): 0=Poor, 1=Moderate, 2=Good
    soil_label (str)
    issues (list)
    """

    score = 0
    issues = []

    # -------- Nutrients --------
    if data.nitrogen >= 120:
        score += 1
    else:
        issues.append("Low nitrogen")

    if data.phosphorus >= 25:
        score += 1
    else:
        issues.append("Low phosphorus")

    if data.potassium >= 150:
        score += 1
    else:
        issues.append("Low potassium")

    # -------- Soil Properties --------
    if 5.5 <= data.ph <= 7.5:
        score += 1
    else:
        issues.append("pH imbalance")

    if 30 <= data.moisture <= 70:
        score += 1
    else:
        issues.append("Improper moisture")

    if data.ec <= 2.0:
        score += 1
    else:
        issues.append("High salinity")

    # -------- Final Classification --------
    if score <= 2:
        return 0, "Poor", issues
    elif score <= 4:
        return 1, "Moderate", issues
    else:
        return 2, "Good", issues
