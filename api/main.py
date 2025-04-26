# api/main.py

from fastapi import FastAPI
from api.routes import router
from database.database import init_db  # Adjust based on your database module location
import uvicorn

app = FastAPI(
    title="WOT French Clan API",
    description="API for managing and updating World of Tanks French Clans",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    # Initialize the database when the app starts.
    init_db()

# Include the API router for handling endpoints.
app.include_router(router)

if __name__ == "__main__":
    # Run the API with uvicorn.
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
