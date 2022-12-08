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

# The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
# The top-middle 5 is visible from the top and right.
# The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
# The left-middle 5 is visible, but only from the right.
# The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
# The right-middle 3 is visible from the right.
# In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

tree_reset = -1

def read_file(filename):
        
    with open(filename) as f:

        for _, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield [int(l) for l in line]

def tree_position(column, row, size):
    return (column, row, size)

def list_visible_trees(trees) -> list:
    tallest = 0
    for ix, tree in enumerate(trees):
        if tree > tallest:
            print(f"tree {ix} [{tree}] is higher than {tallest}")
            yield tree
            tallest = tree
    
def create_tree_row(trees, row):
    return [tree_position(ix, row, t) for ix, t in enumerate(trees)]

def create_tree_column(trees, column):
    return [tree_position(column, ix, t) for ix, t in enumerate(trees)]


def main(filename):
    
    df = pd.DataFrame(read_file(filename))
    print(df)
    
    rows = len(df)
    cols = len(df.columns)
    visible_trees = set()
    
    
    for col in range(0, cols):
        for row in range(0, rows):
            tree_size = df[row][col]
            trees_col = df.iloc[:,row]
            trees_row = df.iloc[col]
            # print(f"rows: \n{trees_row}")
            # print(f"cols: \n{trees_col}")
        
            trees_left = trees_row[:row]
            trees_right = trees_row[row+1:]
            trees_up = trees_col[:col]
            trees_down = trees_col[col+1:]
            
                   
            # IS there a path to the left / right / up / down 
            # There is a path when everythin in a direction is lower
            
            visible = False
            if len(trees_left) == 0 or len(trees_right) == 0 or len(trees_up) == 0 or len(trees_down) == 0:
                visible_trees.add(tree_position(col, row, tree_size))
                visible = True
                
            elif max(trees_left) < tree_size or max(trees_right) < tree_size or max(trees_up) < tree_size or max(trees_down) < tree_size:
                visible_trees.add(tree_position(col, row, tree_size))
                visible = True
            # else:
                # print(f"({col}, {row}) not visible")
            
            print(f"comparing ({col},{row}) [{tree_size}] Visible {visible}")


            # print(f"tree col: {list(trees_col)}")
            # print(f"tree row: {list(trees_row)}")

            # print(f"trees to the left: {list(trees_left)}") 
            # print(f"trees to the right: {list(trees_right)}")
            # print(f"trees up: {list(trees_up)}") 
            # print(f"trees down: {list(trees_down)}") 
            
    
    print(f"[{len(visible_trees)}] trees are visible")
    
    # 3512
    
if __name__ == "__main__":
    # main("test.input")
    main("question.input")