import sys
import os
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data_utils import load_and_clean, train_val_test_split, impute_with_train_median, standardize
from linear_regression_gd import LinearRegressionGD
from logistic_regression_gd import LogisticRegressionGD
from kmeans import KMeans, silhouette_score
from baselines import regression_baseline_predict, classification_baseline_predict
import metrics as m


FEATURE_COLS = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH",
]


def run_regression(df, output_dir):
    target_col = "CO(GT)"

    data = df.dropna(subset=[target_col]).copy()
    X = data[FEATURE_COLS].to_numpy(dtype=float)
    y = data[target_col].to_numpy(dtype=float)
    print("y min:", y.min())
    print("y max:", y.max())
    print("y mean:", y.mean())

    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)
    print("Train mean:", y_train.mean())
    print("Train min:", y_train.min())
    print("Train max:", y_train.max())

    print("Test mean:", y_test.mean())
    print("Test min:", y_test.min())
    print("Test max:", y_test.max())
    X_train, X_val, X_test = impute_with_train_median(X_train, X_val, X_test)
    X_train, X_val, X_test, mean, std = standardize(X_train, X_val, X_test)

    model = LinearRegressionGD(lr=0.05, n_iters=2000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    baseline_pred = regression_baseline_predict(y_train, len(y_test))

    results = {
        "model": {
            "mae": m.mae(y_test, y_pred),
            "mse": m.mse(y_test, y_pred),
            "rmse": m.rmse(y_test, y_pred),
            "r_squared": m.r_squared(y_test, y_pred),
        },
        "baseline": {
            "mae": m.mae(y_test, baseline_pred),
            "mse": m.mse(y_test, baseline_pred),
            "rmse": m.rmse(y_test, baseline_pred),
            "r_squared": m.r_squared(y_test, baseline_pred),
        },
    }

    with open(os.path.join(output_dir, "regression_metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    pred_df = pd.DataFrame({
        "actual": y_test,
        "predicted": y_pred,
        "baseline_predicted": baseline_pred,
    })
    pred_df.to_csv(os.path.join(output_dir, "regression_predictions.csv"), index=False)

    plt.figure()
    plt.plot(model.loss_history)
    plt.xlabel("iteration")
    plt.ylabel("MSE loss")
    plt.title("linear regression training loss")
    plt.savefig(os.path.join(output_dir, "regression_loss_curve.png"))
    plt.close()

    plt.figure()
    plt.scatter(y_test, y_pred, alpha=0.5)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    plt.plot(lims, lims, linestyle="--")
    plt.xlabel("actual CO(GT)")
    plt.ylabel("predicted CO(GT)")
    plt.title("actual vs predicted")
    plt.savefig(os.path.join(output_dir, "actual_vs_predicted.png"))
    plt.close()

    return results


def run_classification(df, output_dir):
    target_source_col = "CO(GT)"

    data = df.dropna(subset=[target_source_col]).copy()
    median_co = data[target_source_col].median()
    data["high_co"] = (data[target_source_col] > median_co).astype(int)

    X = data[FEATURE_COLS].to_numpy(dtype=float)
    y = data["high_co"].to_numpy(dtype=int)

    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)
    X_train, X_val, X_test = impute_with_train_median(X_train, X_val, X_test)
    X_train, X_val, X_test, mean, std = standardize(X_train, X_val, X_test)

    model = LogisticRegressionGD(lr=0.05, n_iters=2000)
    model.fit(X_train, y_train.astype(float))

    y_pred = model.predict(X_test)
    baseline_pred = classification_baseline_predict(y_train, len(y_test))

    tp, tn, fp, fn = m.confusion_matrix(y_test, y_pred)

    results = {
        "model": {
            "accuracy": m.accuracy(y_test, y_pred),
            "precision": m.precision(y_test, y_pred),
            "recall": m.recall(y_test, y_pred),
            "f1_score": m.f1_score(y_test, y_pred),
        },
        "baseline": {
            "accuracy": m.accuracy(y_test, baseline_pred),
            "precision": m.precision(y_test, baseline_pred),
            "recall": m.recall(y_test, baseline_pred),
            "f1_score": m.f1_score(y_test, baseline_pred),
        },
        "confusion_matrix": {
            "tp": int(tp),
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
        },
    }

    with open(os.path.join(output_dir, "classification_metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    pred_df = pd.DataFrame({
        "actual": y_test,
        "predicted": y_pred,
        "baseline_predicted": baseline_pred,
    })
    pred_df.to_csv(os.path.join(output_dir, "classification_predictions.csv"), index=False)

    plt.figure()
    plt.plot(model.loss_history)
    plt.xlabel("iteration")
    plt.ylabel("binary cross entropy loss")
    plt.title("logistic regression training loss")
    plt.savefig(os.path.join(output_dir, "classification_loss_curve.png"))
    plt.close()

    matrix = np.array([[tn, fp], [fn, tp]])
    plt.figure()
    plt.imshow(matrix, cmap="Blues")
    plt.xticks([0, 1], ["pred 0", "pred 1"])
    plt.yticks([0, 1], ["actual 0", "actual 1"])
    for i in range(2):
        for j in range(2):
            plt.text(j, i, str(matrix[i, j]), ha="center", va="center")
    plt.title("confusion matrix")
    plt.colorbar()
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    plt.close()

    return results


def run_clustering(df, output_dir):
    feature_cols = ["T", "RH"]
    data = df.dropna(subset=feature_cols).copy()

    X = data[feature_cols].to_numpy(dtype=float)
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std == 0] = 1.0
    X_scaled = (X - mean) / std

    model = KMeans(k=3, n_iters=100)
    labels = model.fit(X_scaled)
    sil_score = silhouette_score(X_scaled, labels)

    unique, counts = np.unique(labels, return_counts=True)
    cluster_counts = {int(u): int(c) for u, c in zip(unique, counts)}

    results = {
        "inertia": model.inertia_,
        "silhouette_score": sil_score,
        "cluster_counts": cluster_counts,
    }

    with open(os.path.join(output_dir, "clustering_metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    assignments_df = pd.DataFrame({
        "T": X[:, 0],
        "RH": X[:, 1],
        "cluster": labels,
    })
    assignments_df.to_csv(os.path.join(output_dir, "clustering_assignments.csv"), index=False)

    plt.figure()
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", alpha=0.5)
    plt.xlabel("T")
    plt.ylabel("RH")
    plt.title("kmeans clusters (T vs RH)")
    plt.savefig(os.path.join(output_dir, "clustering_plot.png"))
    plt.close()

    return results


def write_model_comparison(output_dir, reg_results, clf_results, clus_results):
    lines = []
    lines.append("# Model Comparison\n\n")

    lines.append("## Regression\n")
    lines.append("Target: CO(GT), predicted from PT08 sensor readings and weather features.\n")
    lines.append(f"Model RMSE: {reg_results['model']['rmse']:.4f}, Baseline RMSE: {reg_results['baseline']['rmse']:.4f}\n")
    lines.append(f"Model R2: {reg_results['model']['r_squared']:.4f}, Baseline R2: {reg_results['baseline']['r_squared']:.4f}\n\n")

    lines.append("## Classification\n")
    lines.append("Target: high_co, 1 if CO(GT) is above the training median, else 0.\n")
    lines.append(f"Model accuracy: {clf_results['model']['accuracy']:.4f}, Baseline accuracy: {clf_results['baseline']['accuracy']:.4f}\n")
    lines.append(f"Model F1: {clf_results['model']['f1_score']:.4f}, Baseline F1: {clf_results['baseline']['f1_score']:.4f}\n\n")

    lines.append("## Clustering\n")
    lines.append("Features used: T, RH. Labels were not used during clustering.\n")
    lines.append(f"Inertia: {clus_results['inertia']:.4f}\n")
    lines.append(f"Silhouette score: {clus_results['silhouette_score']:.4f}\n")

    with open(os.path.join(output_dir, "model_comparison.md"), "w") as f:
        f.writelines(lines)


def write_error_analysis(output_dir):
    lines = []
    lines.append("# Error Analysis\n\n")
    lines.append("See regression_predictions.csv and classification_predictions.csv for the raw errors.\n")
    lines.append("Fill in specific large error examples and reasoning here.\n")

    with open(os.path.join(output_dir, "error_analysis.md"), "w") as f:
        f.writelines(lines)


def main():
    if len(sys.argv) != 3:
        print("usage: python main.py <path to AirQualityUCI.csv> <output dir>")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    df = load_and_clean(csv_path)
    print(df.head())
    print(df.dtypes)
    print(df["CO(GT)"].describe())
    print("Remaining -200s in CO:", (df["CO(GT)"] == -200).sum())
    print("NaNs in CO:", df["CO(GT)"].isna().sum())

    reg_results = run_regression(df, output_dir)
    clf_results = run_classification(df, output_dir)
    clus_results = run_clustering(df, output_dir)

    write_model_comparison(output_dir, reg_results, clf_results, clus_results)
    write_error_analysis(output_dir)

    print("pipeline complete, outputs written to", output_dir)


if __name__ == "__main__":
    main()