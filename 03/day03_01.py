import string

def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield (ix, line)

def main(input):
    
    score = 0
    
    for ix, rucksack in read_file(input):
        print(f"row {ix}")
        split_index = int(len(rucksack) / 2)
        
        compartment1 = rucksack[0:split_index]
        compartment2 = rucksack[split_index:]
        print(f"{len(rucksack)} {len(compartment1) + len(compartment2)} - {compartment1} | {compartment2}")
        set1 = set(compartment1)
        set2 = set(compartment2)
        
        intersection = list(set1.intersection(set2))[0]
        print(f"{intersection}")

        if intersection.islower():    

            index_value = string.ascii_lowercase.index(intersection)
            score += index_value + 1

        elif intersection.isupper():        
            
            index_value = string.ascii_uppercase.index(intersection)
            score += index_value + 1 + 26
        else:
            print("not found")
        # if intersection[0].isupper():
        #     score += 
        
        print(f"{score}")
    
    # print(components)
       
if __name__ == "__main__":
    main("day03_01.input")