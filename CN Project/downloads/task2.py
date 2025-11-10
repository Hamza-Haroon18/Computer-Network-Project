def calculate_island_perimeter():
    island = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    
    print("Original Island Map:")
    for row in island:
        print(" ".join(str(cell) for cell in row))
    print()
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    total_perimeter = 0
    land_cells = 0
    
    for row in range(len(island)):
        for col in range(len(island[0])):
            if island[row][col] == 1:  
                land_cells += 1
                water_neighbors = 0
                
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    
                    if (new_row < 0 or new_row >= len(island) or \
                       (new_col < 0 or new_col >= len(island[0])) or \
                       island[new_row][new_col] == 0):
                        water_neighbors += 1
                
                total_perimeter += water_neighbors
    
    print(f"Number of land cells: {land_cells}")
    print(f"Total perimeter length: {total_perimeter} units")
    
    if land_cells > 0:
        erosion_risk = total_perimeter / land_cells
        print(f"Erosion risk factor: {erosion_risk:.2f} (higher means more risk)")
    else:
        print("No land remaining - island has completely eroded!")

calculate_island_perimeter()