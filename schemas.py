"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Exercise(BaseModel):
    name: str = Field(..., description="Exercise name, e.g., Bench Press")
    sets: int = Field(..., ge=1, le=20, description="Number of sets")
    reps: int = Field(..., ge=1, le=100, description="Repetitions per set")
    weight: float = Field(0, ge=0, description="Weight per rep in kg or lbs")

class Workout(BaseModel):
    """
    Fitness workouts schema
    Collection name: "workout"
    """
    user_id: str = Field(..., description="Identifier for the user")
    workout_date: date = Field(..., description="Date of the workout")
    title: str = Field(..., description="Workout title, e.g., Push Day")
    notes: Optional[str] = Field(None, description="Optional notes")
    exercises: List[Exercise] = Field(default_factory=list, description="List of exercises performed")

class Profile(BaseModel):
    """
    User profile for fitness app
    Collection name: "profile"
    """
    user_id: str = Field(..., description="Identifier for the user")
    name: str = Field(..., description="Display name")
    goal: Optional[str] = Field(None, description="Primary fitness goal")
    height_cm: Optional[float] = Field(None, ge=0, description="Height in centimeters")
    weight_kg: Optional[float] = Field(None, ge=0, description="Current weight in kilograms")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
