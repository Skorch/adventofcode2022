# detects a start-of-packet marker in the datastream
# the start of a packet is indicated by a sequence of four characters that are all different
# subroutine needs to identify the first position where the four most recently received characters were all different
# it needs to report the number of characters from the beginning of the buffer to the end of the first such four-character marker

# How many characters need to be processed before the first start-of-packet marker is detected


def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield (ix, line)

def buffer_marker_position(input, buffer_size):
    buffer = []
    for ix, letter in enumerate(input):
        buffer.append(letter)
        if len(buffer) > buffer_size:
            _ = buffer.pop(0)
            if len(set(buffer)) == buffer_size:
                return ix + 1
             

def main(filename):
    for ix, line in read_file(filename):
        result = buffer_marker_position(line, 4)
        print(f"{ix} {line} {result}")
       
if __name__ == "__main__":
    # main("test.input")
    main("question.input")