import pandas as pd
# how many trees are visible from outside the grid?
#   X
# Y  01234
# ---------
# 0  30373
# 1  25512
# 2  65332
# 3  33549
# 4  35390

# In the example above, consider the middle 5 in the second row:

# Looking up, its view is not blocked; it can see 1 tree (of height 3).
# Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
# Looking right, its view is not blocked; it can see 2 trees.
# Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
# A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).


# However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

# Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
# Looking left, its view is not blocked; it can see 2 trees.
# Looking down, its view is also not blocked; it can see 1 tree.
# Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
# This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.


# What is the highest scenic score possible for any tree?


tree_reset = -1

def read_file(filename):
        
    with open(filename) as f:

        for _, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield [int(l) for l in line]
    

def line_of_sight_trees(trees, current_height):
    line_of_sight = []
    
    for ix, tree in enumerate(trees):
        if tree < current_height:
            line_of_sight.append(tree)
        else:
            line_of_sight.append(tree)
            break
    return line_of_sight

def main(filename):
    
    df = pd.DataFrame(read_file(filename))
    # print(df)
    
    rows = len(df)
    cols = len(df.columns)
    # visible_trees = set()
    scenic_scores = []
    
    
    for col in range(0, cols):
        for row in range(0, rows):
            tree_size = df[row][col]
            trees_col = df.iloc[:,row]
            trees_row = df.iloc[col]
            # print(f"rows: \n{trees_row}")
            # print(f"cols: \n{trees_col}")


            
            trees_left = line_of_sight_trees(reversed(trees_row[:row]), tree_size)
            trees_right = line_of_sight_trees(trees_row[row+1:], tree_size)
            trees_up = line_of_sight_trees(reversed(trees_col[:col]), tree_size)
            trees_down = line_of_sight_trees(trees_col[col+1:], tree_size)


            scenic_score = len(trees_left) * len(trees_right) * len(trees_up) * len(trees_down)
            scenic_scores.append(scenic_score)


            # print(f"comparing ({col},{row}) [{tree_size}] score {scenic_score}")
            # print(f"trees to the left: {list(trees_left)}") 
            # print(f"trees to the right: {list(trees_right)}")
            # print(f"trees up: {list(trees_up)}") 
            # print(f"trees down: {list(trees_down)}") 
            
    
    scenic_scores.sort(reverse=True)
    print(f"{scenic_scores[0]}")
    
    # 3512
    
if __name__ == "__main__":
    # main("test.input")
    main("question.input")