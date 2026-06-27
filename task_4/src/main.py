import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from clean_data import (
    load_data, generate_summary, remove_duplicates, standardize_domains,
    clean_attendance, clean_scores, clean_study_hours, clean_height,
    clean_weight, clean_submitted, handle_missing_values,
    save_cleaned_data, write_report
)
from validate_data import validate_cleaned_data

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def write_json(data: dict, path: str):
    with open(path, "w") as f:
        json.dump(data, f, indent=4, default=str)


def main():
    if len(sys.argv) < 3:
        print("Usage: python task_4/src/main.py <input_csv> <output_csv>")
        sys.exit(1)

    input_path  = sys.argv[1]
    output_path = sys.argv[2]
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load
    df = load_data(input_path)

    # Summary before cleaning
    write_json(generate_summary(df), os.path.join(OUTPUT_DIR, "summary_before.json"))

    # Clean
    df = remove_duplicates(df)
    df = standardize_domains(df)
    df = clean_attendance(df)
    df = clean_scores(df)
    df = clean_study_hours(df)
    df = clean_height(df)
    df = clean_weight(df)
    df = clean_submitted(df)
    df = handle_missing_values(df)

    # Summary after cleaning
    write_json(generate_summary(df), os.path.join(OUTPUT_DIR, "summary_after.json"))

    # Validate
    print("\n[Validation]")
    validate_cleaned_data(df)

    # Save
    save_cleaned_data(df, output_path)
    write_report(os.path.join(OUTPUT_DIR, "cleaning_report.md"))

    print("\nTask 4 complete.")


if __name__ == "__main__":
    main()