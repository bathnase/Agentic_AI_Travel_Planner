from langchain.agents import Tool, initialize_agent
from langchain_openai import ChatOpenAI

# import your EXISTING functions
from main import (
    select_cheapest_flight,
    select_best_hotel,
    get_places_by_city
)
from weather import get_weather
from budget import calculate_budget


def create_travel_agent(flights, hotels, places):
    """
    Creates a LangChain agent that orchestrates travel planning tools
    """

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    tools = [
        Tool(
            name="Flight Search Tool",
            func=lambda x: str(select_cheapest_flight(
                flights,
                x.split(",")[0],
                x.split(",")[1]
            )),
            description="Find cheapest flight. Input: source,destination"
        ),

        Tool(
            name="Hotel Recommendation Tool",
            func=lambda city: str(select_best_hotel(hotels, city)),
            description="Find best hotel for a city"
        ),

        Tool(
            name="Places Recommendation Tool",
            func=lambda city: str(get_places_by_city(places, city)),
            description="Find tourist places for a city"
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    return agent
