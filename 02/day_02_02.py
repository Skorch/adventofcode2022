
ROCK = 1
PAPER = 2
SCICORS = 3

winning_rules = {
    ROCK: PAPER,
    PAPER: SCICORS,
    SCICORS: ROCK
}

losing_rules = {
    ROCK: SCICORS,
    PAPER: ROCK,
    SCICORS: PAPER
}

op_moves = {
    "A": ROCK,
    "B": PAPER,
    "C": SCICORS,
}



scores = {
    ROCK: 1,
    PAPER: 2,
    SCICORS: 3
    
}

WIN = 6
DRAW = 3
LOSE = 0

def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                line_values = line.split(" ")
                yield (ix, line_values[0], line_values[1])


def move_for_result(op_move, desired_result):
    if desired_result == "X":
        return losing_rules[op_move]
    elif desired_result == "Z":
        return winning_rules[op_move]
    else:
        return op_move
    
def score_move(opponent_move, your_move):
    if your_move == opponent_move:
        print(f"draw {opponent_move} == {your_move}")
        return your_move + DRAW
    elif winning_rules[opponent_move] == your_move:
        print(f"win {opponent_move} < {your_move}")
        
        return your_move + WIN
    else:
        print(f"lose {opponent_move} > {your_move}")
        return your_move + LOSE


def main():
    
    moves = read_file("day02_01.input")
    score = 0
    for ix, op_move_encoded, desired_result in moves:
        op_move = op_moves[op_move_encoded]
        your_move = move_for_result(op_move, desired_result)
        new_score = score_move(op_move, your_move)
        print(new_score)
        score += new_score
        
    print(f"final score: {score} after {ix+1} moves")
    
if __name__ == "__main__":
    main()