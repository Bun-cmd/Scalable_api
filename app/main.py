# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.routers import users, items # Assuming these are your router files

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",     # <--- ADD THIS LINE
    redoc_url="/redoc",   # <--- ADD THIS LINE
)

# Include your API routers
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(items.router, prefix=settings.API_V1_STR, tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Scalable FastAPI API!"}