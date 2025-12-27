def calculate_budget(flight_price, hotel_price_per_night, days):
    """
    Calculates total trip budget
    """
    food_cost_per_day = 800

    hotel_cost = hotel_price_per_night * days
    food_cost = food_cost_per_day * days
    total_cost = flight_price + hotel_cost + food_cost

    return {
        "flight": flight_price,
        "hotel": hotel_cost,
        "food": food_cost,
        "total": total_cost
    }
