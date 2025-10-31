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

    # n = le nombre de ville et g = graphe non orienté 
    n = len(distance_matrix)
    G = nx.Graph()

    # Construire le graphe complet pondéré en metant le poids ( distance )
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=distance_matrix[i][j])

    # Arbre couvrant minimal (MST) (le mst cherche le chemin avec le moins de poids(distance))
    mst = nx.minimum_spanning_tree(G)

    # Sommets de degré impair 
    odd_nodes = [v for v, d in mst.degree() if d % 2 == 1]

    # Appairage parfait minimum entre les sommets impairs 
    subgraph = G.subgraph(odd_nodes)
    matching = nx.algorithms.matching.min_weight_matching(subgraph)

    # Combinaison MST + appairage (graphe eulérien) 
    multi_graph = nx.MultiGraph(mst)
    multi_graph.add_edges_from(list(matching))

    # Circuit eulérien 
    euler_circuit = list(nx.eulerian_circuit(multi_graph))

    # Transformer en chemin hamiltonien (on saute les doublons) 
    path = []
    visited = set()
    for u, v in euler_circuit:
        if u not in visited:
            path.append(u)
            visited.add(u)
    path.append(path[0])  # revenir à la ville de départ

    # Distance totale 
    total_distance = sum(distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

    return path, total_distance



