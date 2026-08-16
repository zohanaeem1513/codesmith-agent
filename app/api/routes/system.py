from fastapi import APIRouter
from app.schemas.system import RootResponse,HealthResponse
router = APIRouter()
@router.get("/", response_model=RootResponse)
async def root () -> RootResponse:
    return RootResponse(
        name="CodeSmith Agent",
        status="running",
    )

@router.get("/health",response_model=HealthResponse) 
async def health()-> HealthResponse:
    return HealthResponse(status="Ok",
                          service="CodeSmith Agent",
                         )     