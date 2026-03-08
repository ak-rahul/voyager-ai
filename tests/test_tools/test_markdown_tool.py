import pytest
import os
import shutil
from src.tools.markdown_tool import markdown_tool
from src.models.schemas import ItineraryResponse, BudgetBreakdown, DailyPlan, Activity

def test_markdown_generation():
    test_dir = "tests/test_outputs"
    
    # Setup mock itinerary
    itin = ItineraryResponse(
        destination="Rome",
        summary="A historic trip to Italy.",
        days=[
            DailyPlan(
                dayNumber=1,
                theme="Ancient Wonders",
                activities=[
                    Activity(timeOfDay="Morning", title="Colosseum", description="Tour the ruins", costEstimate=30),
                    Activity(timeOfDay="Afternoon", title="Roman Forum", description="Walk the forum", costEstimate=20)
                ]
            )
        ],
        budget=BudgetBreakdown(flightsTransit=500, accommodation=300, foodDining=200, activities=50, total=1050)
    )
    
    # Execute
    result_path = markdown_tool.generate_itinerary_md(itin, output_dir=test_dir)
    
    # Assert
    assert os.path.exists(result_path)
    
    with open(result_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Voyager AI Itinerary: Rome" in content
        assert "A historic trip to Italy." in content
        assert "Flights & Transit:** $500" in content
        assert "Colosseum" in content
        
    # Cleanup
    shutil.rmtree(test_dir)
