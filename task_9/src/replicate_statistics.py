import numpy as np
from scipy import stats 
import pandas as pd

group_cols = ["domain", "condition", "input_type", "input_value", "input_unit", "signal_unit"]  #grouping features in a list

def load_data(file_path: str)->pd.DataFrame:  #reading input csv 
    df = pd.read_csv(file_path)
    return df 

def calculate_confidence_interval(mean: float, std: float, n: int)-> tuple[float,float]:
    if n<2 or std is None or np.isnan(std):
        return(np.nan,np.nan)
    standard_error = std/np.sqrt(n)
    t_critical = stats.t.ppf(0.975, df=n-1)
    margin = t_critical * standard_error
    return (mean - margin, mean + margin)

def assign_stability_flag(coefficient_of_variation: float) -> str:
    if coefficient_of_variation is None or np.isnan(coefficient_of_variation):
        return "unreliable"
    if coefficient_of_variation<=0.05:
        return "stable"
    if coefficient_of_variation <= 0.15:
        return "moderate"
    return "unstable"

def calculate_replicate_statistics(df: pd.DataFrame)->pd.DataFrame:
    records = []
    for group_keys, group_df in df.groupby(group_cols, dropna = False):
        signal_values = group_df["signal"].dropna()
        n = len(signal_values)
        mean_signal = signal_values.mean() if n > 0 else np.nan
        median_signal = signal_values.median() if n > 0 else np.nan
        minimum_signal = signal_values.min() if n > 0 else np.nan
        maximum_signal = signal_values.max() if n > 0 else np.nan
        if n>=2:
            variance_signal = signal_values.var(ddof=1)
            standard_deviation_signal = signal_values.std(ddof=1)
            standard_error_signal = standard_deviation_signal / np.sqrt(n)
            ci_lower, ci_upper = calculate_confidence_interval(mean_signal, standard_deviation_signal, n)
            coefficient_of_variation = (standard_deviation_signal / mean_signal if mean_signal != 0 else np.nan)
        else:
            variance_signal = np.nan
            standard_deviation_signal = np.nan
            standard_error_signal = np.nan
            ci_lower, ci_upper = (np.nan, np.nan)
            coefficient_of_variation = np.nan

        stability_flag = assign_stability_flag(coefficient_of_variation)

        record = dict(zip(group_cols, group_keys))
        record.update({
            "replicate_count": n,
            "mean_signal": mean_signal,
            "median_signal": median_signal,
            "variance_signal": variance_signal,
            "standard_deviation_signal": standard_deviation_signal,
            "standard_error_signal": standard_error_signal,
            "confidence_interval_lower": ci_lower,
            "confidence_interval_upper": ci_upper,
            "coefficient_of_variation": coefficient_of_variation,
            "minimum_signal": minimum_signal,
            "maximum_signal": maximum_signal,
            "stability_flag": stability_flag,
        })
        records.append(record)

    summary_df = pd.DataFrame(records)
    return summary_df

def save_replicate_summary(summary_df: pd.DataFrame, output_path: str)->None:
    summary_df.to_csv(output_path,index=False)
