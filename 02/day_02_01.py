
ROCK = 1
PAPER = 2
SCICORS = 3

rules = {
    ROCK: SCICORS,
    PAPER: ROCK,
    SCICORS: PAPER
}

op_moves = {
    "A": ROCK,
    "B": PAPER,
    "C": SCICORS,
}

your_moves = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCICORS,
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
                op_move = op_moves[line_values[0]]
                your_move = your_moves[line_values[1]]
                yield (ix, op_move, your_move)


    
def score_move(opponent_move, your_move):
    if your_move == opponent_move:
        print(f"draw {opponent_move} == {your_move}")
        return your_move + DRAW
    elif rules[your_move] == opponent_move:
        print(f"win {opponent_move} < {your_move}")
        
        return your_move + WIN
    else:
        print(f"lose {opponent_move} > {your_move}")
        return your_move + LOSE


def main():
    
    moves = read_file("day02_01.input")
    score = 0
    for ix, op_move, your_move in moves:
        new_score = score_move(op_move, your_move)
        print(new_score)
        score += new_score
        
    print(f"final score: {score} after {ix+1} moves")
    
if __name__ == "__main__":
    main()