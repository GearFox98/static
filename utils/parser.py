import re, os

# REGEX
VARIABLE_FORMAT = re.compile("^[A-Za-z0-9_]+([ ]*=[ ]*)")
VARIABLE_NAME = re.compile("^[A-Za-z0-9_]+")

def is_var(line):
    p = re.match(VARIABLE_FORMAT, line).__bool__()
    print(p)
    return p

def extract_name(line: str):
    end = re.match(VARIABLE_NAME, line).end()
    return line[:end]

def extract_value(line: str):
    end = re.match(VARIABLE_FORMAT, line).end()
    return line[end:]

def parse(path: str, page: str):
    variables = dict()
    print(os.path.exists(path.format(page)))
    with open(path.format(page), 'r') as stream:
        for row in stream.readlines():
            print(row)
            if is_var(row):
                variables = {extract_name(row): extract_value(row)}
    print(variables)