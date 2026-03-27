from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Literal

class UserPreferences(BaseModel):
    destination: Optional[str] = Field(None, description="The desired destination (can be empty for recommendations)")
    duration: int = Field(..., description="Number of days for the trip")
    budget: Literal["budget", "moderate", "luxury"] = Field(..., description="Budget level")
    style: Literal["culture", "nature", "relaxation", "food", "adventure"] = Field(..., description="Travel style")

class Activity(BaseModel):
    timeOfDay: str = Field(description="Morning, Afternoon, or Evening")
    title: str = Field(description="Title of the activity")
    description: str = Field(description="Description of what to do")
    costEstimate: int = Field(description="Estimated cost in USD")

class DailyPlan(BaseModel):
    dayNumber: int
    theme: str = Field(description="Overall theme or location for the day")
    activities: List[Activity]

class BudgetBreakdown(BaseModel):
    flightsTransit: int = Field(description="Estimated cost for flights and main transit")
    accommodation: int = Field(description="Estimated cost for hotels/lodging")
    foodDining: int = Field(description="Estimated food costs")
    activities: int = Field(description="Estimated activities/tours costs")
    total: int = Field(description="Total estimated cost")

    @model_validator(mode="after")
    def check_total(self) -> "BudgetBreakdown":
        expected_total = self.flightsTransit + self.accommodation + self.foodDining + self.activities
        if self.total != expected_total:
            raise ValueError(f"Total {self.total} does not match sum of components {expected_total}")
        return self

class ItineraryResponse(BaseModel):
    destination: str = Field(description="The chosen or recommended destination")
    summary: str = Field(description="A short exciting summary of the trip")
    days: List[DailyPlan]
    budget: BudgetBreakdown
