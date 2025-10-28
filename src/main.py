from utils.graph_tools import load_cities, build_distance_matrix
from algo.christofides import christofides_tsp
from algo.genetic_tsp import genetic_tsp

def main():
    # -------------------------
    # 1️⃣ Chargement des villes
    # -------------------------
    csv_path = "data/villes_france_lat_long.csv"
    print("Chargement des villes depuis :", csv_path)
    cities = load_cities(csv_path)
    print(f"{len(cities)} villes chargées.")

    # -------------------------
    # 2️⃣ Construction de la matrice de distances Haversine
    # -------------------------
    print("Calcul de la matrice de distances Haversine...")
    distance_matrix = build_distance_matrix(cities)
    print("Matrice de distances construite.")

    # -------------------------
    # 3️⃣ Résolution TSP : Christofides
    # -------------------------
    print("\n=== Algorithme de Christofides ===")
    path_c, dist_c = christofides_tsp(distance_matrix)
    print("Chemin Christofides :", path_c)
    print(f"Distance totale Christofides : {dist_c:.2f} km")

    # -------------------------
    # 4️⃣ Résolution TSP : Algorithme génétique
    # -------------------------
    print("\n=== Algorithme Génétique ===")
    path_g, dist_g = genetic_tsp(
        distance_matrix,
        pop_size=100,
        generations=500,
        mutation_rate=0.05
    )
    print("Chemin Génétique :", path_g)
    print(f"Distance totale Génétique : {dist_g:.2f} km")

    # -------------------------
    # 5️⃣ Comparaison rapide
    # -------------------------
    print("\n=== Comparaison des méthodes ===")
    print(f"Christofides : {dist_c:.2f} km")
    print(f"Génétique    : {dist_g:.2f} km")

if __name__ == "__main__":
    main()
