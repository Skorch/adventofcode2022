import logging

DRAW = False
DEBUG = False

input_file = "test.complex.input" if DEBUG else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

register = 1
command_queue = []

def read_file(filename):
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            if line:
                result = line.split(" ")
                command = result[0]
                arg = result[1] if len(result) > 1 else None
                yield (ix, command, arg)

def add_numer(number):
    global register
    register += int(number)
    
def noop(arg):
    pass

def main(filename):
    
    commands = read_file(filename)
    command_countdown = -1
    cycle = 0
    get_command = True
    
    signals = []
    
    while True:
        
        
        if command_countdown == 0 and exec_command:
            exec_command(arg)
            get_command = True

        if get_command:            
            
            ix, command, arg = next(commands, (-1, None, None))
            logging.debug(f"getting next command: {command} {arg}")

            if not command:
                logging.debug("no more input")
                break
            elif command == "addx":
                exec_command = add_numer
                command_countdown = 2
            elif command == "noop":
                exec_command = noop
                command_countdown = 1
            else:
                raise Exception(f"invalid command {command}")
            
            get_command = False

        cycle += 1
        command_countdown -= 1
        
        if cycle in (20, 60, 100, 140, 180, 220):
            signals.append(cycle * register)
            logging.info(f"cycle {cycle} register {register} = {cycle * register}")
       
    logging.info(f"register: {register} after {cycle} cycles = {sum(signals)}")
if __name__ == "__main__":
    main(input_file)
    # main("question.input")