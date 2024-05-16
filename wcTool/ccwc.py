#!/home/agvar/Projects/python/codingChallenges/venv/bin/python
import os 
import sys

class MissingArgumentError(Exception):
     pass

def byteCount(file_path):
    return os.path.getsize(file_path)

def lineCount(file_path):
     line_count = 0
     with open(file_path,"r") as f:
          for line in f:
            line_count += 1
     return line_count

def wordCount(file_path):
     with open(file_path,"r") as f:
          word_count = 0
          for line in f:
               word_count += len(line.split())
          return word_count

def charCount(file_path):
     char_count = 0
     with open(file_path,"r") as f:
          for line in f:
            char_count += len(line)
     return char_count

def lineStdin():
     line_count = 0
     f = sys.stdin
     for line in f:
        line_count += 1
     return line_count
     

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2 :
             raise MissingArgumentError(f"Missing or incorrect arguments when calling the ccwc program")        
        if not sys.stdin.isatty() and len(sys.argv) == 2 and sys.argv[1]=="-l":
             flag = sys.argv[1]
             file_path = "stdin"
             
        elif sys.stdin.isatty() and len(sys.argv) == 3:
            flag = sys.argv[1]
            file_path = sys.argv[2]
        elif sys.stdin.isatty() and len(sys.argv) == 2:
             file_path = sys.argv[1]
             flag = "-all"
             
        else:
             raise MissingArgumentError(f"Missing or incorrect arguments when calling the ccwc program")

        if file_path == "stdin" :
                count = str(lineStdin())
                file_path = ''
        elif os.path.exists(file_path):
                if flag == "-c":
                    count = str(byteCount(file_path))
                elif flag == "-l" :
                    count = lineCount(file_path)
                elif flag == "-w" :
                    count = wordCount(file_path)
                elif flag == "-m" :
                    count = charCount(file_path)
                elif flag == "-all":
                     count = str(lineCount(file_path)) + ' ' + str(wordCount(file_path)) + ' ' + str(byteCount(file_path))
        else:
                raise FileNotFoundError(f"The file{file_path} does not exist")
        print(f"{file_path} {count}")
    except FileNotFoundError as e:
        print(e)
        sys.exit(-1)
    except MissingArgumentError as e:
        print(e)
        sys.exit(-1)