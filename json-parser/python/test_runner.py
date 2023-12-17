import os
import sys

import app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage - python app.py path/to/folder")
    else:
        folder = sys.argv[1]
        files = [f"{folder}/{filename}" for filename in os.listdir(sys.argv[1])]
        files.sort()

        for filename in files:
            print(f"{filename:<30}", end="")
            app.main(filename)
        # main(sys.argv[1])