from utils.graph_tools import load_cities, build_distance_matrix
from algo.christofides import christofides_tsp
from algo.genetic_tsp import genetic_tsp
from visualisation_pygame import TSPVisualizer
import time
import psutil
import os

def get_memory_mb():
    """Retourne la mémoire utilisée (en Mo) par le processus courant."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

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
    mem_before = get_memory_mb()
    start = time.time()
    path_c, dist_c = christofides_tsp(distance_matrix)
    exec_time_christofides = time.time() - start
    mem_after = get_memory_mb()
    mem_usage_christofides = mem_after - mem_before

    print("Chemin Christofides :", path_c)
    print(f"Distance totale Christofides : {dist_c:.2f} km")
    print(f"Temps : {exec_time_christofides:.3f}s |  Mémoire : +{mem_usage_christofides:.2f} Mo")


    # -------------------------
    # 4️⃣ Résolution TSP : Algorithme génétique
    # -------------------------
    print("\n=== Algorithme Génétique ===")
    mem_before = get_memory_mb()    
    start = time.time()
    path_g, dist_g = genetic_tsp(
        distance_matrix,
        pop_size=100,
        generations=500,
        mutation_rate=0.05
    )
    exec_time_genetic = time.time() - start
    mem_after = get_memory_mb()
    mem_usage_genetic = mem_after - mem_before
    print("Chemin Génétique :", path_g)
    print(f"Distance totale Génétique : {dist_g:.2f} km")
    print(f"Temps : {exec_time_genetic:.3f}s | Mémoire : +{mem_usage_genetic:.2f} Mo")

    # -------------------------
    # 5️⃣ Comparaison rapide
    # -------------------------
    print("\n=== Comparaison des méthodes ===")
    print(f"Christofides : {dist_c:.2f} km")
    print(f"Génétique    : {dist_g:.2f} km")

    visualizer = TSPVisualizer(
    cities,
    path_c, path_g,
    dist_c, dist_g,
    exec_time_christofides, exec_time_genetic,
    mem_usage_christofides, mem_usage_genetic
    )
    visualizer.run()

if __name__ == "__main__":
    main()
