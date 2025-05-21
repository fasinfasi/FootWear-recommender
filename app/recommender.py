import pandas as pd
import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')
SIMILARITY_PATH = os.path.join(BASE_DIR, 'model', 'similarity.pkl')

df = pd.read_csv(os.path.join(BASE_DIR, "data", "cleaned_shoe_dataset.csv"))

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(SIMILARITY_PATH, "rb") as f:
    similarity = pickle.load(f)

def recommender_shoes(product_id, top_n=5):
    try:
        idx = df[df['Product_id'] == product_id].index[0]
    except:
        return []

    scores = list(enumerate(similarity[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended = df.iloc[[i[0] for i in sorted_scores]]

    recommendations = []
    for _, row in recommended.iterrows():
        rec_dict = {}
        for column in recommended.columns:
            value = row[column]
            if pd.isna(value):
                rec_dict[column] = None
            elif isinstance(value, (np.integer, np.floating)):
                rec_dict[column] = float(value)
            else:
                rec_dict[column] = value
        recommendations.append(rec_dict)

    return recommendations