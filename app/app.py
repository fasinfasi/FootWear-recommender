from flask import Flask, render_template, request
from recommender import recommender_shoes
import pandas as pd

app = Flask(__name__)

# Load the same dataset to get product IDs
df = pd.read_csv("../data/cleaned_shoe_dataset.csv")
product_ids = df['Product_id'].tolist() 

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_id = None

    if request.method == 'POST':
        selected_id = request.form['product_id']
        recommendations = recommender_shoes(selected_id)

    return render_template("index.html", pid=product_ids, recommendations=recommendations, selected_id=selected_id)

if __name__ == "__main__":
    app.run(debug=True)
