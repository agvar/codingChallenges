#!/home/agvar/Projects/python/codingChallenges/venv/bin/python
import traceback
import os
def read_file(file_path,chunk_size=1024):
    try:
        if not file_path or not os.path.exists(file_path) :
            raise ValueError(f"Invalid file name provided{file_path}")
        if not isinstance(chunk_size,int):
            raise ValueError(f"chunk size provided is not integer")
        char_frequency = {}
        with open(file_path,"r") as f:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    for char in chunk :
                        char_frequency[char] = char_frequency.setdefault(char , 0) + 1
                else:
                    break
        return char_frequency
    except FileNotFoundError as e:
        print(f"{file_path} not found")
    except IOError as e:
        print(f"IO error reading file{file_path}")

if __name__ == "__main__":
    try:
        file_path = "135-0.txt"
        chunk_size = 1024
        char_frequency = read_file(file_path,chunk_size)
        if 'X' in char_frequency:
            print(char_frequency['t'])
    except Exception as e:
        error_stack = traceback.format_exc()
        print(e,error_stack)
