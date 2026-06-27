import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from visualize import (
    load_cleaned_data,
    plot_domain_average_score,
    plot_attendance_vs_score,
    plot_submission_status_count,
    write_plot_summary,
)


def main():
    if len(sys.argv) < 3:
        print("Usage: python task_5/src/main.py <cleaned_csv> <output_dir>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    df = load_cleaned_data(input_path)

    plot_domain_average_score(df,    os.path.join(output_dir, "domain_average_score.png"))
    plot_attendance_vs_score(df,     os.path.join(output_dir, "attendance_vs_score.png"))
    plot_submission_status_count(df, os.path.join(output_dir, "submission_status_count.png"))
    write_plot_summary(              os.path.join(output_dir, "plot_summary.md"))

    print("Task 5 complete.")


if __name__ == "__main__":
    main()