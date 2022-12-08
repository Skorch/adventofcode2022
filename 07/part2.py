import re

class Folder():
    def __init__(self, folder_name: str, parent = None) -> None:
        self.folder_name = folder_name
        self.files = {}
        self.folders = []
        self.parent = parent
    
    def add_folder(self, folder_name):
        new_folder = Folder(folder_name, self)
        self.folders.append( new_folder )
        return new_folder
    
    def add_file(self, file, size) -> None:
        self.files[file] = size
    
    def size(self) -> int:
        folder_sizes = sum([f.size() for f in self.folders])
        file_sizes = sum([self.files[f] for f in self.files]) + folder_sizes
        return file_sizes
    
    def filter_folders(self, size_filter) -> list:

        arr = []

        current_size = self.size()
                
        # print(f"calculating {self.folder_name} {current_size}")
        print(current_size)
        
        if current_size >= size_filter:
            # print(f"adding folder {self.folder_name} with size {current_size}")
            arr.append(current_size)
        
            # print(arr)
        
        for filtered in [f.filter_folders(size_filter) for f in self.folders]:
            arr += filtered
        
        return arr

        
    def tree(self) -> dict:

        return {
            self.folder_name: {
                # "size": self.size(),
                "files": self.files,
                "subfolders": [f.tree() for f in self.folders]
            }
        }
    
def read_file(filename):
    
    with open(filename) as f:

        output = []
        command = None
        args = None
        for ix, line in enumerate([l.rstrip() for l in f]):
            if not line:
                continue
            

            # print(line)
            # new command, yield prior plus any output and reset
            if line.startswith("$ ") and command:
                print(f"sending command {command} {args}")
                yield (ix, command, args, output)
                command = None
                args = None
                output = []
            if line.startswith("$ "):
                result = line.split(" ")
                command = result[1]
                args = result[2:] if len(result) > 2 else None
            else:
                output.append(line)
                
        # print(f"yielding {(ix, command, args, output)}")
        yield (ix, command, args, output)
                

def file_listing(output):
    for line in output:
        
        # print(line)
        args = re.search("^(.+) (.+)$", line).groups(1)
        # print(args)
        if args[0] != "dir":
            filesize = int(args[0])
            filename = args[1]        
            yield(filename, filesize)    
        else:
            print(f"skipping folder {line}")
        

def exec_ls(command_args, output):
    global current_folder
    
    print("ls")
    
    for filename, filesize in file_listing(output):
        print(f"adding file {filename} to {current_folder}")
        current_folder.add_file(filename, filesize)


root_folder = Folder("/")
current_folder = root_folder


def exec_cd(command_args, output):
    global current_folder, root_folder
    
    print("cd ")
    folder = command_args[0]
    if folder == "/":
        print("cd /")
        current_folder = root_folder
        print(f"moving to root {current_folder}")
    elif folder == "..":
        # print(f"cd .. moving from {current_folder.folder_name} to {current_folder.parent.folder_name}")
        print(f"cd .. moving from {current_folder.folder_name} ")
        print(f"to {current_folder.parent.folder_name}")
        parent_folder = current_folder.parent
        
        current_folder = parent_folder
        
        # if parent_folder:
        #     current_folder = parent_folder
        #     print(f"moving to parent: {current_folder}")
        # else:
        #     print("already at root, cannot move to parent")
    else:
        print(f"cd {folder}")
        new_folder = current_folder.add_folder(folder)
        current_folder = new_folder
        print(f"moving to {folder}: {current_folder}")
        

commands = {
    "cd": exec_cd,
    "ls": exec_ls
}

    

def main(filename):
    for ix, command, args, output in read_file(filename):
        # print(f"{ix} {command} {args} {output}")
        commands[command](args, output)
        
    space_available = 70000000 - root_folder.size()
    print(f"space available: {space_available}")
    space_needed = 30000000 - space_available
    print(f"space needed {space_needed}")
    large_folders = root_folder.filter_folders(space_needed)
    large_folders.sort()
    print(f"size of filtered folder {root_folder.folder_name} = {large_folders}")
    
    # print(f"tree: {root_folder.tree()}")
       
if __name__ == "__main__":
    # main("test.input")
    main("question.input")
    
    # 8980615
    