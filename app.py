import streamlit as st

from main import (
    load_json_data,
    select_cheapest_flight,
    select_best_hotel,
    get_places_by_city,
    CITY_COORDINATES
)

from weather import get_weather
from budget import calculate_budget
itinerary = []



# -----------------------------
# WEATHER TYPE HELPER
# -----------------------------
def get_weather_type_by_temp(temp):
    if temp >= 30:
        return "☀️ Sunny & Warm"
    elif temp >= 25:
        return "🌤️ Pleasant"
    elif temp >= 18:
        return "☁️ Mild & Cloudy"
    else:
        return "❄️ Cold"


# -----------------------------
# PAGE HEADER
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>✈️ Agentic AI Travel Planner</h1>
    <p style='text-align: center; color: gray;'>
    Plan your trip intelligently with flights, hotels, itinerary, weather & budget
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# LOAD DATA
# -----------------------------
flights = load_json_data("data/flights.json")
hotels = load_json_data("data/hotels.json")
places = load_json_data("data/places.json")

# -----------------------------
# CITY OPTIONS
# -----------------------------
source_cities = sorted({f["from"].title() for f in flights})
destination_cities = sorted({f["to"].title() for f in flights})

# -----------------------------
# USER INPUTS
# -----------------------------
source = st.selectbox("📍 Source City", source_cities)
destination = st.selectbox("🎯 Destination City", destination_cities)
days = st.selectbox("📅 Number of Days", list(range(1, 8)), index=2)

# -----------------------------
# PLAN TRIP BUTTON
# -----------------------------
if st.button("🚀 Plan My Trip"):

    # -------- VALIDATIONS --------
    if source == destination:
        st.warning("⚠️ Source city and destination city cannot be the same.")
        st.stop()

    # -------- FLIGHT --------
    flight = select_cheapest_flight(flights, source, destination)
    if not flight:
        st.error("❌ No flights found for the selected route.")
        st.stop()

    # -------- HOTEL & ITINERARY --------
    hotel = select_best_hotel(hotels, destination)
    itinerary = get_places_by_city(places, destination)

    # -------- WEATHER --------
    city_key = destination.lower()
    if city_key in CITY_COORDINATES:
        lat, lon = CITY_COORDINATES[city_key]
        weather_data = get_weather(lat, lon, days)
    else:
        weather_data = []

    # -------- BUDGET --------
    budget = calculate_budget(
        flight.get("price", 0),
        hotel.get("price_per_night", 0) if hotel else 0,
        days
    )

    st.success("✅ Trip Planned Successfully!")

    # -----------------------------
    # FLIGHT DETAILS
    # -----------------------------
    st.subheader("✈️ Flight Details")
    st.write(f"**Airline:** {flight.get('airline')}")
    st.write(f"**Departure Time:** {flight.get('departure_time', 'N/A')}")
    st.write(f"**Price:** ₹{flight.get('price')}")

    # -----------------------------
    # HOTEL DETAILS
    # -----------------------------
    st.subheader("🏨 Hotel Details")
    if hotel:
        st.write(f"**Hotel:** {hotel.get('name')}")
        st.write(f"**Stars:** {hotel.get('stars')}")
        st.write(f"**Price/Night:** ₹{hotel.get('price_per_night')}")
    else:
        st.warning("No hotel found")

    # -----------------------------
    # ITINERARY
    # -----------------------------
    st.subheader("📍 Day-wise Itinerary")

    if not itinerary:
        st.warning("No places found")
    else:
        total_places = len(itinerary)

    if days > total_places:
        st.info(
            f"ℹ️ Only {total_places} unique places available. "
            f"Showing all without repetition."
        )

    for i, place in enumerate(itinerary[:days]):
        st.write(f"**Day {i+1}:** {place}")


    # -----------------------------
    # WEATHER (DAY-WISE WITH EMOJI)
    # -----------------------------
    st.subheader("🌦 Weather Forecast")
    st.caption("📌 Weather shown per day based on forecast data")

    if weather_data:
        for i in range(days):
            temp = round(weather_data[i])
            weather_type = get_weather_type_by_temp(temp)
            st.write(f"**Day {i+1}:** {weather_type} – {temp}°C 🌡️")
    else:
        st.warning("Weather data not available 🌫️")

    # -----------------------------
    # BUDGET
    # -----------------------------
    st.subheader("💰 Budget Breakdown")
    st.write(f"✈️ Flight: ₹{budget['flight']}")
    st.write(f"🏨 Hotel: ₹{budget['hotel']}")
    st.write(f"🍴 Food & Travel: ₹{budget['food']}")
    st.markdown("---")
    st.write(f"### 🧾 Total Cost: ₹{budget['total']}")
