import numpy as np


def regression_baseline_predict(y_train, n):
    return np.full(n, np.mean(y_train))


def classification_baseline_predict(y_train, n):
    values, counts = np.unique(y_train, return_counts=True)
    majority_class = values[np.argmax(counts)]
    return np.full(n, majority_class)