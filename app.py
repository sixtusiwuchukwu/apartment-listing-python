from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

app = Flask(__name__)

# Load the trained model
# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)

# Load the house price data
# df = pd.read_csv('houses_prices_index.csv')
# Load the house price data
with open('houses.json', 'r') as f:
  data = json.load(f)
df = pd.DataFrame(data)


import json

# def get_similar_houses(house_id, housesd):
#     # Load the JSON data
#     houses = pd.read_json('houses.json')

#     print(type(houses), "Type of houses")

#     print("---------------------------------------")
#     print(houses[house_id - 1],"target house")
#     # print(houses[house_id - 1],"target house")
#     print("---------------------------------------")
#     # Check if the index is valid
#     if house_id - 1 < 0 or house_id - 1 >= len(houses):
#         return f"Invalid house ID: {house_id}"
    
    
#     # Use the index to get the target house
#     target_house = houses[house_id - 1]
#     # Define similarity criteria
#     def is_similar(house):
#         return (
#             house != target_house and  # Exclude the same house
#             house["location"] == target_house["location"] and  # Match location
#             abs(house["price"] - target_house["price"]) <= 50000 and  # Price range
#             house["bedrooms"] == target_house["bedrooms"]  # Match bedrooms
#         )
    
#     # Find similar houses
#     similar_houses = [house for house in houses if is_similar(house)]
#     return similar_houses

def get_similar_houses(house_id, houses_file):
    # Load the JSON data as a pandas DataFrame
    houses = pd.read_json(houses_file)
    
    
    # Ensure the house_id is within range
    if house_id - 1 < 0 or house_id - 1 >= len(houses):
        return f"Invalid house ID: {house_id}. Expected ID between 1 and {len(houses)}."
    
    # Get the target house using iloc
    target_house = houses.iloc[house_id - 1]
    print(target_house, "Target house")
    
    # Define similarity criteria using pandas filtering
    similar_houses = houses[
   (houses["propertyDetails"].apply(lambda x: x["bedrooms"]) == target_house["propertyDetails"]["bedrooms"])  | # Match location
    (abs(houses["propertyDetails"].apply(lambda x: x["price"]) - target_house["propertyDetails"]["price"]) <= 50000)  # Price range
   |
    (houses["location"] == target_house["location"]) &  # Match bedrooms
    (houses.index != house_id - 1)  # Exclude the target house itself
]

    return similar_houses.to_dict(orient="records")  # Convert to a list of dictionaries


# Example usage
# houses_file = "houses.json"
# house_id = 101  # Replace with the desired house ID
# similar_houses = get_similar_houses(house_id, houses_file)

# print("Similar Houses:", similar_houses)


# Endpoint to get single house details
@app.route('/house/<int:house_id>')
def get_house_details(house_id):
    try:
        house_details = df.iloc[house_id -1 ].to_dict()
        return jsonify(house_details)
    except IndexError:
        return jsonify({'error': 'House not found'}), 404


# Endpoint for houses filter
# Endpoint to get houses with advanced filtering
@app.route('/houses/filter', methods=['GET'])
def filter_houses():
    city = request.args.get('city')
    region = request.args.get('region')
    type = request.args.get('type')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_distance = request.args.get('min_distance')
    max_distance = request.args.get('max_distance')
    keywords = request.args.get('keywords')
    min_rooms = request.args.get('min_rooms')
    max_rooms = request.args.get('max_rooms')
    aircondition = request.args.get('aircondition')
    sort_by = request.args.get('sort_by', 'price')
    sort_order = request.args.get('sort_order', 'desc')
    sort_by = request.args.get('sort_by', 'price')
    sort_order = request.args.get('sort_order', 'desc')
    min_rooms = request.args.get('min_rooms')
    max_rooms = request.args.get('max_rooms')
    min_baths = request.args.get('min_baths')
    max_baths = request.args.get('max_baths')
    min_year = request.args.get('min_year')
    max_year = request.args.get('max_year')
    features = request.args.getlist('features')

    filtered_df = df.copy()

    # Filter by city
    if city:
        filtered_df = filtered_df[filtered_df['City'] == city]

    # Filter by region
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]

    # Filter by type
    if type:
        filtered_df = filtered_df[filtered_df['Type'] == type]

    # Filter by category
    if category:
        filtered_df = filtered_df[filtered_df['Category'] == category]

    # Filter by price range
    if min_price:
        filtered_df = filtered_df[filtered_df['Price'] >= int(min_price)]
    if max_price:
        filtered_df = filtered_df[filtered_df['Price'] <= int(max_price)]

    # Filter by distance (assuming you have latitude and longitude)
    if min_distance or max_distance:
        user_location = (float(request.args.get('user_lat')), float(request.args.get('user_lon')))
        filtered_df['distance'] = filtered_df.apply(lambda row: geopy.distance.geodesic(user_location, (row['Latitude'], row['Longitude'])).km, axis=1) # type: ignore
        if min_distance:
            filtered_df = filtered_df[filtered_df['distance'] >= float(min_distance)]
        if max_distance:
            filtered_df = filtered_df[filtered_df['distance'] <= float(max_distance)]

    # Filter by keywords (assuming you have a 'Keywords' column)
    if keywords:
        filtered_df = filtered_df[filtered_df['Keywords'].str.contains(keywords, case=False)]

    filtered_houses = filtered_df.to_dict('records')
    
    if min_rooms:
        filtered_df = filtered_df[filtered_df['Rooms'] >= int(min_rooms)]
    if max_rooms:
        filtered_df = filtered_df[filtered_df['Rooms'] <= int(max_rooms)]

    # Filter by aircondition
    if aircondition:
        filtered_df = filtered_df[filtered_df['Aircondition'] == aircondition]
    if min_rooms:
        filtered_df = filtered_df[filtered_df['Rooms'] >= int(min_rooms)]
    if min_baths:
        filtered_df = filtered_df[filtered_df['bath'] <= int(max_rooms)]
    if max_baths:
        filtered_df = filtered_df[filtered_df['bath'] <= int(max_rooms)]
    if max_rooms:
        filtered_df = filtered_df[filtered_df['Rooms'] <= int(max_rooms)]
    # ... similar for baths and year built
    # Filter by features
    if features:
        for feature in features:
            filtered_df = filtered_df[filtered_df[feature]]
            
    filtered_df = filtered_df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))
    filtered_houses = filtered_df.to_dict('records')
    return jsonify(filtered_houses)

# Endpoint to get houses with pagination
@app.route('/houses', methods=['GET'])
def get_houses():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    houses = df[start_index:end_index].to_dict('records')
    return jsonify(houses)

@app.route('/houses/similar/<int:house_id>', methods=['GET'])
def get_similar_houses_endpoint(house_id):
    print("-------------------------------------")
    print(house_id)
    print("-------------------------------------")
    similar_houses = get_similar_houses(house_id,"houses.json")
    # return jsonify(similar_houses)
    return jsonify(similar_houses)
     

if __name__ == '__main__':
    app.run(debug=True)