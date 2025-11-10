import math
from collections import deque

def find_shortest_diagonal_path():
    grid_size = 5
    start = (1, 1)
    end = (4, 4)
    
    walls = {(0, 3), (3, 1), (3, 3)}  
    
    moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    visited = {}
    queue = deque()
    queue.append((start, [start]))
    visited[start] = True
    
    while queue:
        current_pos, path = queue.popleft()
        
        if current_pos == end:
            distance = 0.0
            for i in range(len(path)-1):
                dx = path[i+1][0] - path[i][0]
                dy = path[i+1][1] - path[i][1]
                distance += math.sqrt(dx**2 + dy**2)
            
            print("Robot's path found:")
            for step, pos in enumerate(path):
                print(f"Move {step}: Position {pos}")
            print(f"Total distance: {distance:.2f} units")
            return
        
        for move in moves:
            next_x = current_pos[0] + move[0]
            next_y = current_pos[1] + move[1]
            next_pos = (next_x, next_y)
            
            if (0 <= next_x < grid_size and 
                0 <= next_y < grid_size and 
                next_pos not in walls and 
                next_pos not in visited):
                
                visited[next_pos] = True
                new_path = path.copy()
                new_path.append(next_pos)
                queue.append((next_pos, new_path))
    
    print("No valid path found for the robot")

find_shortest_diagonal_path()