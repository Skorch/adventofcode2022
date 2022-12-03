import string

def read_file(filename):
    
    elf1 = None
    elf2 = None
    elf3 = None
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            print(f" {ix} {line}")
            if ix % 3 == 0:
                elf1 = line
            if ix % 3 == 1:
                elf2 = line
            if ix % 3 == 2:
                elf3 = line
                yield (ix, elf1, elf2, elf3)

def main(input):
    
    score = 0
    
    for ix, elf1, elf2, elf3 in read_file(input):
        print(f"row {ix} {elf1} {elf2} {elf3}")
        
    
        set1 = set(elf1)
        set2 = set(elf2)
        set3 = set(elf3)
        
        intersection = list(set1.intersection(set2).intersection(set3))[0]
        print(f"{intersection}")

        if intersection.islower():    

            index_value = string.ascii_lowercase.index(intersection)
            score += index_value + 1

        elif intersection.isupper():        
            
            index_value = string.ascii_uppercase.index(intersection)
            score += index_value + 1 + 26
        else:
            print("not found")
        
        print(f"{score}")
    
       
if __name__ == "__main__":
    main("day03_01.input")