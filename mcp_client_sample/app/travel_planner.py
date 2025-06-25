from crewai.tools import tool
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import Dict

@tool("Search for available flights between cities")
def search_flights(origin: str, destination: str, date: str) -> Dict:
    """
    Search for available flights between cities.
    
    Args:
        origin: Departure city
        destination: Arrival city
        date: Travel date (YYYY-MM-DD)
    
    Returns:
        Dictionary containing flight options and prices
    """
    # Emulate JSON data from an API
    return {
        "flights": [
            {"airline": "Air France", "price": 850, "departure": "New York (JFK)", "arrival": "Paris (CDG)", "duration": "7h 30m", "departure_time": "10:30 AM", "arrival_time": "11:00 PM"},
            {"airline": "Delta Airlines", "price": 780, "departure": "New York (JFK)", "arrival": "Paris (CDG)", "duration": "7h 45m", "departure_time": "5:30 PM", "arrival_time": "6:15 AM"},
            {"airline": "United Airlines", "price": 920, "departure": "New York (EWR)", "arrival": "Paris (CDG)", "duration": "7h 55m", "departure_time": "8:45 PM", "arrival_time": "9:40 AM"}
        ]}             

@tool("Find available hotels in a location") 
def find_hotels(location: str, check_in: str, check_out: str) -> Dict:
    """
    Search for available hotels in a location.
    
    Args:
        location: City name
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
    
    Returns:
        Dictionary containing hotel options and prices
    """
    # Emulate JSON data from an API
    return {
        "hotels": [
            {"name": "Paris Marriott Champs Elysees", "price": 450, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.5, "location": "Central Paris", "amenities": ["Spa", "Restaurant", "Room Service"]},
            {"name": "Citadines Saint-Germain-des-Prés", "price": 280, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.2, "location": "Saint-Germain", "amenities": ["Kitchenette", "Laundry", "Wifi"]},
            {"name": "Ibis Paris Eiffel Tower", "price": 180, "check_in_date": check_in, "check_out_date": check_out, "rating": 4.0, "location": "Near Eiffel Tower", "amenities": ["Restaurant", "Bar", "Wifi"]}
        ]}

@tool("Find available activities in a location")
def find_activities(location: str, date: str, preferences: str) -> Dict:
    """
    Find available activities in a location.
    
    Args:
        location: City name
        date: Activity date (YYYY-MM-DD)
        preferences: Activity preferences/requirements
        
    Returns:
        Dictionary containing activity options
    """
    # Implement actual activity search logic here
    return {
        "activities": [
            {"name": "Eiffel Tower Skip-the-Line", "description": "Priority access to the Eiffel Tower with guided tour of 1st and 2nd floors", "price": 65, "duration": "2 hours", "start_time": "10:00 AM", "meeting_point": "Eiffel Tower South Entrance"},
            {"name": "Louvre Museum Guided Tour", "description": "Expert-guided tour of the Louvre's masterpieces including Mona Lisa", "price": 85, "duration": "3 hours", "start_time": "2:00 PM", "meeting_point": "Louvre Pyramid"},
            {"name": "Seine River Dinner Cruise", "description": "Evening cruise along the Seine with 3-course French dinner and wine", "price": 120, "duration": "2.5 hours", "start_time": "7:30 PM", "meeting_point": "Port de la Bourdonnais"}
        ]}


class TravelPlannerCrewAI:
    def __init__(self):        

        # Create specialized agents for different aspects of travel planning
        self.travel_specialist = Agent(
            role='An expert travel concierge',
            goal='Handle all aspects of travel planning',
            backstory="Expert in airline bookings and flight logistics, hotel bookings, and booking vacation activities.",
            tools=[search_flights, find_hotels, find_activities],
            verbose=False
        )

    def plan_travel(self, request: str) -> Dict:
        # Define the top-level task for travel planning
        travel_planning_task = Task(
            description=f"""
            Plan a comprehensive travel and leisure itinerary based on the following request:
            {request}
            
            The plan should include:
            - Flight arrangements
            - Accommodation bookings
            - Any other relevant travel components
            """,
            expected_output="A detailed travel itinerary covering all requested aspects.",
            agent=self.travel_specialist 
        )

        # Create the crew with a hierarchical process
        crew = Crew(
            agents=[self.travel_specialist],
            tasks=[travel_planning_task],
            process=Process.sequential,
            # manager_llm=self.manager_llm,
            verbose=False
        )

        # Execute the hierarchical plan
        return crew.kickoff()

# Entry point
if __name__ == "__main__":
    planner = TravelPlannerCrewAI()

    # Define a travel request
    request = """
    I need to plan a trip to Paris from New York for 5 days.
    """

    # Execute the hierarchical planning process
    result = planner.plan_travel(request)

    # Print the result
    print("Final Travel Plan:")
    print(result)