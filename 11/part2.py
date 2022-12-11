import logging
import re
from math import trunc
import random
import time
import primefac

DRAW = False
DEBUG = False
TEST_INPUT = False

input_file = "test.input" if TEST_INPUT else "question.input"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

def division_test(value, divisible_by):
    

    return value % divisible_by == 0
    

    # don't need any of the complex rules!!
        
    if divisible_by == 1:
        return True
    elif divisible_by in(2, 5):
        return int(str(value)[-1]) % divisible_by == 0
    elif divisible_by == 3:
        return sum([int(x) for x in str(value)]) % divisible_by == 0
    elif divisible_by in(7, 11):
        n = 1 if divisible_by == 11 else 3
        
        add = True
        result = 0
        str_value = str(value)
        for digit in [str_value[i:i+n] for i in range(0, len(str_value), n)]:
            result += int(digit) if add else -1*int(digit)
            add = not add
        return result == 0 or result % divisible_by == 0
    
    elif divisible_by in(13, 17, 19, 23):
        if divisible_by == 13:
            n = 4
        elif divisible_by == 17:
            n = 5
        elif divisible_by == 19:
            n = 2
        elif divisible_by == 23:
            n = 7
        
        digit_list = str(value).split()
        last_digit = int(digit_list.pop())
        new_value = value - last_digit*n
        return (new_value % divisible_by) == 0
    
    raise Exception(f"Invalid divisible by {divisible_by}")
        
def read_file(filename):
    
    monkey = None
    starting_items = None
    operation = None
    test = None
    test_true_condition = None
    test_false_condition = None
    
    
    with open(filename) as f:

        for ix, line in enumerate([l.rstrip() for l in f]):
            # print(line)
            if line:
                                
                monkey_re = re.match("^Monkey\\s(.*):$", line)
                starting_items_re = re.match("^\\s{2}Starting items: (.*)$", line)
                operation_re = re.match("^\\s{2}Operation: (.*)$", line)
                test_re = re.match("^\\s{2}Test: (.*)$", line)
                test_true_condition_re = re.match("^\\s{4}If true: (.*)$", line)
                test_false_condition_re = re.match("^\\s{4}If false: (.*)$", line)
                
                monkey = monkey_re.groups()[0] if monkey_re else monkey
                starting_items = starting_items_re.groups()[0].split(", ") if starting_items_re else starting_items
                operation = operation_re.groups()[0] if operation_re else operation
                test = test_re.groups()[0] if test_re else test
                test_true_condition = test_true_condition_re.groups()[0] if test_true_condition_re else test_true_condition
                test_false_condition = test_false_condition_re.groups()[0] if test_false_condition_re else test_false_condition
            # print(ix % 7)
            if ix % 7 == 6:

                # print((ix, monkey, starting_items, operation, test, test_true_condition, test_false_condition))
                yield (ix, monkey, starting_items, operation, test, test_true_condition, test_false_condition)
                monkey = None
                starting_items = None
                operation = None
                test = None
                test_true_condition = None
                test_false_condition = None

        yield (ix, monkey, starting_items, operation, test, test_true_condition, test_false_condition)


class Operation():
    def __init__(self, operation_text) -> None:
        self.text = operation_text
        re_result = re.findall("^new = (.*) ([\\+\\*]) (.*)$", operation_text)[0]
        # print(re_result)
        self.lhs = re_result[0]
        self.operator = re_result[1]
        self.rhs = re_result[2]
        
    def is_square(self):
        return self.lhs == "old" and self.rhs == "old" and self.operator == "*"
    def exec(self, old):
        lhs_value = old if self.lhs == "old" else int(self.lhs)
        rhs_value = old if self.rhs == "old" else int(self.rhs)
        if self.operator == "+":
            return lhs_value + rhs_value
        elif self.operator == "*":
            return lhs_value * rhs_value
        else:
            raise Exception(f"Invalid operator {self.operator}")

    def show(self):
        return f"{self.lhs} {self.operator} {self.rhs}"
class Test():
    def __init__(self, test_text, test_true_condition, test_false_condition) -> None:
        self.divisible_by = int(re.findall("^divisible by (\\d.*)$", test_text)[0])
        self.true_monkey = str(re.findall("^throw to monkey (\d.*)$", test_true_condition)[0])
        self.false_monkey = str(re.findall("^throw to monkey (\d.*)$", test_false_condition)[0])
        
    def test(self, value):

        return division_test(value, self.divisible_by)


    def throw_to(self, is_divisible):
        return self.true_monkey if is_divisible else self.false_monkey
    
    def show(self):
        return f"divisible by {self.divisible_by}\n....if true trow to {self.true_monkey}\n....if false throw to {self.false_monkey}"

class Monkey():
    

    def __init__(self, monkey_number, starting_items, operation, test, test_true_condition, test_false_condition) -> None:
        self.monkey_number = monkey_number
        self.inventory = [int(i) for i in starting_items]
        self.operation = Operation(operation)
        self.test = Test(test, test_true_condition, test_false_condition)
        self.inspections = 0
        
    def show_monkey(self):
        if DRAW:
            logging.info(f"\nMonkey {self.monkey_number}\n..Inventory {self.inventory}\n..Operation {self.operation.show()}\n..Test {self.test.show()}")

    def get_items(self):
        while len(self.inventory) > 0:
            self.inspections += 1
            yield self.inventory.pop(0)
        # return self.inventory.pop(0)
    
    def put_item(self, item):
        self.inventory.append(item)


last_perf_check = 0
perf_check_threshold = 0.03
def perf_check(op):
    global last_perf_check
    new_perf_check = time.perf_counter()
    
    # print(new_perf_check - last_perf_check)
    if new_perf_check - last_perf_check >= perf_check_threshold:
        logging.info(f" {op} took {new_perf_check - last_perf_check} seconds")
    
    last_perf_check = new_perf_check

def main(filename):
    
    monkeys = {}
    total_rounds = 10000
    for (ix, monkey_number, starting_items, operation, test, test_true_condition, test_false_condition) in read_file(filename):
        new_monkey = Monkey(monkey_number, starting_items, operation, test, test_true_condition, test_false_condition)
        monkeys[monkey_number] = new_monkey
        # print(f"adding {monkey_number} to {monkeys}")
        new_monkey.show_monkey()
        
    print(monkeys)
    
    cycle_length = 1
    for cycle in [monkeys[m].test.divisible_by for m in monkeys]:
        cycle_length *= cycle

    
    for round in range(total_rounds):
        perf_check("round start")
        logging.info(f"starting round {round + 1}")
        
        for monkey_ix in monkeys:
            monkey = monkeys[monkey_ix]
            for item in monkey.get_items():
                perf_check("get item")                

                logging.debug(f"Monkey {monkey.monkey_number}")
                logging.debug(f"  Monkey inspects an item with a worry level of {item}")
                worry = monkey.operation.exec(item)
                perf_check("operation exec")
                logging.debug(f"    Worry level is multiplied by {monkey.operation.show()} to {worry}")
                # worry = trunc(worry / 3)
                
                can_divide = monkey.test.test(worry)
                throw_to = monkey.test.throw_to(can_divide)
                
                logging.debug(f"    Monkey gets bored with item. Worry level is divided by 3 to {worry}")            
                logging.debug(f"    Current worry level is {can_divide} divisible by {monkey.test.divisible_by}")            

                perf_check(f"divisibility test {worry} / {monkey.test.divisible_by}")
                logging.debug(f"    Item with worry level {worry} is thrown to monkey {throw_to}.") 
                
                new_item = worry%cycle_length

                monkeys[throw_to].put_item(new_item)
                perf_check("put item")
           
        if DRAW: 
            logging.info(f"After round {round+1}, the monkeys are holding items with these worry levels:")
            for monkey_ix in monkeys:
                monkey = monkeys[monkey_ix]
                logging.info(f"Monkey {monkey.monkey_number}: {monkey.inventory}")
        
        
    inspections = []
    for monkey_ix in monkeys:
        monkey = monkeys[monkey_ix]
        inspections.append(monkey.inspections)
        logging.info(f"Monkey {monkey.monkey_number}: {monkey.inspections}")

    inspections.sort(reverse=True)
    logging.info(f"top inspections {inspections[0]} * {inspections[1]} = {inspections[0]*inspections[1]}")
    
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


from functools import reduce

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))    
if __name__ == "__main__":
    main(input_file)
