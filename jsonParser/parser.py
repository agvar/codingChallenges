#!/home/agvar/Projects/python/codingChallenges/venv/bin/python
import sys
import os
import traceback
import re

tokens = {
'startIdentifier': '{',
'endIdentifier' :'}',
'quote' : '"',
'comma': ',',
'separator':':',
'listStartIdentifier':'[',
'listEndIdentifier':']'
}

def tokenizer(file_buffer):
    tokenized_input = []
    concat_val = ''
    idx = 0
    concat_flag = 0
    key_flag = 1
    object_val_flag = 0
    list_val_flag = 0
    print("file_buffer",file_buffer)
    while idx < len(file_buffer):
        print(file_buffer[idx])
        if file_buffer[idx] == tokens['startIdentifier'] :
            if idx == 0 :
                tokenized_input.append(file_buffer[idx])
            elif concat_flag and not key_flag :
                concat_val = file_buffer[idx]
                object_val_flag = 1
        elif file_buffer[idx] == tokens['endIdentifier'] :
            if idx== len(file_buffer)-1:
                if concat_val :
                    tokenized_input.append(concat_val)
                tokenized_input.append(file_buffer[idx])
            elif concat_flag and not key_flag :
                if object_val_flag:
                    object_val_flag = 0
                concat_val += file_buffer[idx]
                tokenized_input.append(concat_val)
                concat_val = ''
        elif file_buffer[idx] == tokens['separator']:
            if key_flag :
                tokenized_input.append(file_buffer[idx])
                key_flag = 0
                concat_flag = 1
                concat_val = ''
            else:
                concat_val += file_buffer[idx]

        elif file_buffer[idx] == tokens['listStartIdentifier'] and not key_flag:
            list_val_flag = 1
            concat_val = file_buffer[idx]
        elif file_buffer[idx] == tokens['listEndIdentifier'] and not key_flag:
            list_val_flag = 0
            concat_val += file_buffer[idx]
            tokenized_input.append(concat_val)
            concat_val = ''
        elif file_buffer[idx] == tokens['comma']:
            if not key_flag and concat_val:
                tokenized_input.append(concat_val)
            tokenized_input.append(file_buffer[idx])
            key_flag = 1
            concat_flag = 0
        elif file_buffer[idx] == tokens['quote']:
            if key_flag :
                if concat_flag :
                    tokenized_input.append(concat_val)
                    tokenized_input.append(file_buffer[idx]) 
                    concat_flag = 0
                    concat_val = ''
                else:
                    concat_flag = 1
                    concat_val = '' 
                    tokenized_input.append(file_buffer[idx])  
            else:
                if concat_flag and concat_val:
                    if object_val_flag  or list_val_flag:
                        concat_val += file_buffer[idx]
                    else:
                        concat_val += file_buffer[idx]
                        tokenized_input.append(concat_val)
                        concat_flag = 0
                        concat_val = ''
                else:
                    concat_flag = 1
                    concat_val = file_buffer[idx]  

        elif not file_buffer[idx].strip():
            pass
        elif concat_flag:
            concat_val += file_buffer[idx]
        else :
            raise ValueError(f'Error in tokenizing input with character {file_buffer[idx]} at index {idx}')
        idx += 1
    print(tokenized_input)
    return tokenized_input 

def parser(tokenized_input) :
    def check_token(value,token):
        nonlocal idx
        print(idx,tokenized_input[idx])
        if value == token :
            if idx < len(tokenized_input) - 1 :
                idx += 1
            else:
                raise ValueError("expected end of line {token}")                   
        else :
            raise ValueError(f"expected {token} but {value} encountered")
        
    def check_string(value):
        nonlocal idx
        print(idx,tokenized_input[idx])
        if isinstance(value,str):
            if idx < len(tokenized_input) - 1 :
                idx += 1
            else:
                raise ValueError(f"unexpected end of line")                   
        else:
            raise ValueError(f"string expected, found {tokenized_input[idx]}")

    def check_value(value):
            nonlocal idx
            print(idx,tokenized_input[idx])
            str_pattern = r'^(").*\1$'
            num_pattern = r'\d*\.?\d+'
            array_pattern = r'\[(".*"|\d+|true|false|null)?\]'
            object_pattern = r'\{(\s*(".*")\s*:\s*(.*)\s*)?\}'
            if re.match(str_pattern, value) or re.match(num_pattern,value) or value in ['true','false','null'] or re.match(array_pattern,value) or re.match(object_pattern,value) :
                if idx < len(tokenized_input) - 1 :
                    idx += 1
                else:
                    raise ValueError(f"unexpected end of line")                   
            else:
                raise ValueError(f"value expected to be string,int or boolean")
           
    if not tokenized_input:
        raise ValueError(f"No input exception")
    else:
        if not tokenized_input[0] == "{" or not tokenized_input[-1] == "}" :
            raise ValueError(f"Missing opening or closing JSON identifiers")
        if tokenized_input[0] == tokens['startIdentifier'] and tokenized_input[1]== tokens['endIdentifier']:
            return 0
        idx = 0
        while idx < len(tokenized_input):
            print(idx,tokenized_input[idx])
            if tokenized_input[idx] == tokens['startIdentifier'] or tokenized_input[idx] == tokens['comma'] :   
                idx += 1
                check_token(tokenized_input[idx],tokens['quote'])
                check_string(tokenized_input[idx])   
                check_token(tokenized_input[idx],tokens['quote'])   
                check_token(tokenized_input[idx],tokens['separator'])  
                check_value(tokenized_input[idx])    
            elif tokenized_input[idx] == tokens['endIdentifier'] :
                return 0
            else:
                raise ValueError(f"unexpected token {tokenized_input[idx]}")
    return 0

if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
        #file_path ="./jsonParser/tests/step2/valid.json"
        if not file_path or not os.path.exists(file_path) :
            raise FileNotFoundError
        with open(file_path,"r") as f:
            file_buffer = f.read().strip()
        tokenized_input = tokenizer(file_buffer)
        parser(tokenized_input)
        print(f"Valid JSON file")
    except FileNotFoundError as e:
        print(f"{file_path} not found ")
        sys.exit(1)
    except Exception as e:
        error_stack = traceback.format_exc()
        print(f"Invalid JSON file")
        print(e,error_stack)
        sys.exit(1)
