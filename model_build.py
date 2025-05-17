import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

df = pd.read_csv('data/cleaned_shoe_dataset.csv')

df.fillna("", inplace=True)

df['combined_features'] = (
    df['Brand'].astype(str) + " " +
    df['Type'].astype(str) + " " +
    df['Gender'].astype(str) + " " +
    df['review_title'].astype(str) + " " +
    df['review_text'].astype(str)
)

vectorizer = TfidfVectorizer(stop_words='english')
vector_matrix = vectorizer.fit_transform(df['combined_features'])

similarity_matrix = cosine_similarity(vector_matrix)


with open("./model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("./model/similarity.pkl", "wb") as f:
    pickle.dump(similarity_matrix, f)
