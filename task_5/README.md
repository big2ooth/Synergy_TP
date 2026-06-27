# Task 5: Matplotlib Visualization

## Objective
Generate three properly labeled plots from the cleaned dataset produced in Task 4.

## Setup
```bash
pip install pandas matplotlib
```

## Run Command
```bash
python task_5/src/main.py task_4/output/cleaned_students.csv task_5/output
```

## Expected Output Files
- `task_5/output/domain_average_score.png` — bar chart of average score per domain
- `task_5/output/attendance_vs_score.png` — scatter plot of attendance vs score
- `task_5/output/submission_status_count.png` — bar chart of submitted vs not submitted
- `task_5/output/plot_summary.md` — explanation of each plot

## Logic Overview
**visualize.py** has one function per plot. Each function loads nothing on its own — it receives the dataframe and an output path, generates the plot, saves it with `savefig()`, and closes it with `close()` so no window opens during execution. `tight_layout()` is used on every plot to prevent label clipping.

**main.py** loads the cleaned CSV from Task 4, calls each plot function, and writes the plot summary.