#!/home/agvar/Projects/python/codingChallenges/venv/bin/python
import os 
import sys

def byteCount(file_path):
    return os.path.getsize(file_path)

def lineCount(file_path):
     lineCount = 0
     with open(file_path,"r") as f:
          linecount += 1
     return lineCount


if __name__ == "__main__":
    try:
        flag = sys.argv[1]
        file_path = sys.argv[2]
        if os.path.exists(file_path):
                if flag == "-c":
                    count = byteCount(file_path)
                elif flag == "-l" :
                    count = lineCount(file_path)

                print(f"{file_path} {count}")
        else:
                raise FileNotFoundError(f"The file{file_path} does not exist")
    except FileNotFoundError as e:
        print(e)
        sys.exit(-1)