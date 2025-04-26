from fastapi import FastAPI
from api.routes import router
from database.database import init_db  # Adjust based on your database module location
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This will run at startup
    init_db()
    yield
    # This will run at shutdown (if you need clean up, add it here)

app = FastAPI(
    title="WOT French Clan API",
    description="API for managing and updating World of Tanks French Clans",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/",      # Swagger at root
    redoc_url=None     # Disable ReDoc
)

# Include the API router for handling endpoints.
app.include_router(router)

if __name__ == "__main__":
    # Run the API with uvicorn.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
