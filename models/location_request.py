from pydantic import BaseModel, Field

class LocationRequest(BaseModel):
    location: str = Field(..., description="The location to get data for")