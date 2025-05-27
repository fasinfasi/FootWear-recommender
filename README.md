# 👟 Shoozy – Shoe Recommender System 👟

**Shoozy** uses a **content-based filtering** that recommends shoes to users based on product similarity and customer preferences. It uses a content-based filtering approach and leverages machine learning and natural language processing to provide tailored recommendations.

Built with a **React frontend**, **Flask backend**, and deployed using **Docker** on **Render.com**, Shoozy delivers a clean, responsive, and smart user experience.

---

## 🌐 Live Demo

🔗 [Visit Shoozy](https://shoozy.onrender.com/)  

---

## 🚀 Features

- 🛍️ Personalized shoe recommendations
- 🔍 Filter by brand, gender, and price range
- 📈 Sort by popularity or ratings
- 🧠 Content-based filtering using product metadata and review text
- 🎨 Responsive UI built with React
- 🐳 Containerized with Docker
- ☁️ Deployed on Render.com

---

## 🧠 Tech Stack

| Layer  | Technology   |
|-----------|-----------|
| Frontend     | React.js     |
| Backend  | Flask (Python)  |
| ML/NLP |  TfidfVectorizer, Cosine Similarity, Scikit-learn |
| Deployment  | Render.com  |
| Data format  | CSV Dataset with 1000+ products  |

---

## 🗂️ Project Structure

```
Footwear/
├── app/
│ ├── app.py             # Flask app with API endpoints
│ ├── requirements.txt
│ ├── Dockerfile         # Backend docker
│ ├── render.yaml
│ └── data
│ │ ├── shoe_dataset.csv          # original dataset
│ │ └── cleaned_shoe_dataset.csv      # cleaned dataset
├── ui/
│ ├── src/
│ │ ├── App.js               # Main React component
│ │ ├── index.js             # React entry point
│ │ ├── Dockerfile           # Frontend docker
│ │ └── components/
│ │   ├── ProductCard.js
│ │   └── FilterPanel.js
├── model/
│ ├── similarity.pkl       # Precomputed similarity matrix
│ └── vectorizer.pkl       # TF-IDF vectorizer
├── notebooks/
│ ├── data_preprocessing.ipynb
│ ├── Feature_engineering.ipynb
│ └── shoe_image_urls_adding.ipynb
├── model_build.py         # Model training + vectorization
├── docker-compose.yml
└── .env  
```

---

## 🧪 How It Works

1. **Dataset**: Contains 1000+ shoe products with metadata like brand, type, gender, price, and reviews.
2. **Preprocessing**: Text reviews and titles are vectorized using `TfidfVectorizer`.
3. **Similarity Matrix**: Cosine similarity is calculated between all products.
4. **User Selection**: When a product is selected, the top N similar products are recommended.
5. **API**: Flask serves recommendations via REST endpoints.
6. **Frontend**: React fetches and displays results with filtering and sorting options.

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/fasinfasi/FootWear-recommender.git
cd shoozy
```

### 2. Run with Docker

```bash
docker build -t shoozy .
docker run -p 5000:5000 shoozy
```
By default, Flask runs on `http://localhost:5000`

### 3. Run React Frontend (Dev Mode)

```bash
cd ui
npm install
npm start
```
React will run on `http://localhost:3000` and fetch data from Flask

## ☁️ Deployment on Render.com

Follow these steps to deploy both **backend (Flask)** and **frontend (React)** using Docker on [Render.com](https://render.com).

### 📦 1. Prerequisites

- A [Render](https://render.com) account (sign up if you don't have one)
- Your project pushed to a public or private GitHub repository
- A working `Dockerfile` in the appropriate directories

---

### 🐳 2. Deploy Flask Backend (API)

Assuming your backend is located inside the `app/` folder and served via `app.py`.

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New Web Service"**
3. Connect your GitHub repository
4. Fill in the following details:

    ```
    Name: shoozy-backend
    Environment: Docker
    Region: (Choose closest to you)
    Branch: main (or your working branch)
    Root Directory: .
    Docker Command: (Leave it empty if using a valid Dockerfile)
    ```

5. Click **"Create Web Service"**

Once deployed, Render will give you a URL like: `https://shoozy-backend.onrender.com`

### 🌐 3. Deploy React Frontend (UI)

Assuming your frontend is located inside the `ui/` folder.

1. Create another **"New Web Service"** on Render
2. Connect the same GitHub repository
3. Set the following details:

    ```
    Name: shoozy-frontend
    Environment: Docker
    Branch: main (or your working branch)
    Root Directory: ui
    Dockerfile Path: ui/Dockerfile
    ```

Make sure your React app calls the correct backend API URL. Update it like this:

```js
// Example: ui/src/App.js
const API_BASE_URL = "https://shoozy-backend.onrender.com";
```

## 🎥 Demo
[Screen Record](https://www.linkedin.com/posts/fasinfasi_who-need-shoe-my-shoozy-will-assist-you-activity-7332814685911560194-SDBN?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD3BfD8BjijEcsfQ3UqR8o2hIwaylWYirK0)

## 📊 Dataset Overview

- Rows: 1000+
- Columns: Product ID, Brand, Type, Gender, Size, Number Sold, Price, Review Title, Review Text, Review Rating
- Used for training the recommender and powering the filtering system.

## 📄License

This project is licensed under the MIT License - see the [License](LICENSE) file for details.

🥰😘 Thanks bro, spending your valuable time to read my ReadMe....😘
Remember my name Fasin 🙋🏻‍♂️
