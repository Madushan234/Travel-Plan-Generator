from pydantic import BaseModel, Field
from typing import List, Optional

class TravelPlanRequest(BaseModel):
    destination: str = Field(..., description="The destination for the travel plan")
    travelDays: int = Field(..., ge=1, description="Number of days for the travel")
    travelersCount: int = Field(..., ge=1, description="Number of travelers")
    budget: str = Field(..., description="Budget category: Low, Medium, High")
    travelPace: str = Field(..., description="Travel pace: Relaxed, Balanced, Fast-paced")
    culturalPreferences: str = Field(..., description="Cultural preferences: Yes or No")
    foodPreferences: Optional[str] = Field(None, description="Food preferences")
    travelExperience: str = Field(..., description="Travel experience level: Beginner, Intermediate, Expert")
    accommodation: str = Field(..., description="Accommodation preference")
    activities: str = Field(..., description="List of activities and interests")