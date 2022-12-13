import logging
import astar2
import string 
import math

DRAW = False
DEBUG = False

input_file = "test.input" if DEBUG else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield (list(line))

def height_from_letter(letter):
    
    if letter == 'S':
        return 0
    elif letter == 'E':
        return 25
    else:
        return string.ascii_lowercase.index(letter)



class Maze(astar2.AStar):
    
    def __init__(self, maze) -> None:
        
        self.maze = maze
        self.maze_height = len(maze)
        self.maze_width = len(maze[0])
        self.adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    def neighbors(self, node):

        node_letter = self.maze[node[0]][node[1]]
        node_height = height_from_letter(node_letter)
        children = []
        for adj_row, adj_col in self.adjacent_squares: # Adjacent squares            

            # Get node position
            adj_position = (node[0] + adj_row, node[1] + adj_col)

            # Make sure within range
            if adj_position[0] > (self.maze_height - 1) or adj_position[0] < 0 or adj_position[1] > (self.maze_width -1) or adj_position[1] < 0:
                continue

            adj_letter = self.maze[adj_position[0]][adj_position[1]]
            adj_height = height_from_letter(adj_letter)

            # print(f"{current_node.height} {new_node.height - 1}")
            if node_height < (adj_height - 1):
                continue
            
            children.append(adj_position)
            
        return children
                    
    
    def distance_between(self, n1, n2) -> float:
        return 1
    
    def heuristic_cost_estimate(self, current, goal) -> float:
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = current
        (x2, y2) = goal
        return math.hypot(x2 - x1, y2 - y1)
        
    
    

def main(filename):
    
    maze = list(read_file(filename))
        
    for ix, line in enumerate(maze):
        logging.debug(f"{line}")
        start_index = line.index("S") if "S" in line else -1        
        if start_index >= 0:
            start_position = (ix, start_index) # (start_index, ix)
            
        target_index = line.index("E") if "E" in line else -1
        if target_index >= 0:
            end_position = (ix, target_index) # (target_index, ix)
       
    print(f"start: {start_position} - end: {end_position}")
    

    astar_maze = Maze(maze)
    
    
    final_path = list(astar_maze.astar(start_position, end_position))
    
    # print(list(final_path))


    print(f"maze result: {len(final_path)-1}")

    print_path(maze, final_path)
    
def print_path(maze, final_path):
    rows = len(maze)
    cols = len(maze[0])
    adjacent_squares = {
        (0, -1): "<",
        (0, 1): ">", 
        (-1, 0): "^", 
        (1, 0): "v"
    }

    
    for row in range(rows):
        row_text = []
        for col in range(cols):
            pos = (row, col)
            if pos in final_path:
                path_index = final_path.index(pos)
                if path_index < len(final_path) - 1:
                    next_val = final_path[path_index+1]
                    difference = tuple(map(lambda i, j: i - j, next_val, pos))
                    # print(f"{val} -> {next_val} = {difference} {adjacent_squares[difference]}")                    
                    row_text.append(adjacent_squares[difference])
                else:
                    row_text.append("E")
            else:            
                row_text.append(".")
        print(''.join(row_text))

        
        
   
    
if __name__ == "__main__":
    main(input_file)
    # main("question.input")