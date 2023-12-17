import sys


def string_validator(file):
    c = get_curr_char(file)

    if c != '"':
        return False
    
    prev = ""
    
    while True:
        c = get_curr_char(file, True)

        if c == None:
            break

        if prev == "\\":
            if c in ["u", "b", "f", "n", "r", "t", "\"", "\\", "/"]:
                prev = ""
                continue

            return False
        
        elif c == '"' :
            return True 

        prev = c


def array_validator(file, array_depth = 1):
    if array_depth >= 20:
        return False

    get_curr_char(file)

    if get_curr_char(file) == "]":
        return True

    file.seek(file.tell() - 1)

    while True:
        if value_validator(file, array_depth + 1) == False:
            break

        c = get_curr_char(file)
        if c == "]":
            return True

        elif c != ",":
            break

    return False


def value_validator(file, array_depth = 1):
    c = get_curr_char(file)
    file.seek(file.tell() - 1)

    if c == "{":
        if object_validator(file) == True:
            return True

    elif c == "[":
        if array_validator(file, array_depth) == True:
            return True

    elif c == '"':
        if string_validator(file) == True:
            return True

    else:
        value = ""

        while True:
            char = get_curr_char(file)

            if char != "," and char != "}" and char != "]":
                value += char
            else:
                file.seek(file.tell() - 1)
                break

        if value in ["null", "true", "false"]:
            return True

        try:
            float(value)
            if value[0] == '0':
                if len(value) != 1 and value[1] != ".":
                    return False
        except:
            return False

        return True
    return False


def pair_validator(file):
    if string_validator(file) == False:
        return False

    if get_curr_char(file) == ":" and value_validator(file):
        return True

    return False


def object_validator(file):
    if get_curr_char(file) != "{":
        return False

    if get_curr_char(file) == "}":
        return True

    file.seek(file.tell() - 1)

    while True:
        if pair_validator(file) != True:
            return False

        char = get_curr_char(file)

        if char == "}":
            return True
        elif char != ",":
            file.seek(file.tell() - 1)
            break

    return False


def get_curr_char(file, in_string = False):
    while True:
        c = file.read(1)
        # print(repr(c))

        if c == " ":
            continue
        if c == "\n":
            if in_string:
                return None
            continue

        elif c in [None, "", "\t", "\n"]:
            return None
        
        return c


def main(path: str) -> int:
    if len(sys.argv) < 2:
        print("Usage - python app.py path/to/file.json")
        return 1

    try:
        file = open(path)  # improve on this by handling line by line
    except FileNotFoundError:
        print(f"Error: File {path} not found.")
        return 2

    if len(file.readline()) == 0:
        print("JSON is not valid ❌")
        return 3

    file.seek(0)
    c = get_curr_char(file)
    file.seek(0)

    if c == "{":
        result = object_validator(file)
    else:
        result = array_validator(file)

    if result and get_curr_char(file) == None:
        print("JSON is valid ✅")
        return 0
    else:
        print("JSON is not valid ❌")
        return 3


if __name__ == "__main__":
    exit(main(sys.argv[1]))
