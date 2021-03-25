import codecs
import multiprocessing
import sys
import os
import time


def load_stop_words(stop_words_file):
    with open(stop_words_file, "r", encoding="UTF-8") as f_read:
        lines = f_read.readlines()
        stop_words = []
        for i in range(2, 21):
            stop_words.append(lines[i].split("\t")[0])
        return stop_words


def load_remove_words(freq_words_file):
    with open(freq_words_file, "r", encoding="UTF-8") as f_read:
        lines = f_read.readlines()
        remove_words = []
        for line in lines:
            pieces = line.split("\t")
            if int(pieces[1])<21:
                remove_words.append(pieces[0])
        return remove_words


stop_words = load_stop_words("freq_text/stop_words.txt")
remove_words = load_remove_words("freq_text/freq_words.txt")
need_remove_words = stop_words + list(set(remove_words) - set(stop_words))

def remove_stopwords(f_in, f_out):
    f_read = codecs.open(f_in, "r", encoding='utf-8')
    text = f_read.read()
    words = []
    for word in text.split():
        if word not in need_remove_words:
            words.append(word)
    text = ' '.join(words)
    f_write = codecs.open(f_out, "w+", encoding='utf-8')
    f_write.write(text)
    f_write.close()
    f_read.close()


if __name__ == '__main__':
    folder_in = sys.argv[1]
    folder_out = sys.argv[2]
    os.makedirs(folder_out, exist_ok=True)
    for label in os.listdir(folder_in):
        print("Processing {}".format(label))
        start = time.time()
        list_files = []
        path_label = os.path.join(folder_in, label)
        path_out = os.path.join(folder_out, label)
        os.makedirs(path_out, exist_ok=True)
        for file_origin in os.listdir(path_label):
            f_read = os.path.join(path_label, file_origin)
            f_write = os.path.join(path_out, file_origin)
            list_files.append((f_read, f_write))
        with multiprocessing.Pool(processes=8) as pool:
            pool.starmap(remove_stopwords, list_files)
        end = time.time()
        print("\t\tDone in {:.2f}".format(end - start))
