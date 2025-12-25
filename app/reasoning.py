from app.location_crop_helper import get_location_crops


def generate_reasoning(
    data,
    soil_health,
    issues,
    actions,
    warnings,
    weather: dict | None = None
):
    enhanced_issues = list(set(issues))
    enhanced_warnings = list(warnings)
    enhanced_actions = list(actions)

    # ----------------------
    # Derived Issues (Human-friendly)
    # ----------------------
    if data.moisture < 30:
        enhanced_issues.append("Low soil moisture")

    if data.temperature >= 35:
        enhanced_issues.append("High temperature stress")

    if 7.5 <= data.ph <= 8.0:
        enhanced_issues.append("Slightly alkaline soil")

    # ----------------------
    # Weather-Aware Enhancements
    # ----------------------
    if weather and weather.get("rain_probability") is not None:
        rain_prob = weather["rain_probability"]

        if rain_prob > 60:
            enhanced_warnings.append(
                "High rainfall probability – postpone fertilizer application"
            )
        elif rain_prob < 20:
            enhanced_warnings.append(
                "Low rainfall expected – irrigate before fertilizer application"
            )

        if weather.get("today_temp") and weather["today_temp"] >= 35:
            enhanced_warnings.append(
                "High temperature – apply fertilizer during early morning or evening"
            )

    # ----------------------
    # Default Actions for Healthy Soil
    # ----------------------
    if soil_health == "Good" and not enhanced_actions:
        enhanced_actions.extend([
            "Maintain current nutrient levels using balanced fertilization",
            "Monitor soil parameters periodically"
        ])

    # ----------------------
    # 🌍 STATE ➜ DISTRICT ➜ SEASON Crop Recommendation
    # ----------------------
    location_crops = get_location_crops(
        data.state,
        data.district,
        data.season
    )

    if data.crop:
        # If user provided crop, do NOT override it
        crops = [data.crop.title()]
    elif location_crops:
        if soil_health == "Good":
            crops = location_crops
        elif soil_health == "Moderate":
            crops = location_crops[: max(1, len(location_crops) // 2)]
        else:
            crops = ["Millets", "Pulses"]
    else:
        crops = ["Millets", "Pulses"]

    # ----------------------
    # Explanation Summary
    # ----------------------
    summary = (
        f"Soil health is {soil_health}. "
        f"N={data.nitrogen}, P={data.phosphorus}, K={data.potassium}, "
        f"pH={data.ph}, Moisture={data.moisture}%, "
        f"EC={data.ec}, Temperature={data.temperature}°C."
    )

    if weather and weather.get("today_short_forecast"):
        summary += (
            f" Weather forecast: {weather.get('today_short_forecast')}, "
            f"Rain probability: {weather.get('rain_probability', 0)}%."
        )

    return {
        "summary": summary,
        "issues": sorted(set(enhanced_issues)),
        "actions": enhanced_actions,
        "recommended_crops": crops,
        "warnings": sorted(set(enhanced_warnings)) if enhanced_warnings else []
    }
