import networkx as nx
import numpy as np

def christofides_tsp(distance_matrix):
    """
    Résout le TSP à l'aide de l'algorithme de Christofides.
    distance_matrix : numpy array NxN (symétrique, respecte l’inégalité triangulaire)
    
    Retour :
        best_path : chemin hamiltonien approximé
        total_distance : distance totale
    """
    n = len(distance_matrix)
    G = nx.Graph()

    # --- 1️⃣ Construire le graphe complet pondéré ---
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=distance_matrix[i][j])

    # --- 2️⃣ Arbre couvrant minimal (MST) ---
    mst = nx.minimum_spanning_tree(G)

    # --- 3️⃣ Sommets de degré impair ---
    odd_nodes = [v for v, d in mst.degree() if d % 2 == 1]

    # --- 4️⃣ Appairage parfait minimum entre les sommets impairs ---
    subgraph = G.subgraph(odd_nodes)
    matching = nx.algorithms.matching.min_weight_matching(subgraph)

    # --- 5️⃣ Combinaison MST + appairage (graphe eulérien) ---
    multi_graph = nx.MultiGraph(mst)
    multi_graph.add_edges_from(list(matching))

    # --- 6️⃣ Circuit eulérien ---
    euler_circuit = list(nx.eulerian_circuit(multi_graph))

    # --- 7️⃣ Transformer en chemin hamiltonien (on saute les doublons) ---
    path = []
    visited = set()
    for u, v in euler_circuit:
        if u not in visited:
            path.append(u)
            visited.add(u)
    path.append(path[0])  # revenir à la ville de départ

    # --- 8️⃣ Distance totale ---
    total_distance = sum(distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

    return path, total_distance


# ------------------------- #
# Exemple de test
# ------------------------- #
if __name__ == "__main__":
    from utils.graph_tools import load_cities, build_distance_matrix

    cities = load_cities("data/villes_france_lat_long.csv")
    distance_matrix = build_distance_matrix(cities)

    path, dist_tot = christofides_tsp(distance_matrix)
    print("Chemin approximé (Christofides) :", path)
    print("Distance totale :", dist_tot)
