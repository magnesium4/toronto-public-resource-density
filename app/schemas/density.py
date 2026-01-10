from pydantic import BaseModel


class DensityResponse(BaseModel):
    neighbourhood: str
    resource_count: int
    area_km2: float
    density: float
