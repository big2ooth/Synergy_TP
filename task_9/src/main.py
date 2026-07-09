import os
import sys

import pandas as pd

from replicate_statistics import (
    load_data,
    calculate_replicate_statistics,
    save_replicate_summary,
    group_cols,
)
from correlation_analysis import (
    calculate_correlations,
    plot_calibration_curve,
    plot_signal_input_scatter,
)
from feature_engineering import (
    add_rolling_average,
    add_normalized_signal,
    add_power_feature,
    add_error_percent,
    add_stress_ratio,
    add_ml_readiness_flag,
    save_engineered_features,
)


def main(input_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    # --- Part 1: Replicate statistics ---
    df = load_data(input_path)
    replicate_summary_df = calculate_replicate_statistics(df)
    save_replicate_summary(
        replicate_summary_df, os.path.join(output_dir, "replicate_summary.csv")
    )

    # --- Part 2: Calibration and correlation analysis ---
    correlation_summary_df = calculate_correlations(df)
    correlation_summary_df.to_csv(
        os.path.join(output_dir, "correlation_summary.csv"), index=False
    )
    # calibration_summary.csv mirrors the correlation summary; slope, intercept,
    # R-squared, MAE, and RMSE come from the same simple linear calibration fit.
    correlation_summary_df.to_csv(
        os.path.join(output_dir, "calibration_summary.csv"), index=False
    )

    for domain in ["Biochem", "Electronics", "Mechanical"]:
        plot_calibration_curve(
            replicate_summary_df, domain,
            os.path.join(output_dir, f"calibration_curve_{domain.lower()}.png"),
        )
    plot_signal_input_scatter(
        df, os.path.join(output_dir, "correlation_signal_input.png")
    )

    # --- Part 3: Feature engineering ---
    features_df = df.copy()
    features_df = add_rolling_average(features_df)
    features_df = add_normalized_signal(features_df)
    features_df = add_power_feature(features_df)
    features_df = add_error_percent(features_df)
    features_df = add_stress_ratio(features_df)

    # Merge stability_flag from the replicate summary onto each row so
    # ml-readiness reflects replicate-group reliability.
    stability_lookup = replicate_summary_df[group_cols + ["stability_flag"]]
    features_df = features_df.merge(stability_lookup, on=group_cols, how="left")

    features_df = add_ml_readiness_flag(features_df)

    save_engineered_features(
        features_df, os.path.join(output_dir, "engineered_features.csv")
    )

    ml_ready_df = features_df[features_df["ml_ready"]].copy()
    ml_ready_df.to_csv(os.path.join(output_dir, "ml_ready_dataset.csv"), index=False)

    print(f"Pipeline complete. Outputs written to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv_path> <output_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])