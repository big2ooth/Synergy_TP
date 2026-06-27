import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from manual_parser import read_csv_manual, convert_types, calculate_summary, write_json
from pandas_parser  import read_csv_pandas, calculate_summary_pandas, write_json as write_json_pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def generate_comparison_report(manual, pandas_, report_path):
    keys = [
        "total_students", "submitted_count", "missing_submissions",
        "average_score", "highest_scorer", "lowest_scorer_among_submitted",
        "domain_wise_average_score", "students_who_did_not_submit",
        "students_scoring_below_5"
    ]
    lines = ["# Comparison Report: Manual Parser vs Pandas\n"]
    all_match = True

    for key in keys:
        m_val, p_val = manual.get(key), pandas_.get(key)
        match  = m_val == p_val
        if not match: all_match = False
        status = "Match" if match else "Mismatch"
        lines += [f"## {key}\n",
                  f"- Manual : `{m_val}`",
                  f"- Pandas : `{p_val}`",
                  f"- Status : {status}\n"]

    lines.append("---")
    lines.append("**Result: All fields match.**" if all_match
                 else "**Result: Some fields differ.**")

    with open(report_path, "w") as f:
        f.write("\n".join(lines))


def main():
    if len(sys.argv) < 2:
        print("Usage: python task_3/src/main.py task_3/data/submissions.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Manual
    rows           = convert_types(read_csv_manual(csv_path))
    manual_summary = calculate_summary(rows)
    write_json(manual_summary, os.path.join(OUTPUT_DIR, "manual_summary.json"))

    # Pandas
    df             = read_csv_pandas(csv_path)
    pandas_summary = calculate_summary_pandas(df)
    write_json_pd(pandas_summary, os.path.join(OUTPUT_DIR, "pandas_summary.json"))

    # Comparison
    generate_comparison_report(
        manual_summary, pandas_summary,
        os.path.join(OUTPUT_DIR, "comparison_report.md")
    )
    print("Task 3 complete.")


if __name__ == "__main__":
    main()