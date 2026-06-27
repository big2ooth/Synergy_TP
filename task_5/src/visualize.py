import pandas as pd
import matplotlib.pyplot as plt


def load_cleaned_data(file_path: str):
    return pd.read_csv(file_path)


def plot_domain_average_score(df, output_path: str) -> None:
    domain_avg = df.groupby("domain")["score"].mean()

    plt.figure()
    plt.bar(domain_avg.index, domain_avg.values)
    plt.title("Average Score by Domain")
    plt.xlabel("Domain")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_attendance_vs_score(df, output_path: str) -> None:
    plt.figure()
    plt.scatter(df["attendance_percent"], df["score"])
    plt.title("Attendance vs Score")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_submission_status_count(df, output_path: str) -> None:
    counts = df["submitted"].value_counts()

    plt.figure()
    plt.bar(counts.index, counts.values)
    plt.title("Submission Status Count")
    plt.xlabel("Submitted")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def write_plot_summary(output_path: str) -> None:
    summary = """# Plot Summary

## 1. domain_average_score.png
Bar chart showing the average score for each domain (ML, Web, Electronics).
This helps identify which domain performed best overall in Task 2.

## 2. attendance_vs_score.png
Scatter plot showing the relationship between attendance percentage and score.
Each point represents one student. Helps identify if higher attendance
correlates with better scores.

## 3. submission_status_count.png
Bar chart showing how many students submitted vs did not submit.
Gives a quick overview of overall task completion rate.
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)