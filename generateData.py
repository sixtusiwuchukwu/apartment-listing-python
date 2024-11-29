import json

def generate_house_data(num_houses=30):
    houses = []
    for i in range(num_houses):
        house = {
            "title": f"House {i+1}",
            "location": f"City {i+1}, Province {i%4+1}",
            "description": f"A beautiful house in {i+1} city.",
            "address": f"{i+1} Main Street, City {i+1}",
            "Sqft": 1500 + i * 50,
            "propertyDetails": {
                "images": [f"https://example.com/image_{i+1}.jpg"],
                "propertyStatus": "For Sale",
                "propertyType": "Single Family Home",
                "rooms": 3 + i % 3,
                "garages": 1 + i % 2,
                "bedrooms": 2 + i % 3,
                "yearBuilt": 1990 + i,
                "propertyId": f"P{i+1000}",
                "price": 300000 + i * 10000,
                "bath": 2 + i % 2
            },
            "floorPlan": f"https://example.com/floorplan_{i+1}.jpg",
            "propertyFeatures": {
                "Air Conditioned": i % 2 == 0,
                "Swimming Pool": i % 3 == 0,
                "Fitness Gym": False,
                "Laundry": True,
                "Window Coverings": True,
                "Security Garage": i % 2 == 1,
                "Parking": 2,
                "Fireplace": i % 2 == 0,
                "Refrigerator": True
            }
        }
        houses.append(house)
    return houses

# Generate 30 house data points
houses_data = generate_house_data()

# Write the data to a JSON file
with open('houses.json', 'w') as f:
    json.dump(houses_data, f, indent=4)