
def min_max_parts(group):
    parts = group.split("-")
    return (int(parts[0]), int(parts[1]))

def read_file(filename):
    
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                groups = line.split(",")
                
                group1_min, group1_max = min_max_parts(groups[0])
                group2_min, group2_max = min_max_parts(groups[1])
                
                yield (ix, group1_min, group1_max, group2_min, group2_max)

def main(filename):
    
    total = 0
    for ix, group1_min, group1_max, group2_min, group2_max in read_file(filename):
        print(f"{ix} {group1_min} - {group1_max} {group2_min} - {group2_max}")

        if group1_min <= group2_min <= group1_max:
            print("group 2 min in 1a")
            total += 1
        elif group1_min <= group2_max <= group1_max:
            print("group 2 max in 1b")
            total += 1
        elif group2_min <= group1_min <= group2_max:
            print("group 1 contained in 2a")
            total += 1
        elif group2_min <= group1_max <= group2_max:
            print("group 1 contained in 2b")
            total += 1
        
        
    print(total)
       
if __name__ == "__main__":
    main("question.input")
    # main("test.input")