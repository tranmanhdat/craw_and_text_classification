import multiprocessing
import sys
import os, time
from random import shuffle
import shutil

def copy_file(f_in, f_out):
    shutil.move(f_in, f_out)
if __name__ == '__main__':
    folder_in = sys.argv[1]
    folder_out = sys.argv[2]
    os.makedirs(folder_out, exist_ok=True)
    train_path = os.path.join(folder_out, "train")
    os.makedirs(train_path, exist_ok=True)
    test_path = os.path.join(folder_out, "test")
    os.makedirs(test_path, exist_ok=True)
    for label in os.listdir(folder_in):
        list_files = []
        path_label = os.path.join(folder_in, label)
        files = os.listdir(path_label)
        shuffle(files)
        for i in range(len(files)):
            f_read = os.path.join(path_label, files[i])
            if i<0.7*len(files):
                path_folder = os.path.join(train_path, label)
            else:
                path_folder = os.path.join(test_path, label)
            os.makedirs(path_folder, exist_ok=True)
            f_write = os.path.join(path_folder, files[i])
            list_files.append((f_read, f_write))
        with multiprocessing.Pool(processes=8) as pool:
            pool.starmap(copy_file, list_files)