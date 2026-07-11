import pandas as pd
import numpy as np


def load_and_clean(path):
    df = pd.read_csv(path, sep=";") #error: displaying single column in o/p for df.shape fix -> sep = ";"

    df_proc = df.dropna(axis=1, how="all") #dropping fully empty features "Unnamed: 15" & "Unnamed: 16"
    df_proc = df_proc.dropna(axis=0, how="all") #dropping empty rows
    # features with missing values are: PT08.S2(NMHC),NOx(GT),PT08.S3(NOx),NO2(GT),PT08.S4(NO2),PT08.S5(O3),PT08.S1(CO),NMHC(GT)

    # from missing_percent_report() output it can be observed that the feature "NMHC(GT)" can be safely dropped since it doesn't influence the dataset (90%)
    df_proc = df_proc.drop(columns='NMHC(GT)')

    #converting str dtype features to float
    df_proc["CO(GT)"] = df_proc["CO(GT)"].str.replace(",", ".", regex=False).astype(float)
    df_proc["C6H6(GT)"] = df_proc["C6H6(GT)"].str.replace(",", ".", regex=False).astype(float)
    df_proc["T"] = df_proc["T"].str.replace(",", ".", regex=False).astype(float)
    df_proc["RH"] = df_proc["RH"].str.replace(",", ".", regex=False).astype(float)
    df_proc["AH"] = df_proc["AH"].str.replace(",", ".", regex=False).astype(float)

    # Replace dataset missing-value marker (-200) with NaN
    df_proc.replace(-200, np.nan, inplace=True)

    return df_proc


def train_val_test_split(X, y, val_size=0.15, test_size=0.15, seed=42):
    n = X.shape[0]
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)

    test_n = int(n * test_size)
    val_n = int(n * val_size)

    test_idx = idx[:test_n]
    val_idx = idx[test_n:test_n + val_n]
    train_idx = idx[test_n + val_n:]

    X_train, y_train = X[train_idx], y[train_idx]
    X_val, y_val = X[val_idx], y[val_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    return X_train, y_train, X_val, y_val, X_test, y_test


def fill_nan(X, values):
    X = X.copy()
    for col in range(X.shape[1]):
        mask = np.isnan(X[:, col])
        X[mask, col] = values[col]
    return X


def impute_with_train_median(X_train, X_val, X_test):
    medians = np.nanmedian(X_train, axis=0)

    X_train = fill_nan(X_train, medians)
    X_val = fill_nan(X_val, medians)
    X_test = fill_nan(X_test, medians)

    return X_train, X_val, X_test


def standardize(X_train, X_val, X_test):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    std[std == 0] = 1.0

    X_train = (X_train - mean) / std
    X_val = (X_val - mean) / std
    X_test = (X_test - mean) / std

    return X_train, X_val, X_test, mean, std


def missing_percent_report(df_proc):
    missing = df_proc.isnull().sum()
    missing_percent = (missing / len(df_proc)) * 100

    print(pd.DataFrame({
        "Missing": missing,
        "Percent": missing_percent
    }).sort_values("Percent", ascending=False))


def analyze_feature(df_proc, column):
    import matplotlib.pyplot as plt

    print(df_proc[column].describe())
    plt.hist(df_proc[column].dropna(), bins=30)
    plt.title(column)
    plt.show()