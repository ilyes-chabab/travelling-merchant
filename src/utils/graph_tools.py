import pandas as pd
import numpy as np
from .haversine import haversine

def load_cities(path):
    """Charge le CSV et retourne une liste de dictionnaires {city, lat, lon}"""
    df = pd.read_csv(path)
    return df.to_dict(orient="records")

def build_distance_matrix(cities):
    """Construit la matrice NxN des distances Haversine"""
    n = len(cities)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine(cities[i]["Latitude"], cities[i]["Longitude"],
                                         cities[j]["Latitude"], cities[j]["Longitude"])
    return matrix