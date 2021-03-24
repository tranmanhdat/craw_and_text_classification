from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from utils import load_data
import time
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='log/6.3.log', filemode='w', level=logging.DEBUG,
                        format=(
                            '%(levelname)s:\t''%(filename)s:''%(funcName)s():''%(lineno)d\n''%(message)s'))
    print("Loading data...")
    start = time.time()
    X_train, y_train, labels = load_data("../data_5/train")
    X_test, y_test, _ = load_data("../data_5/test")
    end = time.time()
    logging.info("Load data in {:.2f}s".format(end - start))
    print("Start training...")
    start = time.time()
    label_encoder = LabelEncoder()
    label_encoder.fit(labels)
    le_name_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    logging.info(le_name_mapping)
    y_train = label_encoder.transform(y_train)
    y_test = label_encoder.transform(y_test)
    text_clf = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), max_df=0.5)),
                         ('tfidf', TfidfTransformer()),
                         ('clf', LogisticRegression(max_iter=5000)),
                         ])
    text_clf.fit(X_train, y_train)
    end = time.time()
    logging.info("Trained in {:.2f}s".format(end - start))
    predicted = text_clf.predict(X_train)
    logging.info(metrics.classification_report(y_train, predicted))
    logging.info(metrics.confusion_matrix(y_train, predicted))

    predicted = text_clf.predict(X_test)
    logging.info(metrics.classification_report(y_test, predicted))
    logging.info(metrics.confusion_matrix(y_test, predicted))