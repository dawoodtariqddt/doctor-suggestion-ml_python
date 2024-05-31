#app/ml_model.py
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.naive_bayes import GaussianNB
import numpy as np
from .database import get_connection

class DoctorSuggestionModel:
    def __init__(self):
        pass

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch data for training the model
        cursor.execute("SELECT disability_related_to, disability_with, specialities FROM doctors")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        X = []
        y = []

        for row in data:
            # Assume disability_related_to and disability_with are lists
            X.append(row[:2])  # Features: disability_related_to, disability_with
            y.append(row[2])   # Target: specialities

        return np.array(X), np.array(y)

    def train_model(self, X, y):
        # Train clustering model
        self.kmeans = KMeans(n_clusters=3)  # Assuming 3 clusters
        self.kmeans.fit(X)

        # Train K-nearest neighbors model
        self.knn = KNeighborsClassifier(n_neighbors=3)
        self.knn.fit(X, y)

        # Train Bayesian neural network
        self.nb = GaussianNB()
        self.nb.fit(X, y)

    def predict_doctor(self, user_input):
        # Assume user_input is a tuple (disability_related_to, disability_with)
        cluster_label = self.kmeans.predict([user_input])[0]

        # Fetch doctors belonging to the predicted cluster
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, specialities FROM doctors WHERE cluster_label = %s", (cluster_label,))
        doctors_data = cursor.fetchall()
        cursor.close()
        conn.close()

        # Predict using K-nearest neighbors
        knn_prediction = self.knn.predict([user_input])

        # Predict using Bayesian neural network
        nb_prediction = self.nb.predict([user_input])

        return {
            "cluster_label": cluster_label,
            "doctors_in_cluster": doctors_data,
            "knn_prediction": knn_prediction[0],
            "nb_prediction": nb_prediction[0]
        }
