from utils import process_text
import sys, os, time
import multiprocessing

if __name__ == '__main__':
    folder_in = sys.argv[1]
    folder_out = sys.argv[2]
    os.makedirs(folder_out, exist_ok=True)
    for label in os.listdir(folder_in):
        print("Processing {}".format(label))
        # test = 0
        start = time.time()
        list_files = []
        path_label = os.path.join(folder_in, label)
        path_out = os.path.join(folder_out, label)
        os.makedirs(path_out, exist_ok=True)
        for file_origin in os.listdir(path_label):
            f_read = os.path.join(path_label, file_origin)
            f_write = os.path.join(path_out, file_origin)
            list_files.append((f_read, f_write))
            # test = test + 1
            # if test>1500:
            #     break
        with multiprocessing.Pool(processes=8) as pool:
            pool.starmap(process_text, list_files)
        end = time.time()
        print("\t\tDone in {:.2f}".format(end-start))