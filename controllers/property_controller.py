"""
controllers/property_controller.py
Dwello – Property Search Controller

Called by: ui/preference_screen.py
Calls to:  database layer (db/property_queries.py or similar)
"""


def search_properties_controller(region: str,
                                  min_budget: int,
                                  max_budget: int) -> dict:
    """
    Query the database for properties matching region and budget.

    Parameters
    ----------
    region     : str  – "mainland" or "island"
    min_budget : int  – minimum price in Naira
    max_budget : int  – maximum price in Naira

    Returns
    -------
    dict with keys:
        success    : bool
        properties : list[dict]  – each dict has id, title, location, price, image_path
        message    : str
    """
    # ── TODO: replace with real DB call ───────────────────────────────────────
    # from db.property_queries import fetch_properties
    # return fetch_properties(region, min_budget, max_budget)

    # Stub: return sample data filtered loosely by region keyword
    sample = [
        {"id": 1, "title": "2 Bedroom Apartment",  "location": "Yaba, Lagos Mainland",            "price": "₦4,000,000.00", "image_path": None},
        {"id": 2, "title": "Luxury House",         "location": "Victoria Island, Lagos Island",   "price": "₦4,500,000.00", "image_path": None},
        {"id": 3, "title": "Standard Duplex",      "location": "Yaba, Lagos Mainland",            "price": "₦3,800,000.00", "image_path": None},
        {"id": 4, "title": "3 Bedroom Terrace",    "location": "Ikeja, Lagos Mainland",           "price": "₦4,200,000.00", "image_path": None},
        {"id": 5, "title": "Mini Flat",            "location": "Surulere, Lagos Mainland",        "price": "₦2,500,000.00", "image_path": None},
        {"id": 6, "title": "Penthouse Suite",      "location": "Lekki, Lagos Island",             "price": "₦4,900,000.00", "image_path": None},
    ]

    region_keyword = "Mainland" if region == "mainland" else "Island"
    filtered = [p for p in sample if region_keyword in p["location"]]

    return {
        "success": True,
        "properties": filtered,
        "message": "",
    }
