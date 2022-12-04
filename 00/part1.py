
def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield (ix, line)

def main(filename):
    for ix, line in read_file(filename):
        print(f"{ix} {line}")
       
if __name__ == "__main__":
    main("test.input")
    # main("question.input")