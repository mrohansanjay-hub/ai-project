from app.state_district_crop_map import STATE_DISTRICT_CROP_MAP

def get_location_crops(state: str, district: str, season: str):
    return (
        STATE_DISTRICT_CROP_MAP
        .get(state, {})
        .get(district, {})
        .get(season, [])
    )
