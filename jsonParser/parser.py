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
    """
    Tokenizes the input file buffer into a list of tokens.

    Args:
        file_buffer (str): The input file buffer to be tokenized.

    Returns:
        list: A list of tokens representing the input file buffer.

    Raises:
        ValueError: If there is an error in tokenizing the input file buffer.

    """
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
    """
    A recursive descent parser for JSON input.
    Args:
        tokenized_input (List[str]): The input JSON string tokenized into a list of strings.
    Raises:
        ValueError: If the input is empty, missing opening or closing JSON identifiers, or if there is an unexpected token.
    Returns:
        int: Returns 0 if the input is valid JSON, otherwise raises a ValueError.
    The parser function uses nested helper functions to check the validity of the input JSON string. It recursively checks the validity of the input by matching the tokens with the expected patterns.
    The check_token function checks if the given value matches the expected token. It raises a ValueError if the value does not match the expected token.
    The check_string function checks if the given value is a string. It raises a ValueError if the value is not a string or if there is an unexpected end of line.
    The check_value function checks the validity of the input value based on specified patterns. It raises a ValueError if the value does not match the expected patterns.
    The main function first checks if the tokenized_input is empty. If it is, it raises a ValueError with the message "No input exception".

    """
    def check_token(value,token):
        """
        Check if the given value matches the expected token.
        Args:
            value (Any): The value to check.
            token (Any): The expected token.
        Raises: 
            ValueError: If the value does not match the expected token.
        Returns: None

        """
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
        """
        Check if the given value is a string.
        Args:
            value (Any): The value to check.
        Raises:
            ValueError: If the value is not a string or if there is an unexpected end of line.
        Returns: None

        """
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
            """
            A function to check the validity of the input value based on specified patterns.
            Args:
                value (Any): The value to be checked.
            Raises:
                ValueError: If the value does not match the expected patterns.
            Returns: None

            """
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
