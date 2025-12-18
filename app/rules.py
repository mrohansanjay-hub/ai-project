def classify_soil_health(data):
    score = 0
    issues = []

    # --- Nitrogen ---
    if data.nitrogen >= 40:
        score += 1
    else:
        issues.append("Low nitrogen")

    # --- Phosphorus ---
    if data.phosphorus >= 25:
        score += 1
    else:
        issues.append("Low phosphorus")

    # --- Potassium ---
    if data.potassium >= 30:
        score += 1
    else:
        issues.append("Low potassium")

    # --- pH ---
    if 5.5 <= data.ph <= 7.5:
        score += 1
    else:
        issues.append("pH imbalance")

    # --- Moisture ---
    if 30 <= data.moisture <= 70:
        score += 1
    else:
        issues.append("Improper moisture")

    # --- EC (Salinity) ---
    if data.ec <= 2.0:
        score += 1
    else:
        issues.append("High salinity")

    # --- Temperature ---
    if 15 <= data.temperature <= 35:
        score += 1
    else:
        issues.append("Temperature stress")

    # --- Final Soil Health ---
    if score >= 6:
        health = "Healthy"
    elif score >= 4:
        health = "Moderate"
    else:
        health = "Poor"

    return health, issues


def apply_rules(data):
    actions = []
    warnings = []

    # ======================
    # Fertilizer Actions
    # ======================

    # --- Nitrogen ---
    if data.nitrogen < 40:
        actions.append(
            "Apply 20–25 kg urea per acre to improve nitrogen levels"
        )

    # --- Phosphorus ---
    if data.phosphorus < 25:
        actions.append(
            "Apply 40–50 kg DAP or SSP per acre for better root development"
        )

    # --- Potassium ---
    if data.potassium < 30:
        actions.append(
            "Apply 20–25 kg MOP (potash) per acre to strengthen crop resistance"
        )

    # ======================
    # pH Correction
    # ======================

    if data.ph < 5.5:
        actions.append(
            "Apply lime to increase soil pH"
        )
    elif data.ph > 7.8:
        actions.append(
            "Apply gypsum or sulfur to reduce soil pH"
        )

    # ======================
    # Warnings & Safety
    # ======================

    # --- Salinity ---
    if data.ec > 2.5:
        warnings.append(
            "High soil salinity detected – reduce fertilizer usage and improve drainage"
        )

    # --- Moisture ---
    if data.moisture > 70:
        warnings.append(
            "Avoid irrigation – soil is waterlogged"
        )
    elif data.moisture < 25:
        warnings.append(
            "Soil is dry – irrigation required before fertilizer application"
        )

    # --- Temperature ---
    if data.temperature > 40:
        warnings.append(
            "High temperature stress – avoid fertilizer application during midday"
        )
    elif data.temperature < 10:
        warnings.append(
            "Low temperature – fertilizer efficiency may be reduced"
        )

    return actions, warnings
