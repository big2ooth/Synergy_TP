# Task 3: Manual CSV Parser and Pandas Comparison

## Objective
Build a CSV parser from scratch using only Python file I/O,
then replicate the same analysis with pandas and compare outputs.

## Folder Structure
task_3/
  README.md
  data/
    submissions.csv
  output/
    manual_summary.json
    pandas_summary.json
    comparison_report.md
  src/
    manual_parser.py
    pandas_parser.py
    main.py

## Required Packages
pandas

## Setup
pip install pandas

## Run Command
python task_3/src/main.py task_3/data/submissions.csv

## Expected Output Files
- task_3/output/manual_summary.json
- task_3/output/pandas_summary.json
- task_3/output/comparison_report.md

## Logic Overview
manual_parser.py  — opens CSV with open(), splits lines manually,
                    builds list of dicts, handles empty/malformed rows
pandas_parser.py  — same calculations via pandas groupby/idxmax
main.py           — orchestrates both, writes JSONs, generates report