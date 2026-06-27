import json
import pandas as pd


def read_csv_pandas(file_path: str):
    return pd.read_csv(file_path)


def calculate_summary_pandas(df) -> dict:
    df = df.copy()
    df["submitted"] = df["submitted"].str.strip().str.lower()
    df["score"]     = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)

    total        = len(df)
    submitted_df = df[df["submitted"] == "yes"]
    missing_df   = df[df["submitted"] == "no"]
    avg_score    = round(df["score"].mean(), 2)
    highest      = df.loc[df["score"].idxmax()]
    lowest_sub   = submitted_df.loc[submitted_df["score"].idxmin()] \
                   if not submitted_df.empty else None

    domain_avg = df.groupby("domain")["score"].mean().round(2).to_dict()
    below_5    = df[df["score"] < 5]["name"].tolist()

    return {
        "total_students":      total,
        "submitted_count":     int(len(submitted_df)),
        "missing_submissions": int(len(missing_df)),
        "average_score":       avg_score,
        "highest_scorer":      {"name": highest["name"], "score": int(highest["score"])},
        "lowest_scorer_among_submitted": (
            {"name": lowest_sub["name"], "score": int(lowest_sub["score"])}
            if lowest_sub is not None else None
        ),
        "domain_wise_average_score":   domain_avg,
        "students_who_did_not_submit": missing_df["name"].tolist(),
        "students_scoring_below_5":    below_5,
    }


def write_json(data: dict, output_path: str) -> None:
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Written: {output_path}")