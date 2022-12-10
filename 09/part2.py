import copy
import logging
import math

DRAW = False
DEBUG = False
input_file = "test.input" if DEBUG else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

# initial state:
# 5x5 grid
# for simplicity sake, ignore origin as (0,0)?
# origin = (0,4)


grid = [[" "]*6 for _ in range(5)]
origin = (4,0)
head_pos = origin
# tail_pos = origin
tail_movements = set()



def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                move = line.split(" ")
                move_direction = move[0]
                move_length = int(move[1])
                yield (ix, move_direction, move_length)


def draw_grid():
    global grid
    
    if not DRAW:
        return
    
    logging.debug(f"head position {head_pos}")

    output_grid = copy.deepcopy(grid)
    output_grid[origin[0]][origin[1]] = "s"
    for ix, knot in enumerate(knots):
        if output_grid[knot[0]][knot[1]] in(' ', 's'):
            output_grid[knot[0]][knot[1]] = f"{ix+1}"
    output_grid[head_pos[0]][head_pos[1]] = "H"
    for row in output_grid:
        logging.debug(row)
    

knots = [origin]*9

def move(position, move_direction):
    if not move_direction:
        return position
    
    new_position = None
    if move_direction == "L":
        new_position = (position[0], position[1] - 1)
    elif move_direction == "R":
        new_position = (position[0], position[1] + 1)
    elif move_direction == "D":
        new_position = (position[0] + 1, position[1])
    elif move_direction == "U":
        new_position = (position[0] - 1, position[1])
    elif move_direction == "UL":
        new_position = (position[0] - 1, position[1] - 1)
    elif move_direction == "UR":
        new_position = (position[0] - 1, position[1] + 1)
    elif move_direction == "DL":
        new_position = (position[0] + 1, position[1] - 1)
    elif move_direction == "DR":
        new_position = (position[0] + 1, position[1] + 1)
        
    else:
        logging.error(f"Invalid move {move_direction}")    

    return new_position

def main(filename):
    global head_pos, knots, tail_movements
    
    draw_grid()

    # tail_movements.add(tail_pos)
   
    logging.debug("-===============-")
    
    for ix, move_direction, move_length in read_file(filename):
        logging.debug(f"{ix} {move_direction} {move_length}")
        
        for _ in range(1, move_length + 1):
            
            new_position = move(head_pos, move_direction)

            head_pos = new_position

            draw_grid()
            
            head_knot = head_pos
            
            for knot_number, knot in enumerate(knots):
                
                # 0 + = right
                # 0 - = left
                # + 0 = down
                # - 0 = up

                # + + = down right
                # + - = down left
                # - + = up right
                # - - = up left
                
                dy = head_knot[0] - knot[0]
                dx = head_knot[1] - knot[1]
                dist = math.hypot(dx, dy)
                if abs(dy) > 1 or abs(dx) > 1:
                    if dy == 0 and dx >= 1:
                        new_move = "R"
                    elif dy == 0 and dx <= -1:
                        new_move = "L"
                    elif dy >= 1 and dx == 0:
                        new_move = "D"
                    elif dy <= -1 and dx == 0:
                        new_move = "U"
                    elif dy >= 1 and dx >= 1:
                        new_move = "DR"
                    elif dy >= 1 and dx <= -1:
                        new_move = "DL"
                    elif dy <= -1 and dx >= 1:
                        new_move = "UR"
                    elif dy <= -1 and dx <= -1:
                        new_move = "UL"
                else:
                    new_move = None

                logging.debug(f"dy {dy} dx {dx} [{dist}]- knot {knot_number+1} should move {new_move}")
                
                # was the move on one of the same axis?
                straight = (head_knot[0] == knot[0] or head_knot[1] == knot[1])
            
                knot = move(knot, new_move)                                

                
                knots[knot_number] = knot

                head_knot = knot
            tail_movements.add(knot)
            draw_grid()
        logging.debug("-===============-")
        

    if DEBUG:
        logging.info(f"tail_movements [{len(tail_movements)}] = {(tail_movements)}")
    else:
        logging.info(f"tail_movements [{len(tail_movements)}]")
    # print(grid)
       
if __name__ == "__main__":
    main(input_file)
    # main("question.input")