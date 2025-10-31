import random

def genetic_tsp(distance_matrix, pop_size=100, generations=50000, mutation_rate=0.05):
    """
    Résout le TSP par algorithme génétique.
    distance_matrix : numpy array NxN
    pop_size : taille de la population
    generations : nombre de générations
    mutation_rate : probabilité de mutation
    Retour :
        best_path : meilleur parcours trouvé
        best_distance : distance totale
    """
    n = len(distance_matrix)

    # --- Population initiale ---
    # Plein de listes aléatoires
    population = [random.sample(range(n), n) for _ in range(pop_size)]

    def fitness(path):
        """Distance totale d'un chemin"""
        return sum(distance_matrix[path[i]][path[i+1]] for i in range(n-1)) + distance_matrix[path[-1]][path[0]]

    # --- 2️⃣ Boucle de générations ---
    for gen in range(generations):
        # Calcul des fitness et tri
        scores = [(fitness(ind), ind) for ind in population]
        scores.sort(key=lambda x: x[0])  # plus petit score = meilleur

        # Garde les meilleurs 50%
        population = [ind for _, ind in scores[:pop_size//2]]

        # --- 3️⃣ Crossover ---
        # parent1 et parent2 → deux bons chemins sélectionnés.
        # On copie un segment de parent1 dans child.
        # Puis on remplit le reste avec les villes manquantes dans l’ordre de parent2.
        
        children = []
        while len(children) + len(population) < pop_size:
            parent1, parent2 = random.sample(population, 2)
            start, end = sorted(random.sample(range(n), 2))
            child = [-1]*n
            child[start:end] = parent1[start:end]
            pointer = 0
            for city in parent2:
                if city not in child:
                    while child[pointer] != -1:
                        pointer += 1
                    child[pointer] = city
            children.append(child)
        population += children
        
        
        #parent1 = [A, B, C, D, E, F]
        #parent2 = [C, D, F, E, B, A]
        #start, end = (2, 4)
        #→ child = [-1, -1, C, D, -1, -1]
        #→ on remplit avec parent2 sans répéter : [C, D, F, E, B, A]
        #→ child = [F, E, C, D, B, A]

        # --- 4️⃣ Mutation ---
        #échange 2 villes avec une proba 
        for ind in population:
            if random.random() < mutation_rate:
                i, j = random.sample(range(n), 2)
                ind[i], ind[j] = ind[j], ind[i]

    # --- 5️⃣ Meilleur individu ---
    best_path = min(population, key=fitness)
    best_distance = fitness(best_path)
    return best_path, best_distance


# -------------------------
# Test rapide avec graph_tools
# -------------------------
if __name__ == "__main__":
    from utils.graph_tools import load_cities, build_distance_matrix

    cities = load_cities("data/villes_france_lat_long.csv")
    distance_matrix = build_distance_matrix(cities)

    path, dist_tot = genetic_tsp(distance_matrix, pop_size=50, generations=200, mutation_rate=0.1)
    print("Meilleur chemin trouvé :", path)
    print("Distance totale :", dist_tot)
