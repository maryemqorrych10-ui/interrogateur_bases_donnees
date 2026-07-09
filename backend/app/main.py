from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.config import settings
from app.routers import connections, queries
from app.schemas import HealthResponse

# Create tables on startup
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️ Error creating tables: {e}")

# Initialize app
app = FastAPI(
    title="Database Interrogator API",
    description="API for querying and managing multiple databases",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(connections.router)
app.include_router(queries.router)


@app.get("/", response_model=HealthResponse)
def root():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        message="Database Interrogator API is running"
    )


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is healthy and ready to serve requests"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
