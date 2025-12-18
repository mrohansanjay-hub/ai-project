def generate_reasoning(data, soil_health, issues, actions, warnings):

    analysis = (
        f"Soil health is classified as {soil_health}. "
        f"N={data.nitrogen}, P={data.phosphorus}, K={data.potassium}, "
        f"pH={data.ph}, Moisture={data.moisture}%, EC={data.ec}, "
        f"Temperature={data.temperature}°C."
    )

    if issues:
        analysis += " Issues detected: " + ", ".join(issues) + "."

    crops = []

    if soil_health == "Healthy":
        if data.moisture > 60:
            crops.append("Rice")
        crops.extend(["Maize", "Cotton", "Groundnut"])

    elif soil_health == "Moderate":
        crops.extend(["Maize", "Groundnut", "Millets"])

    else:
        crops.extend(["Millets", "Pulses"])

    return {
        "analysis": analysis,
        "actions": actions,
        "crop_suitability": list(set(crops)),
        "warnings": warnings if warnings else None
    }
