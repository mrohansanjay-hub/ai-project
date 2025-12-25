from pydantic import BaseModel , field_validator

class SoilInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    moisture: float
    ec: float
    temperature: float
    latitude: float
    longitude: float
    crop: str
    state: str
    district: str
    season: str

    @field_validator("state", "district", "season", "crop")
    @classmethod
    def normalize(cls, v: str):
        return v.strip().lower()
