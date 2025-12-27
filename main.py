import json

# -----------------------------
# CITY COORDINATES
# -----------------------------
CITY_COORDINATES = {
    "delhi": (28.6139, 77.2090),
    "goa": (15.2993, 74.1240),
    "hyderabad": (17.3850, 78.4867),
    "mumbai": (19.0760, 72.8777)
}

# -----------------------------
# LOAD JSON DATA
# -----------------------------
def load_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# -----------------------------
# FLIGHT SELECTION
# -----------------------------
def select_cheapest_flight(flights, source, destination):
    matches = [
        f for f in flights
        if f.get("from", "").lower() == source.lower()
        and f.get("to", "").lower() == destination.lower()
    ]
    return min(matches, key=lambda x: x.get("price", float("inf"))) if matches else None

# -----------------------------
# HOTEL SELECTION
# -----------------------------
def select_best_hotel(hotels, city):
    matches = [
        h for h in hotels
        if h.get("city", "").lower() == city.lower()
    ]
    return max(matches, key=lambda x: x.get("stars", 0)) if matches else None

# -----------------------------
# PLACES / ITINERARY
# -----------------------------
def get_places_by_city(places, city):
    return [
        place.get("name")
        for place in places
        if place.get("city", "").lower() == city.lower()
    ]


if __name__ == "__main__":
    print("Backend module only. Run app.py for UI.")
