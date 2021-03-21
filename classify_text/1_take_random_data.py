import sys
import os
import random
import shutil

if __name__ == '__main__':
    folder_in = sys.argv[1]
    assert os.path.exists(folder_in), "folder is'nt exist!"
    folder_out = sys.argv[2]
    number_files = sys.argv[3]
    os.makedirs(folder_out, exist_ok=True)
    folders = [d for d in os.listdir(folder_in) if
               os.path.isdir(os.path.join(folder_in, d))]
    for folder in folders:
        list_files = []
        sub_folder = os.path.join(folder_in, folder)
        save_sub_folder = os.path.join(folder_out, folder)
        os.makedirs(save_sub_folder, exist_ok=True)
        news_folders = os.listdir(sub_folder)
        for news_folder in news_folders:
            path_news = os.path.join(sub_folder, news_folder)
            files = [os.path.join(path_news, file) for file in os.listdir(path_news)]
            if len(files)>0:
                list_files = list_files + files
        if len(list_files)>int(number_files):
            random.shuffle(list_files)
            list_files = list_files[:int(number_files)]
        id = 1
        for file in list_files:
            shutil.move(file, os.path.join(save_sub_folder, str(id)+".txt"))
            id = id + 1
        print("Processed {} done!".format(folder))
