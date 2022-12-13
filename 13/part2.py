import logging
import json
from ast import literal_eval
import functools

DRAW = False
DEBUG = False
PROD = True

input_file = "test.input" if not PROD else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)


def read_file(filename):
    
    with open(filename) as f:
        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:                
                yield literal_eval(line)


EQ = 0
GT = 1
LT = -1

MARKER1 = [[2]]
MARKER2 = [[6]]

def compare(lhs, rhs):
    
    logging.debug(f"lhs {lhs} rhs {rhs}")

    if lhs == rhs:
        return EQ
    
    if type(lhs) is int:
        if type(rhs) is int:
            return LT if lhs < rhs else GT
        return compare([lhs], rhs)

    if type(rhs) is int:
        return compare(lhs, [rhs])
            
    if lhs and rhs:
        result = compare(lhs[0], rhs[0])
        
        return compare(lhs[1:], rhs[1:]) if result == EQ else result

    return LT if rhs else GT


def main(filename):

    lines = list(read_file(filename))
    lines += [MARKER1 , MARKER2]
    
    sorted_lines = sorted(lines, key=functools.cmp_to_key(compare) )
    
    print(f"{(sorted_lines.index(MARKER1)+1) * (sorted_lines.index(MARKER2)+1)}")

if __name__ == "__main__":
    main(input_file)
