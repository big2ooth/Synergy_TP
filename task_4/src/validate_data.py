"""
validate_data.py
Validation checks for the cleaned dataset.
"""

import pandas as pd

VALID_DOMAINS = {"ML", "Web", "Electronics", "Mechanical"}
CRITICAL_COLS = ["student_id", "name", "domain", "attendance_percent",
                 "score", "study_hours", "height_cm", "weight_kg", "submitted"]


def validate_cleaned_data(df) -> bool:
    passed = True

    checks = [
        (df["student_id"].duplicated().sum() == 0,              "No duplicate student_id"),
        (df["attendance_percent"].between(0, 100).all(),         "attendance_percent in [0, 100]"),
        (pd.to_numeric(df["score"],       errors="coerce").notna().all(), "score is numeric"),
        (pd.to_numeric(df["study_hours"], errors="coerce").notna().all(), "study_hours is numeric"),
        (pd.to_numeric(df["height_cm"],   errors="coerce").notna().all(), "height_cm is numeric"),
        (pd.to_numeric(df["weight_kg"],   errors="coerce").notna().all(), "weight_kg is numeric"),
        (df["submitted"].isin({"yes", "no"}).all(),              "submitted is yes/no only"),
        (df["domain"].isin(VALID_DOMAINS).all(),                 "domain values are valid"),
        (df[CRITICAL_COLS].isnull().sum().sum() == 0,            "No nulls in critical columns"),
    ]

    for condition, msg in checks:
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {msg}")
        if not condition:
            passed = False

    return passed