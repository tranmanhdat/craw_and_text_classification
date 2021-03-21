from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from utils import rdr_segmenter
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from utils import load_data
import time
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='log/6.2.log', filemode='w', level=logging.DEBUG,
                        format=(
                            '%(levelname)s:\t''%(filename)s:''%(funcName)s():''%(lineno)d\n''%(message)s'))
    print("Loading data...")
    start = time.time()
    X_train, y_train, labels = load_data("../data_split/train")
    X_test, y_test, _ = load_data("../data_split/test")
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

    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier()),
    ])
    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__max_features': (None, 5000, 10000, 50000),
        'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        'tfidf__use_idf': (True, False),
        'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
        'clf__max_iter': (500, 1000, 2000),
    }
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)
    t0 = time.time()
    grid_search.fit(X_train, y_train)
    print("done in %0.3fs".format(time.time() - t0))
    logging.info("done in %0.3fs".format(time.time() - t0))
    print()
    print("Best score: %0.3f".format(grid_search.best_score_))
    logging.info("Best score: %0.3f".format(grid_search.best_score_))
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
        logging.info("\t%s: %r" % (param_name, best_parameters[param_name]))

    # text_clf = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), max_df=0.5)),
    #                      ('tfidf', TfidfTransformer()),
    #                      ('clf', LinearSVC()),
    #                      ])
    # text_clf.fit(X_train, y_train)
    # end = time.time()
    # logging.info("Trained in {:.2f}s".format(end - start))
    # predicted = text_clf.predict(X_test)
    # logging.info(metrics.classification_report(y_test, predicted))
    # logging.info(metrics.confusion_matrix(y_test, predicted))
    # with open("result/2_SVM_Classifier_accuracy.txt", "w+",
    #           encoding="UTF-8") as f_out:
    #     f_out.write(str(metrics.classification_report(y_test, predicted)))
    # with open("result/2_SVM_Classifier_confusion_matrix.txt", "w+",
    #           encoding="UTF-8") as f_out:
    #     f_out.write(str(metrics.confusion_matrix(y_test, predicted)))