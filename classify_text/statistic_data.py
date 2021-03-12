import sys
import os

if __name__ == '__main__':
    root = sys.argv[1]

    folders = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    print(folders)