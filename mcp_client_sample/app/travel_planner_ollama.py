from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool  # Use BaseTool instead of @tool
from textwrap import dedent
from langchain_community.llms import Ollama

# Initialize LLM with Ollama
llm = Ollama(
    model="llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.7,
)

# Define Tools using BaseTool
class SearchFlightsTool(BaseTool):
    name: str = "Search for available flights between cities"
    description: str = (
        "Search for available flights between cities. "
        "Args: origin (str), destination (str), date (str, YYYY-MM-DD). "
        "Returns: Dictionary containing flight options and prices."
    )

    def _run(self, origin: str, destination: str, date: str) -> dict:
        try:
            flights = [
                {
                    "airline": "Air France",
                    "price": 850,
                    "departure": f"{origin} (JFK)",
                    "arrival": f"{destination} (CDG)",
                    "duration": "7h 30m",
                    "departure_time": "10:30 AM",
                    "arrival_time": "11:00 PM",
                    "date": date
                },
                {
                    "airline": "Delta Airlines",
                    "price": 780,
                    "departure": f"{origin} (JFK)",
                    "arrival": f"{destination} (CDG)",
                    "duration": "7h 45m",
                    "departure_time": "5:30 PM",
                    "arrival_time": "6:15 AM",
                    "date": date
                },
                {
                    "airline": "United Airlines",
                    "price": 920,
                    "departure": f"{origin} (EWR)",
                    "arrival": f"{destination} (CDG)",
                    "duration": "7h 55m",
                    "departure_time": "8:45 PM",
                    "arrival_time": "9:40 AM",
                    "date": date
                }
            ]
            return {"flights": flights}
        except Exception as e:
            return {"error": f"Failed to fetch flights: {str(e)}"}

class FindHotelsTool(BaseTool):
    name: str = "Find available hotels in a location"
    description: str = (
        "Search for available hotels in a location. "
        "Args: location (str), check_in (str, YYYY-MM-DD), check_out (str, YYYY-MM-DD). "
        "Returns: Dictionary containing hotel options and prices."
    )

    def _run(self, location: str, check_in: str, check_out: str) -> dict:
        try:
            return {
                "hotels": [
                    {
                        "name": "Paris Marriott Champs Elysees",
                        "price": 450,
                        "check_in_date": check_in,
                        "check_out_date": check_out,
                        "rating": 4.5,
                        "location": f"Central {location}",
                        "amenities": ["Spa", "Restaurant", "Room Service"]
                    },
                    {
                        "name": "Citadines Saint-Germain-des-Prés",
                        "price": 320,
                        "check_in_date": check_in,
                        "check_out_date": check_out,
                        "rating": 4.2,
                        "location": "Saint-Germain",
                        "amenities": ["Kitchenette", "Laundry", "Wifi"]
                    },
                    {
                        "name": "Ibis Paris Eiffel Tower",
                        "price": 380,
                        "check_in_date": check_in,
                        "check_out_date": check_out,
                        "rating": 4.0,
                        "location": f"Near Eiffel Tower, {location}",
                        "amenities": ["Restaurant", "Bar", "Wifi"]
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to fetch hotels: {str(e)}"}

class FindActivitiesTool(BaseTool):
    name: str = "Find available activities in a location"
    description: str = (
        "Find available activities in a location. "
        "Args: location (str), date (str, YYYY-MM-DD), preferences (str). "
        "Returns: Dictionary containing activity options."
    )

    def _run(self, location: str, date: str, preferences: str) -> dict:
        try:
            return {
                "activities": [
                    {
                        "name": "Eiffel Tower Skip-the-Line",
                        "description": f"Priority access to the Eiffel Tower in {location} with guided tour",
                        "price": 65,
                        "duration": "2 hours",
                        "start_time": "10:00 AM",
                        "meeting_point": "Eiffel Tower South Entrance",
                        "date": date
                    },
                    {
                        "name": "Louvre Museum Guided Tour",
                        "description": f"Expert-guided tour of the Louvre in {location}",
                        "price": 85,
                        "duration": "3 hours",
                        "start_time": "2:00 PM",
                        "meeting_point": "Louvre Pyramid",
                        "date": date
                    },
                    {
                        "name": "Seine River Dinner Cruise",
                        "description": f"Evening cruise along the Seine in {location}",
                        "price": 120,
                        "duration": "2.5 hours",
                        "start_time": "7:30 PM",
                        "meeting_point": "Port de la Bourdonnais",
                        "date": date
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to fetch activities: {str(e)}"}

class FindTransportationTool(BaseTool):
    name: str = "Find local transportation options"
    description: str = (
        "Find local transportation options between locations. "
        "Args: location (str), origin (str), destination (str). "
        "Returns: Dictionary containing transportation options."
    )

    def _run(self, location: str, origin: str, destination: str) -> dict:
        try:
            return {
                "options": [
                    {
                        "type": "Metro",
                        "cost": 1.90,
                        "duration": "25 minutes",
                        "frequency": "Every 5 minutes",
                        "route": f"Line 1 to Châtelet, then Line 4 to {destination}",
                        "pros": "Fast, avoids traffic",
                        "cons": "Can be crowded during peak hours"
                    },
                    {
                        "type": "Taxi",
                        "cost": 22.50,
                        "duration": "20 minutes",
                        "frequency": "On demand",
                        "route": "Direct",
                        "pros": "Door-to-door service, comfortable",
                        "cons": "More expensive, subject to traffic"
                    },
                    {
                        "type": "Bus",
                        "cost": 1.90,
                        "duration": "35 minutes",
                        "frequency": "Every 10 minutes",
                        "route": f"Route 42 direct to {destination}",
                        "pros": "Scenic route, above ground",
                        "cons": "Slower than metro, subject to traffic"
                    },
                    {
                        "type": "Walking",
                        "cost": 0,
                        "duration": "45 minutes",
                        "frequency": "Anytime",
                        "route": f"Through {location} city center",
                        "pros": "Free, healthy, scenic",
                        "cons": "Takes longer, weather dependent"
                    }
                ],
                "passes": [
                    {
                        "name": "Day Pass",
                        "cost": 7.50,
                        "valid_for": "Unlimited travel for 24 hours",
                        "recommended_if": "Making more than 4 trips in a day"
                    },
                    {
                        "name": "Paris Visite",
                        "cost": 12.00,
                        "valid_for": f"Unlimited travel for 1 day in {location}, includes discounts",
                        "recommended_if": "Planning to visit multiple tourist sites"
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to fetch transportation options: {str(e)}"}

# Instantiate Tools
search_flights_tool = SearchFlightsTool()
find_hotels_tool = FindHotelsTool()
find_activities_tool = FindActivitiesTool()
find_transportation_tool = FindTransportationTool()

# Create the Agents
flight_booking_worker = Agent(
    role="Flight Booking Specialist",
    goal="Find and book the optimal flights for the traveler",
    backstory="""You are an experienced flight booking specialist with extensive knowledge of airlines, 
    routes, and pricing strategies. You excel at finding the best flight options balancing cost, 
    convenience, and comfort according to the traveler's preferences.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_flights_tool],
    llm=llm,
    max_iter=1,
    max_retry_limit=3
)

hotel_booking_worker = Agent(
    role="Hotel Accommodation Expert",
    goal="Secure the ideal hotel accommodations for the traveler",
    backstory="""You have worked in the hospitality industry for over a decade and have deep knowledge 
    of hotel chains, boutique accommodations, and local lodging options worldwide. You're skilled at 
    matching travelers with accommodations that meet their budget, location preferences, and amenity requirements.""",
    verbose=True,
    allow_delegation=False,
    tools=[find_hotels_tool],
    llm=llm,
    max_iter=1,
    max_retry_limit=3
)

activity_planning_worker = Agent(
    role="Activities and Excursions Planner",
    goal="Curate personalized activities and experiences for the traveler",
    backstory="""You're a well-traveled activities coordinator with insider knowledge of attractions, 
    tours, and unique experiences across numerous destinations. You're passionate about creating 
    memorable itineraries that align with travelers' interests, whether they seek adventure, culture, 
    relaxation, or culinary experiences.""",
    verbose=True,
    allow_delegation=False,
    tools=[find_activities_tool],
    llm=llm,
    max_iter=1,
    max_retry_limit=3
)

transportation_worker = Agent(
    role="Local Transportation Coordinator",
    goal="Arrange efficient and convenient local transportation",
    backstory="""You specialize in local transportation logistics across global destinations. Your expertise 
    covers public transit systems, private transfers, rental services, and navigation, ensuring travelers 
    can move smoothly between destinations and activities.""",
    verbose=True,
    allow_delegation=False,
    tools=[find_transportation_tool],
    llm=llm,
    max_iter=1,
    max_retry_limit=3
)

# Define tasks for all the agents
flight_search_task = Task(
    description=dedent("""
        Use the SearchFlightsTool to find flight options from origin to destination on the specified date.
        Review the returned JSON data and recommend the best option based on the traveler's priorities, if any.
        Compare the available options and explain why the recommended choice best meets their needs.
    """),
    agent=flight_booking_worker,
    expected_output="A flight itinerary for booking based on the traveler's preferences."
)

hotel_search_task = Task(
    description=dedent("""
        Use the FindHotelsTool to search for accommodations in the destination for the specified check-in and check-out dates.
        Review the returned JSON data and recommend the best option considering budget and preferences.
        Explain why your recommended choice is the best match for this traveler.
    """),
    agent=hotel_booking_worker,
    expected_output="A hotel recommendation based on the traveler's preferences and budget."
)

activity_planning_task = Task(
    description=dedent("""
        Use the FindActivitiesTool to identify options in the destination for each day of the entire trip duration.
        The traveler's interests are: {activity_interests} with a {activity_pace} pace preference.
        Create a day-by-day plan using the returned JSON data, ensuring activities flow logically and match the traveler's interests.
    """),
    agent=activity_planning_worker,
    expected_output="A day-by-day activity plan that matches the traveler's interests and pace preferences."
)

transportation_planning_task = Task(
    description=dedent("""
        Use the FindTransportationTool to identify options at the destination for:
        1. Airport to hotel transfer
        2. Transportation between daily activities
        3. Hotel to airport transfer
        Consider the traveler's preferences where possible.
        Based on the returned JSON data, recommend the best transportation options for each segment of their trip.
    """),
    agent=transportation_worker,
    expected_output="A transportation plan covering all necessary transfers during the trip."
)

# Coordinator Agent
coordinator_agent = Agent(
    role="Coordinator Agent",
    goal="Ensure cohesive travel plans and maintain high customer satisfaction",
    backstory="""A seasoned travel industry veteran with 15 years of experience in luxury travel planning 
    and project management. Known for orchestrating seamless multi-destination trips for high-profile clients 
    and managing complex itineraries across different time zones and cultures.""",
    verbose=True,
    llm=llm,
    max_iter=1,
    max_retry_limit=3
)

# Delegate Plan Function
def delegate_plan(plan: str, activity_interests: str = "culture, history", activity_pace: str = "moderate"):
    """
    Delegate travel planning tasks to specialized agents based on the provided plan.
    
    Args:
        plan: The travel plan string containing origin, destination, dates, etc.
        activity_interests: Traveler's activity interests (default: culture, history)
        activity_pace: Preferred pace of activities (default: moderate)
    
    Returns:
        A formatted itinerary with flight, hotel, activities, and transportation details
    """
    # Validate plan input
    if not plan or not isinstance(plan, str):
        raise ValueError("Plan must be a non-empty string")

    # Replace placeholders in activity_planning_task description
    formatted_activity_task_description = activity_planning_task.description.format(
        activity_interests=activity_interests,
        activity_pace=activity_pace
    )
    activity_planning_task.description = formatted_activity_task_description

    delegator_goal = dedent(f"""
        Effectively distribute travel planning tasks to specialized workers to create a detailed booking itinerary
        for the plan below:
        
        {plan}
        
        Based on this plan, your goal is to create a detailed booking itinerary and trip plan for the user that includes
        flight booking & cost recommendation, hotels and hotel cost, activities and local transportation options
        and recommendations.
    """)

    delegator_agent = Agent(
        role="Travel Planning Delegator",
        goal=delegator_goal,
        backstory="""You are an expert project manager with a talent for breaking down travel planning into 
        component tasks and assigning them to the right specialists. You understand each worker's strengths 
        and ensure they have the information needed to excel. You track progress, resolve bottlenecks, and 
        ensure all elements of the trip are properly addressed.""",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    # Create and execute the crew
    delegator_crew = Crew(
        agents=[flight_booking_worker, hotel_booking_worker, transportation_worker, activity_planning_worker],
        tasks=[flight_search_task, hotel_search_task, transportation_planning_task, activity_planning_task],
        verbose=True,
        manager_agent=delegator_agent,
        process=Process.hierarchical,
        planning=True,
        full_output=True
    )

    try:
        full_itinerary = delegator_crew.kickoff()
        print("\n=== Delegator Task Complete ===\n")
        return full_itinerary
    except Exception as e:
        return {"error": f"Failed to generate itinerary: {str(e)}"}

# Example Usage
if __name__ == "__main__":
    sample_plan = """
    Traveler wants to go from New York to Paris from 2025-07-01 to 2025-07-07.
    Budget is $2000 for flights and hotels combined.
    Prefers cultural and historical activities at a moderate pace.
    """
    result = delegate_plan(
        plan=sample_plan,
        activity_interests="culture, history",
        activity_pace="moderate"
    )
    print(result)