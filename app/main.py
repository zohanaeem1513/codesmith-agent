from fastapi import FastAPI
from app.api.routes.system import router as system_router
app = FastAPI(title= "SmithCode Agent",
              version="0.1.0")
app.include_router(system_router,
                   prefix="/api/v1")