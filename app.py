import math
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

app = Flask(__name__)
# Enable CORS for the entire application
CORS(app)
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

import pandas as pd

import pandas as pd

def get_similar_houses(house_id, houses_file, page=1, page_size=2):
    """
    Find similar houses based on specified criteria and paginate results.

    Parameters:
    - house_id: The ID of the target house.
    - houses_file: Path to the JSON file containing house data.
    - page: The current page number (default is 1).
    - page_size: The number of results per page (default is 10).

    Returns:
    - A dictionary containing the current page, total pages, and similar houses as a list of dictionaries.
    """
    # Load the JSON data as a pandas DataFrame
    houses = pd.read_json(houses_file)
    
    # Ensure the house_id exists in the dataset
    target_house = houses[houses["propertyDetails"].apply(lambda x: x.get("propertyId") == house_id)]
    if target_house.empty:
        return {"error": f"Invalid house ID: {house_id}. No matching house found."}

    # Extract target house details
    target_house = target_house.iloc[0]  # Extract the first (and only) matching row

    # Define similarity criteria
    similar_houses = houses[
        (
            houses["propertyDetails"].apply(lambda x: x.get("bedrooms")) == target_house["propertyDetails"]["bedrooms"]
        ) | (
            abs(houses["propertyDetails"].apply(lambda x: x.get("price", 0)) - target_house["propertyDetails"]["price"]) <= 50000
        ) | (
            houses["location"] == target_house["location"]
        )
    ]

    # Exclude the target house itself
    similar_houses = similar_houses[houses["propertyDetails"].apply(lambda x: x.get("propertyId")) != house_id]

    # Apply pagination
    total_results = len(similar_houses)
    total_pages = (total_results + page_size - 1) // page_size  # Calculate total pages
    start = (page - 1) * page_size
    end = start + page_size

    # Slice the DataFrame for the current page
    paginated_houses = similar_houses.iloc[start:end]

    # Return the paginated results
    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_results": total_results,
        "similar_houses": paginated_houses.to_dict(orient="records")
    }


# Example usage
# houses_file = "houses.json"
# house_id = 101  # Replace with the desired house ID
# similar_houses = get_similar_houses(house_id, houses_file)

# print("Similar Houses:", similar_houses)


# Endpoint to get single house details
@app.route('/house/<property_id>', methods=['GET'])
def get_house_details(property_id):
    try:
        # Ensure property_id is treated as a string
        property_id = str(property_id)

        # Filter the DataFrame based on the propertyId inside 'propertyDetails'
        house_details = df[df['propertyDetails'].apply(lambda x: x.get('propertyId') == property_id)]

        # Check if a house with the given ID was found
        if house_details.empty:
            return jsonify({'error': 'House not found'}), 404

        # Return the first (and only) matching house as a dictionary
        return jsonify(house_details.iloc[0].to_dict())

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


@app.route('/houses/filter', methods=['GET'])
def filter_houses():
    try:
        
        # Extract query parameters
        city = request.args.get('city')
        region = request.args.get('region')
        house_type = request.args.get('type')
        keywords = request.args.get('keywords')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_bedrooms = request.args.get('min_bedrooms')
        max_bedrooms = request.args.get('max_bedrooms')
        min_bathrooms = request.args.get('min_bathrooms')
        max_bathrooms = request.args.get('max_bathrooms')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
      # # Flatten the nested propertyDetails dictionary
        df['price'] = df['propertyDetails'].apply(lambda x: x['price'])
        # df['city'] = df['propertyDetails'].apply(lambda x: x['city'])
        df['propertyType'] = df['propertyDetails'].apply(lambda x: x['propertyType'])
        df['bedrooms'] = df['propertyDetails'].apply(lambda x: x['bedrooms'])
        df['bathrooms'] = df['propertyDetails'].apply(lambda x: x['bathrooms'])

        # Create a copy of the DataFrame to filter
        filtered_df = df.copy()

        # Apply filters conditionally
        if city:
            filtered_df = filtered_df[filtered_df['city'].str.contains(city, case=False)]
            print('city:',city)
        if region:
            filtered_df = filtered_df[filtered_df['region'].str.contains(region, case=False)]
            print('region:',region)

        if house_type:
            filtered_df = filtered_df[filtered_df['propertyType'].str.contains(house_type, case=False)]
            print('house type:',house_type)

        if keywords:
            filtered_df = filtered_df[filtered_df['description'].str.lower().str.contains(keywords.lower())] 
            print('keyword',keywords)

        if min_price:
            filtered_df = filtered_df[filtered_df['price'] >= int(min_price)]
            print('min price',min_price)

        if max_price:
            filtered_df = filtered_df[filtered_df['price'] <= int(max_price)]
            print('max price: ',max_price)

        if min_bedrooms:
            filtered_df = filtered_df[filtered_df['bedrooms'] >= int(min_bedrooms)]
            print('min bed room')

        if max_bedrooms:
            filtered_df = filtered_df[filtered_df['bedrooms'] <= int(max_bedrooms)]
            print('max bed')

        if min_bathrooms:
            filtered_df = filtered_df[filtered_df['bathrooms'] >= int(min_bathrooms)]
            print('max bath')

        if max_bathrooms:
            filtered_df = filtered_df[filtered_df['bathrooms'] <= int(max_bathrooms)]
            print('min bath')

        # Handle case where no filters are applied
        if not any([city, region, house_type, keywords, min_price, max_price, 
                    min_bedrooms, max_bedrooms, min_bathrooms, max_bathrooms]):
            filtered_df = df.copy() 

        # Pagination
        total_houses = len(filtered_df)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_houses = filtered_df.iloc[start_index:end_index].to_dict('records')

        # Response
        return jsonify({
            "houses": paginated_houses,
            "total_houses": total_houses,
            "total_pages": math.ceil(total_houses / per_page),
            "current_page": page
        })
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


# Endpoint to get houses with pagination
@app.route('/houses', methods=['GET'])
def get_houses():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    total_houses = len(df)
    total_pages = math.ceil(total_houses / per_page)

    houses = df[start_index:end_index].to_dict('records')

    return jsonify({
            "houses": houses,
            "total_pages": total_pages,
            "current_page": page,
            "total_houses": total_houses,
            "per_page": per_page
        })

@app.route('/houses/similar/<house_id>', methods=['GET'])
def get_similar_houses_endpoint(house_id):
   
    similar_houses = get_similar_houses(house_id,"houses.json")
    # return jsonify(similar_houses)
    return jsonify(similar_houses)
     

if __name__ == '__main__':
    app.run(debug=True)