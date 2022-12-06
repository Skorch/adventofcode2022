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

def start_of_packet(input):
    buffer = []
    for ix, letter in enumerate(input):
        buffer.append(letter)
        if len(buffer) > 4:
            _ = buffer.pop(0)
            if len(set(buffer)) == 4:
                return ix + 1
            
def start_of_message(input):
    buffer = []
    for ix, letter in enumerate(input):
        buffer.append(letter)
        if len(buffer) > 14:
            _ = buffer.pop(0)
            if len(set(buffer)) == 14:
                return ix + 1
            
def main(filename):
    for ix, line in read_file(filename):
        packet_index = start_of_message(line)
        print(f"{ix} {line} {packet_index}")
       
if __name__ == "__main__":
    # main("test.input")
    main("question.input")