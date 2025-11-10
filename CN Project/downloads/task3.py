def find_shortest_tour():
    distances = {
        'A': {'B': 10, 'C': 15},
        'B': {'A': 10, 'C': 20, 'D': 25},
        'C': {'A': 15, 'B': 20, 'D': 30, 'E': 35},
        'D': {'B': 25, 'C': 30, 'E': 20, 'F': 15},
        'E': {'C': 35, 'D': 20, 'F': 40, 'G': 30},
        'F': {'D': 15, 'E': 40, 'G': 10, 'H': 20},
        'G': {'E': 30, 'F': 10, 'H': 25, 'I': 35},
        'H': {'F': 20, 'G': 25, 'I': 15, 'J': 40},
        'I': {'G': 35, 'H': 15, 'J': 30},
        'J': {'H': 40, 'I': 30}
    }

    cities = list(distances.keys())
    print("Cities to visit:", " ".join(cities))

    visited = []
    current_city = 'A'  
    visited.append(current_city)
    total_distance = 0

    print("\nFinding shortest route...")

    while len(visited) < len(cities):
        nearest_city = None
        shortest_distance = float('inf')

        for city, dist in distances[current_city].items():
            if city not in visited and dist < shortest_distance:
                shortest_distance = dist
                nearest_city = city

        if nearest_city:
            visited.append(nearest_city)
            total_distance += shortest_distance
            current_city = nearest_city
        else:
            break

    if len(visited) == len(cities):
        total_distance += distances[current_city]['A']
        visited.append('A')

    print("\nBest route found:")
    print(" -> ".join(visited))
    print("Total distance:", total_distance, "miles")
    
    hours = total_distance / 50
    print("Travel time:", round(hours, 1), "hours")

find_shortest_tour()