import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date

from database import db, create_document, get_documents
from schemas import Workout, Profile

app = FastAPI(title="Fitness App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Fitness App Backend Running"}

# Public schema endpoint for viewer
@app.get("/schema")
def get_schema():
    return {
        "workout": Workout.model_json_schema(),
        "profile": Profile.model_json_schema(),
    }

# Simple endpoints to create and list workouts using DB helpers
class WorkoutCreate(BaseModel):
    user_id: str
    workout_date: date
    title: str
    notes: str | None = None
    exercises: List[dict] = []

@app.post("/api/workouts")
def create_workout(payload: WorkoutCreate):
    try:
        workout = Workout(**payload.model_dump())
        inserted_id = create_document("workout", workout)
        return {"id": inserted_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workouts")
def list_workouts(user_id: str):
    try:
        docs = get_documents("workout", {"user_id": user_id}, limit=50)
        # Convert ObjectId to str
        for d in docs:
            d["_id"] = str(d["_id"]) if "_id" in d else None
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
