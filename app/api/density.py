from fastapi import APIRouter
from app.schemas.density import DensityResponse
from app.services.density_service import compute_washroom_density

router = APIRouter(prefix="/density", tags=["density"])


@router.get("", response_model=list[DensityResponse])
def get_density():
    df = compute_washroom_density()
    return df.to_dict(orient="records")
