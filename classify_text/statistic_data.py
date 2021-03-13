import sys
import os
import matplotlib.pyplot as plt
import numpy as np


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


if __name__ == '__main__':
    root = sys.argv[1]
    figure_folder = sys.argv[2]
    os.makedirs(figure_folder, exist_ok=True)
    folders = [d for d in os.listdir(root) if
               os.path.isdir(os.path.join(root, d))]
    type_news = {}
    for folder in folders:
        if folder not in type_news:
            type_news[folder] = [0, 0]
        sub_folder = os.path.join(root, folder)
        news_folders = os.listdir(sub_folder)
        for news_folder in news_folders:
            path_news = os.path.join(sub_folder, news_folder)
            files = os.listdir(path_news)
            if len(files) > 0:
                tmp = type_news[folder]
                tmp[0] = tmp[0] + 1
                tmp[1] = tmp[1] + len(files)
                type_news[folder] = tmp
    print(type_news)
    type_news = sorted(type_news.items(), key=lambda x: x[1][0])
    type_news = dict(type_news)
    type_of_news, number_news, number_para = [], [], []
    for key, value in type_news.items():
        type_of_news.append(key)
        number_news.append(value[0])
        number_para.append(value[1])

    x = np.arange(len(type_of_news))  # the label locations
    width = 0.6  # the width of the bars
    fig, ax = plt.subplots()
    rect = ax.bar(x, number_news, width, label='number')
    ax.set_xlabel('Type')
    ax.set_ylabel('Number')
    ax.set_title('Number news crawled by type')
    ax.set_xticks(x)
    ax.set_xticklabels(type_of_news)
    ax.legend(loc='upper left')
    autolabel(rect)
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout()
    plt.savefig(os.path.join(figure_folder, "number_of_news.png"), dpi=100)
    plt.show()

    fig, ax = plt.subplots()
    rect = ax.bar(x, number_para, width, label='number')
    ax.set_xlabel('Type')
    ax.set_ylabel('Number')
    ax.set_title('Number of paragraphs crawled by type')
    ax.set_xticks(x)
    ax.set_xticklabels(type_of_news)
    ax.legend(loc='upper left')
    autolabel(rect)
    fig.set_size_inches(18.5, 10.5)
    fig.tight_layout()
    plt.savefig(os.path.join(figure_folder, "number_of_paragraphs.png"), dpi=100)
    plt.show()