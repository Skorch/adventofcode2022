import logging
import json
from ast import literal_eval

DRAW = False
DEBUG = False
PROD = True

input_file = "test.input" if not PROD else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)


def read_file(filename):
    
    with open(filename) as f:
        file_index = 1
        parsed = []
        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                
                # parsed.append(json.loads(line))
                parsed.append(literal_eval(line))
                
            else:
                yield (file_index, parsed)
                parsed = []
                file_index += 1


    yield (file_index, parsed)

def check_line(lhs, rhs):
    
    logging.debug(f"lhs {lhs} rhs {rhs}")

    if lhs == rhs:
        return None
    
    if type(lhs) is int:
        if type(rhs) is int:
            return lhs < rhs
        return check_line([lhs], rhs)

    if type(rhs) is int:
        return check_line(lhs, [rhs])
            
    if lhs and rhs:
        result = check_line(lhs[0], rhs[0])
        
        return check_line(lhs[1:], rhs[1:]) if result == None else result

    return True if rhs else False   


def main(filename):
    correct = []
    for ix, line in read_file(filename):
        l_list = line[0]
        r_list = line[1]        
        logging.debug(f"Signal {ix} -> {l_list} vs {r_list}")
        is_in_order = check_line(l_list, r_list)
        if is_in_order:
            correct.append(ix)
        
       
    logging.info(f"correct {correct} sum={sum(correct)}")
if __name__ == "__main__":
    main(input_file)
