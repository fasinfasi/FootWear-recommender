from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import recommender_shoes
import pickle
import pandas as pd
import os
import random

app = Flask(__name__)
# Enable CORS for all routes and all origins for development
CORS(app)

# Get the absolute path to the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "similarity.pkl")

df = pd.read_csv(os.path.join(BASE_DIR, "data", "cleaned_shoe_dataset.csv"))

# Load the dataset
product_ids = df['Product_id'].unique().tolist()

@app.route('/')
def home():
    return jsonify({"message": "Shoe Recommender API is running"})

@app.route('/products', methods=['GET'])
def get_products():
    try:
        return jsonify(product_ids)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/random-shoes', methods=['GET'])
def get_random_shoes():
    try:
        # Get 30 random shoes from the dataset
        random_shoes = df.sample(n=min(90, len(df)))
        
        output = random_shoes[['Product_id', 'Brand', 'Type', 'Gender', 'Size', 'Number_Sold', 'Price(USD)', 'url','review_rating', 'review_text']].to_dict(orient='records')
        
        return jsonify(output)
    except Exception as e:
        import traceback
        print(f"Error in /random-shoes: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/filter-shoes', methods=['POST'])
def filter_shoes():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        selected_brand = data.get('brand', '')
        selected_gender = data.get('gender', '')
        price_range = data.get('price_range', '')
        sort_by = data.get('sort_by', '')

        print(f"Filter request data: {data}")  # Debug print
        
        # Start with all shoes
        filtered_shoes = df.copy()

        # Apply filters
        if selected_brand:
            filtered_shoes = filtered_shoes[filtered_shoes['Brand'] == selected_brand]
        if selected_gender:
            filtered_shoes = filtered_shoes[filtered_shoes['Gender'] == selected_gender]
        if price_range:
            if price_range == '0-50':
                filtered_shoes = filtered_shoes[filtered_shoes['Price(USD)'] <= 50]
            elif price_range == '50-100':
                filtered_shoes = filtered_shoes[(filtered_shoes['Price(USD)'] > 50) & (filtered_shoes['Price(USD)'] <= 100)]
            elif price_range == '100+':
                filtered_shoes = filtered_shoes[filtered_shoes['Price(USD)'] > 100]

        # Apply sorting
        if sort_by == 'rating':
            filtered_shoes = filtered_shoes.sort_values(by='review_rating', ascending=False, na_position='last')
        elif sort_by == 'sold':
            filtered_shoes = filtered_shoes.sort_values(by='Number_Sold', ascending=False, na_position='last')

        # Limit to 50 results for better performance
        filtered_shoes = filtered_shoes.head(50)

        output = filtered_shoes[['Product_id', 'Brand', 'Type', 'Gender', 'Size', 'Number_Sold', 'Price(USD)', 'url','review_rating', 'review_text']].to_dict(orient='records')

        return jsonify(output)
    except Exception as e:
        import traceback
        print(f"Error in /filter-shoes: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        product_name = data.get('product_name')
        if not product_name:
            return jsonify({"error": "No product_name provided"}), 400
            
        selected_brand = data.get('brand', '')
        selected_gender = data.get('gender', '')
        price_range = data.get('price_range', '')
        sort_by = data.get('sort_by', '')

        print(f"Request data: {data}")  # Debug print
        
        if product_name not in df['Product_id'].values:
            return jsonify([])

        with open(MODEL_PATH, "rb") as f:
            similarity = pickle.load(f)

        index = df[df['Product_id'] == product_name].index[0]
        distances = similarity[index]
        similar_items = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:51]

        recommended = df.iloc[[i[0] for i in similar_items]].copy()

        if selected_brand:
            recommended = recommended[recommended['Brand'] == selected_brand]
        if selected_gender:
            recommended = recommended[recommended['Gender'] == selected_gender]
        if price_range:
            if price_range == '0-50':
                recommended = recommended[recommended['Price(USD)'] <= 50]
            elif price_range == '50-100':
                recommended = recommended[(recommended['Price(USD)'] > 50) & (recommended['Price(USD)'] <= 100)]
            elif price_range == '100+':
                recommended = recommended[recommended['Price(USD)'] > 100]

        if sort_by == 'rating':
            recommended = recommended.sort_values(by='review_rating', ascending=False, na_position='last')
        elif sort_by == 'sold':
            recommended = recommended.sort_values(by='Number_Sold', ascending=False, na_position='last')

        output = recommended[['Product_id', 'Brand', 'Type', 'Gender', 'Size', 'Number_Sold', 'Price(USD)', 'url','review_rating', 'review_text']].head(10).to_dict(orient='records')

        return jsonify(output)
    except Exception as e:
        import traceback
        print(f"Error in /recommend: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)