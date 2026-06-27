import pandas as pd
import json


def load_data(file_path: str):
    return pd.read_csv(file_path)


def generate_summary(df) -> dict:
    return {
        "total_rows": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "unique_domains": df["domain"].unique().tolist() if "domain" in df.columns else []
    }


def remove_duplicates(df):
    df = df.drop_duplicates()
    return df.reset_index(drop=True)


def standardize_domains(df):
    mapping = {
        "ml": "ML", "ML": "ML", "MACHINE LEARNING": "ML",
        "web": "Web", "Web Dev": "Web", "web development": "Web", "Web": "Web",
        "electronics": "Electronics", "Electronics": "Electronics",
        "Mechanical": "Mechanical"
    }
    df["domain"] = df["domain"].str.strip().map(mapping)
    return df


def clean_attendance(df):
    # Removing % and convert to float
    def parse_attendance(val):
        if pd.isna(val):
            return None
        val = str(val).replace("%", "").strip()
        try:
            return float(val)
        except ValueError:
            return None

    df["attendance_percent"] = df["attendance_percent"].apply(parse_attendance)

    # Removing rows where attendance is below 0 or above 100
    df = df[df["attendance_percent"].isna() | df["attendance_percent"].between(0, 100)]
    return df.reset_index(drop=True)


def clean_scores(df):
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    def parse_score(val):
        if pd.isna(val):
            return None
        val = str(val).strip().lower()
        if val in word_to_num:
            return float(word_to_num[val])
        try:
            return float(val)
        except ValueError:
            return None

    df["score"] = df["score"].apply(parse_score)
    median = df["score"].median()
    df["score"] = df["score"].fillna(median)
    return df


def clean_study_hours(df):
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    def parse_hours(val):
        if pd.isna(val):
            return None
        val = str(val).strip().lower()
        if val in word_to_num:
            return float(word_to_num[val])
        try:
            return float(val)
        except ValueError:
            return None

    df["study_hours"] = df["study_hours"].apply(parse_hours)
    median = df["study_hours"].median()
    df["study_hours"] = df["study_hours"].fillna(median)
    return df


def clean_height(df):
    def parse_height(val):
        if pd.isna(val):
            return None
        val = str(val).strip().lower()
        if "cm" in val:
            return float(val.replace("cm", "").strip())
        elif "m" in val:
            return float(val.replace("m", "").strip()) * 100
        return None

    df["height_cm"] = df["height"].apply(parse_height)
    df = df.drop(columns=["height"])
    return df


def clean_weight(df):
    def parse_weight(val):
        if pd.isna(val):
            return None
        val = str(val).strip().lower().replace("kg", "").strip()
        try:
            return float(val)
        except ValueError:
            return None

    df["weight_kg"] = df["weight"].apply(parse_weight)
    df = df.drop(columns=["weight"])
    return df


def clean_submitted(df):
    mapping = {"yes": "yes", "y": "yes", "no": "no", "n": "no"}
    df["submitted"] = df["submitted"].str.strip().str.lower().map(mapping)
    return df


def handle_missing_values(df):
    # Impute remaining numeric nulls with median
    for col in ["attendance_percent", "height_cm", "weight_kg"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Missing submitted defaults to no
    df["submitted"] = df["submitted"].fillna("no")
    return df


def validate_cleaned_data(df) -> bool:
    valid_domains = {"ML", "Web", "Electronics", "Mechanical"}
    critical_cols = ["student_id", "name", "domain", "attendance_percent",
                     "score", "study_hours", "height_cm", "weight_kg", "submitted"]
    passed = True

    checks = [
        (df["student_id"].duplicated().sum() == 0, "No duplicate student_id"),
        (df["attendance_percent"].between(0, 100).all(), "attendance_percent in [0, 100]"),
        (pd.to_numeric(df["score"], errors="coerce").notna().all(), "score is numeric"),
        (pd.to_numeric(df["study_hours"], errors="coerce").notna().all(), "study_hours is numeric"),
        (pd.to_numeric(df["height_cm"], errors="coerce").notna().all(), "height_cm is numeric"),
        (pd.to_numeric(df["weight_kg"], errors="coerce").notna().all(), "weight_kg is numeric"),
        (df["submitted"].isin({"yes", "no"}).all(), "submitted is yes/no only"),
        (df["domain"].isin(valid_domains).all(), "domain values are valid"),
        (df[critical_cols].isnull().sum().sum() == 0, "No nulls in critical columns"),
    ]

    for condition, msg in checks:
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {msg}")
        if not condition:
            passed = False

    return passed


def save_cleaned_data(df, output_path: str) -> None:
    cols = ["student_id", "name", "domain", "attendance_percent",
            "score", "study_hours", "height_cm", "weight_kg", "submitted"]
    df[cols].to_csv(output_path, index=False)


def write_report(report_path: str) -> None:
    report = """# Cleaning Report — Task 4

## Issues found and fixed

### 1. Duplicate rows
S005 (Rohan) appeared twice. The duplicate row was removed using drop_duplicates().

### 2. Domain standardization
Values like `ml`, `MACHINE LEARNING`, `Web Dev`, `web development`, `electronics`
were mapped to canonical labels: ML, Web, Electronics, Mechanical.

### 3. attendance_percent
Stripped the % symbol and converted to float.
S007 (Dev) had -10 and S008 (Naina) had 105% — both are impossible values.
These rows were removed rather than imputed to avoid fabricating attendance data.
Remaining missing values were filled with the column median.

### 4. score
Word numbers (nine → 9) were converted using a lookup dictionary.
S009 (Omkar) had a missing score — filled with the column median.

### 5. study_hours
Word numbers (two → 2) were converted using the same lookup dictionary.

### 6. height → height_cm
Values in metres (1.62 m, 1.55 m) were multiplied by 100 to get cm.
Values already in cm had the unit text stripped.
Column renamed from height to height_cm.

### 7. weight → weight_kg
Stripped the kg suffix and converted to float.
S003 (Kabir) had a missing weight — filled with the column median.
Column renamed from weight to weight_kg.

### 8. submitted
Inconsistent values (Yes, Y, N) were normalized to yes/no using a mapping dict.

## Summary table

| Issue | Rows affected | Action |
|---|---|---|
| Duplicate row | S005 | Removed |
| Invalid attendance | S007, S008 | Rows removed |
| Word score | S004 (nine) | Converted to 9 |
| Word study_hours | S005 (two) | Converted to 2 |
| Height in metres | S002, S010 | Converted to cm |
| Missing weight | S003 | Median imputation |
| Missing score | S009 | Median imputation |
| Inconsistent submitted | S002, S006, S009 | Normalized to yes/no |
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)