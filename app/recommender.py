import pandas as pd
import pickle
import os
 
# Get the absolute path to the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the dataset
df = pd.read_csv(os.path.join(BASE_DIR, "data", "cleaned_shoe_dataset.csv"))

# Load the vectorizer
with open(os.path.join(BASE_DIR, "model", "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)

# Load the similarity matrix
with open(os.path.join(BASE_DIR, "model", "similarity.pkl"), "rb") as f:
    similarity = pickle.load(f)

def recommender_shoes(product_id, top_n=5):
    try:
        idx = df[df['Product_id'] == product_id].index[0]
    except:
        return []

    scores = list(enumerate(similarity[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended = df.iloc[[i[0] for i in sorted_scores]]

    return recommended.to_dict(orient="records")
