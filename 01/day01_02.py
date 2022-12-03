import pandas as pd

def read_file(filename):
    
    with open(filename) as f:

        for elf_index, line in enumerate([l.rstrip() for l in f]):
            if line:
                yield (f"{elf_index}", int(line))


elf_values = read_file("day01_01.input")

df = pd.DataFrame(data=elf_values)
df.columns = ["elf", "calories"]

elf_sums = df.groupby("elf").sum()

print(elf_sums.nlargest(n=3, columns="calories").sum())

