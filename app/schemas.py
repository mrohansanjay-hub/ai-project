from pydantic import BaseModel

class SoilInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    moisture: float
    ec: float
    temperature: float
