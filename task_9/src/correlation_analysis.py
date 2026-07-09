import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from scipy import stats

relationships = [
    {
        "relationship": "Biochem: signal vs concentration",
        "domain": "Biochem",
        "input_type": "concentration",
        "x_col": "input_value",
        "y_col":"signal"
    },
    {
        "relationship": "Electronics: signal vs load",
        "domain": "Electronics",
        "input_type": "load",
        "x_col": "input_value",
        "y_col": "signal",
    },
    {
        "relationship": "Electronics: signal vs temperature",
        "domain": "Electronics",
        "input_type": None,
        "x_col": "temperature_c",
        "y_col": "signal",
    },
    {
         "relationship": "Mechanical: signal vs load",
        "domain": "Mechanical",
        "input_type": "load",
        "x_col": "input_value",
        "y_col": "signal",
    },
    {
        "relationship": "Mechanical: stress_mpa vs load",
        "domain": "Mechanical",
        "input_type": "load",
        "x_col": "input_value",
        "y_col": "stress_mpa",
    },
]


def _subset_for_relationship(df: pd.DataFrame, spec: dict) -> pd.DataFrame:
    subset = df[df["domain"] == spec["domain"]]
    if spec["input_type"] is not None:
        subset = subset[subset["input_type"] == spec["input_type"]]
    subset = subset[[spec["x_col"], spec["y_col"]]].dropna()
    return subset


def fit_calibration_line(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Fit a simple linear regression y = slope * x + intercept."""
    slope, intercept, _, _, _ = stats.linregress(x, y)
    return slope, intercept


def calculate_fit_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    """Return R-squared, mean absolute error, and root mean squared error."""
    residuals = y_true - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else np.nan
    mae = np.mean(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals ** 2))
    return r_squared, mae, rmse


def calculate_correlations(df: pd.DataFrame) -> pd.DataFrame:
    records = []

    for spec in relationships:
        subset = _subset_for_relationship(df, spec)
        x = subset[spec["x_col"]].to_numpy(dtype=float)
        y = subset[spec["y_col"]].to_numpy(dtype=float)
        n = len(x)

        if n >= 2 and np.std(x) > 0:
            pearson_r, _ = stats.pearsonr(x, y)
            spearman_r, _ = stats.spearmanr(x, y)
            slope, intercept = fit_calibration_line(x, y)
            y_pred = slope * x + intercept
            r_squared, mae, rmse = calculate_fit_metrics(y, y_pred)
        else:
            pearson_r = np.nan
            spearman_r = np.nan
            slope, intercept, r_squared, mae, rmse = (np.nan,) * 5

        records.append({
            "relationship": spec["relationship"],
            "domain": spec["domain"],
            "x_variable": spec["x_col"],
            "y_variable": spec["y_col"],
            "n_samples": n,
            "pearson_correlation": pearson_r,
            "spearman_correlation": spearman_r,
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "mean_absolute_error": mae,
            "root_mean_squared_error": rmse,
        })

    return pd.DataFrame(records)

def plot_calibration_curve(replicate_summary_df: pd.DataFrame, domain: str, output_path: str) -> None:
    subset = replicate_summary_df[replicate_summary_df["domain"] == domain].copy()
    subset = subset.sort_values("input_value")

    x = subset["input_value"].to_numpy(dtype=float)
    y = subset["mean_signal"].to_numpy(dtype=float)
    ci_lower = subset["confidence_interval_lower"].to_numpy(dtype=float)
    ci_upper = subset["confidence_interval_upper"].to_numpy(dtype=float)

    # Error bars: half-width of the CI; fall back to 0 where CI is unreliable
    lower_err = np.where(np.isnan(ci_lower), 0, y - ci_lower)
    upper_err = np.where(np.isnan(ci_upper), 0, ci_upper - y)

    plt.figure(figsize=(6, 4.5))
    plt.errorbar(
        x, y, yerr=[lower_err, upper_err],
        fmt="o-", capsize=4, color="#8B1E3F", ecolor="#444444",
        markerfacecolor="#8B1E3F", linewidth=1.5,
    )
    plt.xlabel("Input Value")
    plt.ylabel("Mean Signal")
    plt.title(f"Calibration Curve: {domain}")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_signal_input_scatter(df: pd.DataFrame, output_path: str) -> None:
    """Scatter plot of raw signal versus input_value, colored by domain."""
    plt.figure(figsize=(6.5, 5))
    colors = {"Biochem": "#2E7D32", "Electronics": "#1565C0", "Mechanical": "#8B1E3F"}

    for domain, group in df.groupby("domain"):
        plt.scatter(
            group["input_value"], group["signal"],
            label=domain, color=colors.get(domain, "#555555"), alpha=0.8, edgecolor="black"
        )

    plt.xlabel("Input Value")
    plt.ylabel("Raw Signal")
    plt.title("Raw Signal vs Input Value (All Domains)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
