# Thống kê các word xuất hiện ở tất cả các nhãn
import codecs
import os
import sys

if __name__ == '__main__':
    folder_in = sys.argv[1]
    folder_out = sys.argv[2]
    os.makedirs(folder_out, exist_ok=True)
    folders = [d for d in os.listdir(folder_in) if
               os.path.isdir(os.path.join(folder_in, d))]
    vocab = {}
    label_vocab = {}
    freq_text = {}
    for folder in folders:
        path_folder = os.path.join(folder_in, folder)
        files = os.listdir(path_folder)
        for file in files:
            f_in = codecs.open(os.path.join(path_folder, file), "r", encoding='utf-8')
            text = f_in.read()
            words = text.split(" ")
            label = str(folder)
            if label not in label_vocab:
                label_vocab[label] = {}
            for word in words:
                freq_text[word] = freq_text.get(word, 0) + 1
                label_vocab[label][word] = label_vocab[label].get(word, 0) + 1
                if word not in vocab:
                    vocab[word] = set()
                vocab[word].add(label)
    count = {}
    total_label = len(folders)
    for word in vocab:
        if len(vocab[word]) == total_label:
            count[word] = min([label_vocab[x][word] for x in label_vocab])
    sorted_count = sorted(count, key=count.get, reverse=True)
    # stop_words = sorted_count[:20]
    with open(os.path.join(folder_out, "stop_words.txt"), "w+",
              encoding='utf-8') as f_out:
        for word in sorted_count:
            f_out.write("{}\t{}\n".format(word, count[word]))
    sorted_freq = sorted(freq_text, key=freq_text.get)
    with open(os.path.join(folder_out, "freq_words.txt"), "w+",
              encoding='utf-8') as f_out:
        for word in sorted_freq:
            f_out.write("{}\t{}\n".format(word, freq_text[word]))