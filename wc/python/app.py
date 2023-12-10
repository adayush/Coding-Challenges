import sys


def parse_args(args) -> dict:
    flags = []
    filename = ""
    for arg in args:
        if arg.startswith("-"):
            flags.append(arg)
        else:
            filename = arg
            break

    return {"flags": flags, "filename": filename}


def count_bytes(text) -> int:
    count = len(text.encode("utf-8"))

    return count


def count_lines(text) -> int:
    count = text.count("\n")

    return count


def count_words(text) -> int:
    count = 0
    for line in text.split("\n"):
        count += len(line.split())

    return count


def count_chars(text) -> int:
    count = len(text)

    return count


def main() -> None:
    # parse arguments
    args = parse_args(sys.argv[1:])

    flags = args["flags"]
    filename = args["filename"]

    if filename:
        try:
            # windows newline is \r\n but macos uses \n. test.tx uses the former
            text = open(filename, newline="\r\n").read()
        except FileNotFoundError:
            print("Error: file not found")
            return
    else:
        text = sys.stdin.read()

    tools = {
        "-c": count_bytes,
        "-l": count_lines,
        "-w": count_words,
        "-m": count_chars
    }

    if len(flags) == 0:
        flags = ["-c", "-l", "-w"]

    output = []

    for flag in flags:
        if flag not in tools:
            print(f"Error: Flag '{flag}' is not supported ")
            continue

        output.append(tools[flag](text))

    output.sort()

    for result in output:
        print(f"{result:<8}", end="")

    print(filename)


if __name__ == "__main__":
    main()
