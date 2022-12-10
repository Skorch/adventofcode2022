import copy
import logging


DEBUG = False
input_file = "test.input" if DEBUG else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.DEBUG)

# initial state:
# 5x5 grid
# for simplicity sake, ignore origin as (0,0)?
# origin = (0,4)


grid = [[" "]*6 for _ in range(5)]
origin = (4,0)
head_pos = origin
tail_pos = origin
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
    
    if not DEBUG:
        return
    
    logging.debug(f"head position {head_pos}")

    output_grid = copy.deepcopy(grid)
    output_grid[origin[0]][origin[1]] = "s"
    output_grid[tail_pos[0]][tail_pos[1]] = "T"
    output_grid[head_pos[0]][head_pos[1]] = "H"
    for row in output_grid:
        logging.debug(row)
    
    # for row in range(0, len(grid)):
    #     column = grid[row]        
    #     for col in range(0, len(column)):
            
    #     print(grid_output)
            




def main(filename):
    global head_pos, tail_pos, tail_movements
    
    draw_grid()
    tail_movements.add(tail_pos)
   
    logging.debug("-===============-")
    
    for ix, move_direction, move_length in read_file(filename):
        logging.debug(f"{ix} {move_direction} {move_length}")
        
        for _ in range(1, move_length + 1):
            
            if move_direction == "L":
                head_pos = (head_pos[0], head_pos[1] - 1)
            elif move_direction == "R":
                head_pos = (head_pos[0], head_pos[1] + 1)
            elif move_direction == "D":
                head_pos = (head_pos[0] + 1, head_pos[1])
            elif move_direction == "U":
                head_pos = (head_pos[0] - 1, head_pos[1])
            else:
                logging.error(f"Invalid move {move_direction}")

            draw_grid()
            
            if head_pos[0] - tail_pos[0] > 1:
                tail_move_len = head_pos[0] - 1
                logging.debug(f"tail needs to move down {tail_move_len}")
                tail_pos = (tail_move_len, head_pos[1])
                tail_movements.add(tail_pos)
            elif tail_pos[0] - head_pos[0] > 1:
                tail_move_len = head_pos[0] + 1
                logging.debug(f"tail needs to move up {tail_move_len}")
                tail_pos = (tail_move_len, head_pos[1])
                tail_movements.add(tail_pos)
            if head_pos[1] - tail_pos[1] > 1:
                tail_move_len = head_pos[1] - 1
                logging.debug(f"tail needs to move right {tail_move_len}")
                tail_pos = (head_pos[0], tail_move_len)
                tail_movements.add(tail_pos)
            elif tail_pos[1] - head_pos[1] > 1:
                tail_move_len = head_pos[1] + 1
                logging.debug(f"tail needs to move left {tail_move_len}")
                tail_pos = (head_pos[0], tail_move_len)
                tail_movements.add(tail_pos)
            
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