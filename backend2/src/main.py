from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth import router as auth_router
from src.config import settings
from src.database import check_db_connection, create_tables
from src.routers.user import router as user_router
from src.routers.service import router as service_router
from src.routers.appointment import router as appointment_router
from src.routers.payment import router as payment_router

app = FastAPI(
    title="Beauty Salon API",
    description="API для салона красоты",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await create_tables()


main_router = APIRouter(prefix="/api")
main_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
main_router.include_router(user_router, tags=["Users"])
main_router.include_router(service_router, tags=["Services"])
main_router.include_router(appointment_router, tags=["Appointments"])
main_router.include_router(payment_router, tags=["Payments"])


app.include_router(main_router)


