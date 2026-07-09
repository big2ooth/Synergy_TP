import numpy as np
import pandas as pd


def add_rolling_average(df: pd.DataFrame) -> pd.DataFrame:

    df = df.sort_values(["domain", "condition", "time_step"]).copy()
    df["rolling_average_signal"] = (
        df.groupby(["domain", "condition"])["signal"]
        .transform(lambda s: s.rolling(window=3, min_periods=1).mean())
    )
    return df


def add_normalized_signal(df: pd.DataFrame) -> pd.DataFrame:
    baseline = df["baseline_signal"]
    valid = baseline.notna() & (baseline != 0)
    df["normalized_signal"] = np.where(valid, df["signal"] / baseline, np.nan)
    return df


def add_power_feature(df: pd.DataFrame) -> pd.DataFrame:
    is_electronics = df["domain"] == "Electronics"
    has_values = df["voltage_v"].notna() & df["current_a"].notna()
    valid = is_electronics & has_values
    df["power_w"] = np.where(valid, df["voltage_v"] * df["current_a"], np.nan)
    return df


def add_error_percent(df: pd.DataFrame) -> pd.DataFrame:
    expected = df["expected_signal"]
    valid = expected.notna() & (expected != 0)
    df["error_percent"] = np.where(
        valid, ((df["signal"] - expected) / expected) * 100, np.nan
    )
    return df


def add_stress_ratio(df: pd.DataFrame) -> pd.DataFrame:
    is_mechanical = df["domain"] == "Mechanical"
    ref = df["reference_stress_mpa"]
    valid = is_mechanical & df["stress_mpa"].notna() & ref.notna() & (ref != 0)
    df["stress_ratio"] = np.where(valid, df["stress_mpa"] / ref, np.nan)
    return df


def add_ml_readiness_flag(df: pd.DataFrame) -> pd.DataFrame:
    has_core_values = (
        df["signal"].notna()
        & df["expected_signal"].notna()
        & df["input_value"].notna()
        & df["domain"].notna()
        & df["condition"].notna()
    )

    if "stability_flag" in df.columns:
        stable_group = ~df["stability_flag"].isin(["unstable", "unreliable"])
    else:
        stable_group = True

    df["ml_ready"] = has_core_values & stable_group
    return df


def save_engineered_features(df: pd.DataFrame, output_path: str) -> None:
    """Save the engineered features DataFrame to a CSV file."""
    df.to_csv(output_path, index=False)