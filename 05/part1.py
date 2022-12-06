import re

def read_state(filename):
    
    with open(filename) as f:
        
        states = {}

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                states[str(ix+1)] = line.split(",")

        return states

def read_input(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                print(line)
                result = re.search(r"^move (\b\d+) from (\b\d+) to (\b\d+)$", line)
                move_total = int(result.groups(1)[0])
                source_bucket = result.groups(1)[1]
                destination_bucket = result.groups(0)[2]
                yield (ix, move_total, source_bucket, destination_bucket)


def main(filename, statefile):
    states = read_state(statefile)
    print(states)
    for ix, move_total, source_bucket, destination_bucket in read_input(filename):
        print(f"{ix} {move_total}, {source_bucket}, {destination_bucket}")
        
        
        for move_index in range(0, move_total):
            source_state_orig = states[source_bucket]
            source_state = states[source_bucket]
            dest_state = states[destination_bucket]
            source_val = source_state.pop(0)
            print(f"{ix} move {move_index} -> {source_val} from {source_bucket}:{source_state_orig} to {destination_bucket}:{dest_state} ")
            dest_state.insert(0,source_val)
            states[source_bucket] = source_state
            states[destination_bucket] = dest_state            
        
    print(states)
    result = ""
    for ix in states:
        result += states[ix].pop(0)
    
    print(result)
    
if __name__ == "__main__":
    # main("test.input", "test.state")
    main("question.input", "question.state")
