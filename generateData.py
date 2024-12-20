import json
import random

# def generate_house_data(num_houses=30):
#     houses = []
#     for i in range(num_houses):
#         house = {
#             "title": f"House {i+1}",
#             "location": f"City {i+1}, Province {i%4+1}",
#             "description": f"A beautiful house in {i+1} city.",
#             "address": f"{i+1} Main Street, City {i+1}",
#             "Sqft": 1500 + i * 50,
#             "propertyDetails": {
#                 "images": [f"https://example.com/image_{i+1}.jpg"],
#                 "propertyStatus": "For Sale",
#                 "propertyType": "Single Family Home",
#                 "rooms": 3 + i % 3,
#                 "garages": 1 + i % 2,
#                 "bedrooms": 2 + i % 3,
#                 "yearBuilt": 1990 + i,
#                 "propertyId": f"P{i+1000}",
#                 "price": 300000 + i * 10000,
#                 "bath": 2 + i % 2
#             },
#             "floorPlan": f"https://example.com/floorplan_{i+1}.jpg",
#             "propertyFeatures": {
#                 "Air Conditioned": i % 2 == 0,
#                 "Swimming Pool": i % 3 == 0,
#                 "Fitness Gym": False,
#                 "Laundry": True,
#                 "Window Coverings": True,
#                 "Security Garage": i % 2 == 1,
#                 "Parking": 2,
#                 "Fireplace": i % 2 == 0,
#                 "Refrigerator": True
#             }
#         }
#         houses.append(house)
#     return houses

# # Generate 30 house data points
# houses_data = generate_house_data()

# # Write the data to a JSON file
# with open('houses.json', 'w') as f:
#     json.dump(houses_data, f, indent=4)
import json

# def update_data(data):
#     """
#     Updates the given data by adding 'region', 'keywords', and 'city' keys 
#     to each house dictionary.

#     Args:
#         data: A list of dictionaries, where each dictionary represents a house.

#     Returns:
#         A list of updated dictionaries with the added keys.
#     """

#     updated_data = []  # Create an empty list to store the updated houses

#     for house in data:
#         # Extract city and region from location
#         try:
#             city, region = house['location'].split(', ') 
#         except ValueError:
#             print(f"Error: Invalid location format for house: {house}")
#             city = None
#             region = None

#         # Extract keywords from description (optional: improve keyword extraction)
#         keywords = house['description'].lower().split() 

#         # Create a new dictionary with updated information
#         updated_house = {
#             **house,  # Copy existing key-value pairs
#             'region': region,
#             'city': city,
#             'keywords': keywords
#         }

#         # Append the updated house to the list
#         updated_data.append(updated_house)

#     return updated_data

# if __name__ == "__main__":
#     with open('houses.json', 'r') as f:
#         data = json.load(f)

#     updated_data = update_data(data)

#     with open('updated_houses.json', 'w') as f:
#         json.dump(updated_data, f, indent=4)
        
        
        
        
     

# def update_house_cities(houses):
#   """
#   Updates the 'city' field in each house object with a random Canadian city.

#   Args:
#     houses: A list of dictionaries, where each dictionary represents a house.

#   Returns:
#     A list of updated houses with Canadian city names.
#   """

#   canadian_cities = [
#       "Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa", 
#       "Edmonton", "Mississauga", "Brampton", "Hamilton", "Quebec City",
#       "Winnipeg", "Surrey", "Laval", "Halifax", "Windsor",
#       "Burnaby", "Richmond", "London", "Kitchener", "Victoria",
#       "Saskatoon", "Kelowna", "Regina", "Oshawa", "Guelph",
#       "St. Catharines", "Thunder Bay", "St. John's", "Abbotsford", 
#       "Markham", "Vaughan", "Barrie", "Moncton", "Kingston",
#       "Charlottetown", "Whitehorse", "Yellowknife", "Iqaluit",
#       # Add more Canadian cities if needed
#   ]

#   for house in houses:
#     house["city"] = random.choice(canadian_cities)

#   return houses


import random
import random

# def rename_houses(houses):
#   """
#   Renames the 'title' field in each house object with a more creative name.

#   Args:
#     houses: A list of dictionaries, where each dictionary represents a house.

#   Returns:
#     A list of updated houses with creative names.
#   """

#   house_names = [
#       "The Haven", "Sunnyside Cottage", "Oakwood Manor", "Willow Creek", 
#       "Riverbend Retreat", "Cedarwood Lodge", "Windswept Cottage", 
#       "Stonehaven", "Meadowbrook", "Bluebird Haven",
#       "Green Gables", "The Burrow", "Hillside Manor", "Harbor View", 
#       "Whispering Pines", "Starlight Cottage", "Golden Oak", 
#       "The Croft", "Woodland Retreat", "Seabreeze Cottage",
#       "Lakeside Lodge", "Forest Glen", "Sunstone Villa", "Azure Waters",
#       "Crimson Ridge", "Emerald Vale", "Silverwood", "Amberstone",
#       # Add more house names if needed
#   ]

#   for house in houses:
#     house["title"] = random.choice(house_names)

#   return houses

from faker import Faker

def update_house_addresses(houses):
  """
  Updates the 'address' field in each house object with a more realistic Canadian address.

  Args:
    houses: A list of dictionaries, where each dictionary represents a house.

  Returns:
    A list of updated houses with Canadian addresses.
  """

  fake = Faker('en_CA') 

  for house in houses:
    house["address"] = fake.street_address() 

  return houses




if __name__ == "__main__":
    with open('houses.json', 'r') as f:
        data = json.load(f)

    updated_data = update_house_addresses(data)
    print(updated_data)

    with open('updated_houses.json', 'w') as f:
        json.dump(updated_data, f, indent=4)
   