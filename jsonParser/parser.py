#!/home/agvar/Projects/python/codingChallenges/venv/bin/python
import sys
import os

tokens = {
'{' :'start',
'}': 'end' ,
'"' : 'quote',
',' : 'separator'
}

def tokenizer(file):
    print("raw_input",file)
    tokenized_input = []
    current = ''
    for char in file_buffer:
        if char in tokens:
            tokenized_input.append(char)
            if current :
                tokenized_input.append(current)
                current =''
        else:
            current += char
    return tokenized_input 

def parser(tokenized_input) :
    if not tokenized_input:
        return 1
    for token in tokenized_input :
        print(token)
    return 0

if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
        if not file_path or not os.path.exists(file_path) :
            raise FileNotFoundError
        
        with open(file_path,"r") as f:
            file_buffer = f.read()

        tokenized_input = tokenizer(file_buffer)
        return_flag = parser(tokenized_input)
        if return_flag :
            print(f"Invalid parser, return {return_flag}")
        else:
            print(f"Valid parser, return {return_flag}")

    except FileNotFoundError as e:
        print(f"{file_path} not found ")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
