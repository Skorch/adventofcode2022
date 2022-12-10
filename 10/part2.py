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
    exec_command = None
    crt_output = []
    crt_row = []
    
    signals = []
    
    while True:
        
        cycle += 1
        
        logging.debug(f"starting cycle {cycle}")

        if not exec_command:            
            
            ix, command, arg = next(commands, (-1, None, None))
            # logging.debug(f"getting next command: {command} {arg}")

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

            logging.debug(f"beginning executing {command} {arg}")


        command_countdown -= 1
        
        
        sprite_output = ['.']*38
        sprite_output[register-1:register+1] = "###"
        crt_cycle_position = cycle % 40 - 1
        
        logging.debug(f"crt draws pixel in position {crt_cycle_position}")
        logging.debug(f"sprite position{''.join(sprite_output)}")
        crt_row.append(sprite_output[crt_cycle_position])
        logging.debug(f"Current CRT Row: {''.join(crt_row)}")
        
        if cycle %40 ==0:
            crt_output.append(crt_row)
            crt_row = []
            logging.debug(f"new crt row after cycle {cycle}")


        if command_countdown == 0:
            logging.debug(f"finishing executing {command} {arg}")
            exec_command(arg)
            exec_command = None
            

    for row in crt_output:
        logging.info(f"{''.join(row)}")
    logging.info(f"register: {register} after {cycle} cycles = {sum(signals)}")
if __name__ == "__main__":
    main(input_file)
    # main("question.input")