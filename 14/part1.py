import logging
from collections import namedtuple
import numpy as np
import pandas as pd
Point = namedtuple("Point", "x y")


PROD = True
DEBUG = False

input_file = "test.input" if not PROD else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                path = [Point(int(p.split(',')[0]), int(p.split(',')[1])) for p in line.split(" -> ")]
                yield path


def draw_cave(cave):
    for row in cave:
        for col in row:
            
            logging.debug(f"")

def build_cave(paths):
    cave = pd.DataFrame()


    for path in paths:
        logging.debug(f"{path}")
        
        for point_index in range(len(path)-1):
            point1 = path[point_index]
            point2 = path[point_index+1]
            
            dx_start = min(point1.x, point2.x)
            dx_end = max(point1.x, point2.x)
            dy_start = min(point1.y, point2.y)
            dy_end = max(point1.y, point2.y)
            
            
            
            for dx in range(dx_start, dx_end + 1):
                # if not str(dx) in cave.columns:
                    # cave[str(dx)] = "."
                
                for dy in range(dy_start, dy_end + 1):
                    logging.debug(f"dx,dy {dx},{dy}")                    
                    cave.at[dy, dx] = "#"

    
    for x in range(cave.index.max()):
        if not x in cave.index:
            cave.at[x,:] = "."

    cave.at[:,cave.columns.max()+1] = "."
    cave.at[:,cave.columns.min()-1] = "."
    cave.at[cave.index.max()+1,:] = "^"
    
    
    cave = cave.fillna(".")
    cave = cave.reindex(sorted(cave.columns), axis=1)
    # print(f"index {cave.sort_index()}")
    cave = cave.sort_index(axis=0)
    
    
    # cave = cave.reindex(sorted(cave), axis=1)
    return cave

def value_at(position, cave):
    return cave.at[position.y, position.x]

def move_sand(sand_position, cave):
    
    position_down = Point(sand_position.x, sand_position.y + 1)
    position_left = Point(sand_position.x-1, sand_position.y + 1)
    position_right = Point(sand_position.x+1, sand_position.y + 1)
    down_value = value_at(position_down, cave)
    if down_value in('.', '^'):
        return position_down
    if down_value in('o', '#') and value_at(position_left, cave) in('.', '^'):
        return position_left
    if down_value in('o', '#') and value_at(position_right, cave) in('.', '^'):
        return position_right    
    return None


def main(filename):
    
    starting_point = Point(500, 0)
    
    path_walls = []
    paths = list(read_file(filename))
    cave = build_cave(paths)
    logging.debug(cave)

    sand_ix = 0
    sand_dropping = False
    sand_position = None
    while True:

        if not sand_dropping:
            sand_ix += 1
            sand_position = starting_point


        new_sand_position = move_sand(sand_position, cave)
        if new_sand_position:
            
            if value_at(new_sand_position, cave) in ('^'):
                logging.info(f"done after {sand_ix-1} drops")
                break
            
            sand_dropping = True
            cave.at[sand_position.y, sand_position.x] = "."
            cave.at[new_sand_position.y, new_sand_position.x] = "o"
            sand_position = new_sand_position
        else:
            sand_dropping = False
        
        
        logging.debug(cave) 
                
    
    
if __name__ == "__main__":
    main(input_file)

# 1016