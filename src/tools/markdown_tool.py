import os
from datetime import datetime
from src.models.schemas import ItineraryResponse

class MarkdownTool:
    """Utility for generating beautiful markdown itineraries from Pydantic models."""
    
    @staticmethod
    def generate_itinerary_md(itinerary: ItineraryResponse, output_dir: str = "outputs") -> str:
        """Converts an ItineraryResponse model into a formatted markdown file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{itinerary.destination.replace(' ', '_').lower()}_itinerary_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        md_content = f"# Voyager AI Itinerary: {itinerary.destination}\n\n"
        md_content += f"**Overview:** {itinerary.summary}\n\n"
        
        md_content += "## 💰 Estimated Budget Breakdown\n"
        md_content += f"- **Flights & Transit:** ${itinerary.budget.flightsTransit}\n"
        md_content += f"- **Accommodation:** ${itinerary.budget.accommodation}\n"
        md_content += f"- **Food & Dining:** ${itinerary.budget.foodDining}\n"
        md_content += f"- **Activities:** ${itinerary.budget.activities}\n"
        md_content += f"**Total Estimated Cost:** ${itinerary.budget.total}\n\n"
        
        md_content += "## 📅 Day-by-Day Plan\n\n"
        for day in itinerary.days:
            md_content += f"### Day {day.dayNumber}: {day.theme}\n"
            for activity in day.activities:
                md_content += f"- **{activity.timeOfDay}**: *{activity.title}* - {activity.description} (Est. ${activity.costEstimate})\n"
            md_content += "\n"
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        return filepath

# Global instance for easy import
markdown_tool = MarkdownTool()
