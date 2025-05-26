from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Enable CORS for all routes and all origins for development
CORS(app, resources={r"/*": {"origins": "https://shoozy.onrender.com/"}})
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "similarity.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "..", "model", "vectorizer.pkl")
CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_shoe_dataset.csv")

# Initialize global variables
df = None
product_ids = []
similarity_model = None
vectorizer_model = None

def load_data():
    """Load dataset and model"""
    global df, product_ids, similarity_model, vectorizer_model
    
    try:
        # Load CSV
        if not os.path.exists(CSV_PATH):
            logger.error(f"CSV file not found at: {CSV_PATH}")
            return False
            
        df = pd.read_csv(CSV_PATH)
        product_ids = df['Product_id'].unique().tolist()
        logger.info(f"Loaded {len(df)} shoes from dataset")
        
        # Load similarity model
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                similarity_model = pickle.load(f)
            logger.info("Similarity model loaded successfully")
        else:
            logger.warning(f"Similarity model not found at: {MODEL_PATH}")
            
        # Load vectorizer model
        if os.path.exists(VECTORIZER_PATH):
            with open(VECTORIZER_PATH, "rb") as f:
                vectorizer_model = pickle.load(f)
            logger.info("Vectorizer model loaded successfully")
        else:
            logger.warning(f"Vectorizer model not found at: {VECTORIZER_PATH}")
            
        return True
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return False

# Load data on startup
if not load_data():
    logger.error("Failed to load data on startup")

@app.route('/')
def home():
    return jsonify({
        "message": "Shoe Recommender API is running",
        "endpoints": [
            "/products - Get all product IDs",
            "/random-shoes - Get random shoes",
            "/filter-shoes - Filter shoes (POST)",
            "/recommend - Get recommendations (POST)"
        ],
        "status": "healthy" if df is not None else "unhealthy"
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy" if df is not None else "unhealthy",
        "data_loaded": df is not None,
        "similarity_model_loaded": similarity_model is not None,
        "vectorizer_model_loaded": vectorizer_model is not None,
        "total_shoes": len(df) if df is not None else 0
    })

@app.route('/products', methods=['GET'])
def get_products():
    try:
        if df is None:
            return jsonify({"error": "Dataset not loaded"}), 500
        return jsonify(product_ids)
    except Exception as e:
        logger.error(f"Error in /products: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/random-shoes', methods=['GET'])
def get_random_shoes():
    try:
        if df is None:
            return jsonify({"error": "Dataset not loaded"}), 500
            
        # Get random shoes from the dataset
        n_samples = min(90, len(df))
        random_shoes = df.sample(n=n_samples)
        
        # Select columns and handle missing values
        columns_to_return = ['Product_id', 'Brand', 'Type', 'Gender', 'Size', 
                           'Number_Sold', 'Price(USD)', 'url', 'review_rating', 'review_text']
        
        output = random_shoes[columns_to_return].fillna('').to_dict(orient='records')
        
        logger.info(f"Returning {len(output)} random shoes")
        return jsonify(output)
        
    except Exception as e:
        logger.error(f"Error in /random-shoes: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/filter-shoes', methods=['POST'])
def filter_shoes():
    try:
        if df is None:
            return jsonify({"error": "Dataset not loaded"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        selected_brand = data.get('brand', '')
        selected_gender = data.get('gender', '')
        price_range = data.get('price_range', '')
        sort_by = data.get('sort_by', '')

        logger.info(f"Filter request: {data}")
        
        # Start with all shoes
        filtered_shoes = df.copy()

        # Apply filters
        if selected_brand:
            filtered_shoes = filtered_shoes[filtered_shoes['Brand'] == selected_brand]
            logger.info(f"After brand filter: {len(filtered_shoes)} shoes")
            
        if selected_gender:
            filtered_shoes = filtered_shoes[filtered_shoes['Gender'] == selected_gender]
            logger.info(f"After gender filter: {len(filtered_shoes)} shoes")
            
        if price_range:
            if price_range == '0-50':
                filtered_shoes = filtered_shoes[filtered_shoes['Price(USD)'] <= 50]
            elif price_range == '50-100':
                filtered_shoes = filtered_shoes[
                    (filtered_shoes['Price(USD)'] > 50) & 
                    (filtered_shoes['Price(USD)'] <= 100)
                ]
            elif price_range == '100+':
                filtered_shoes = filtered_shoes[filtered_shoes['Price(USD)'] > 100]
            logger.info(f"After price filter: {len(filtered_shoes)} shoes")

        # Apply sorting
        if sort_by == 'rating':
            filtered_shoes = filtered_shoes.sort_values(
                by='review_rating', ascending=False, na_position='last'
            )
        elif sort_by == 'sold':
            filtered_shoes = filtered_shoes.sort_values(
                by='Number_Sold', ascending=False, na_position='last'
            )

        # Limit results
        filtered_shoes = filtered_shoes.head(50)

        columns_to_return = ['Product_id', 'Brand', 'Type', 'Gender', 'Size', 
                           'Number_Sold', 'Price(USD)', 'url', 'review_rating', 'review_text']
        
        output = filtered_shoes[columns_to_return].fillna('').to_dict(orient='records')
        
        logger.info(f"Returning {len(output)} filtered shoes")
        return jsonify(output)
        
    except Exception as e:
        logger.error(f"Error in /filter-shoes: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        if df is None:
            return jsonify({"error": "Dataset not loaded"}), 500
            
        if similarity_model is None:
            return jsonify({"error": "Recommendation model not loaded"}), 500
        
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

        logger.info(f"Recommendation request: {data}")
        
        # Check if product exists
        if product_name not in df['Product_id'].values:
            logger.warning(f"Product {product_name} not found")
            return jsonify([])

        # Get recommendations
        index = df[df['Product_id'] == product_name].index[0]
        distances = similarity_model[index]
        similar_items = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:51]

        recommended = df.iloc[[i[0] for i in similar_items]].copy()
        logger.info(f"Found {len(recommended)} similar items")

        # Apply filters
        if selected_brand:
            recommended = recommended[recommended['Brand'] == selected_brand]
        if selected_gender:
            recommended = recommended[recommended['Gender'] == selected_gender]
        if price_range:
            if price_range == '0-50':
                recommended = recommended[recommended['Price(USD)'] <= 50]
            elif price_range == '50-100':
                recommended = recommended[
                    (recommended['Price(USD)'] > 50) & 
                    (recommended['Price(USD)'] <= 100)
                ]
            elif price_range == '100+':
                recommended = recommended[recommended['Price(USD)'] > 100]

        # Apply sorting
        if sort_by == 'rating':
            recommended = recommended.sort_values(
                by='review_rating', ascending=False, na_position='last'
            )
        elif sort_by == 'sold':
            recommended = recommended.sort_values(
                by='Number_Sold', ascending=False, na_position='last'
            )

        columns_to_return = ['Product_id', 'Brand', 'Type', 'Gender', 'Size', 
                           'Number_Sold', 'Price(USD)', 'url', 'review_rating', 'review_text']
        
        output = recommended[columns_to_return].head(10).fillna('').to_dict(orient='records')
        
        logger.info(f"Returning {len(output)} recommendations")
        return jsonify(output)
        
    except Exception as e:
        logger.error(f"Error in /recommend: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
