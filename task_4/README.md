# Task 4: Messy CSV Cleaning

## Objective
Clean a messy CSV dataset using pandas and produce a clean dataset, validation checks, and a written cleaning report.

## Setup
```bash
pip install pandas
```

## Run Command
```bash
python task_4/src/main.py task_4/data/messy_students.csv task_4/output/cleaned_students.csv
```

## Expected Output Files
- `task_4/output/cleaned_students.csv` — fully cleaned dataset
- `task_4/output/summary_before.json` — shape, missing values, duplicates before cleaning
- `task_4/output/summary_after.json` — same stats after cleaning
- `task_4/output/cleaning_report.md` — every cleaning decision documented

## Logic Overview
**clean_data.py** handles all cleaning in individual functions:
- Removes duplicate rows
- Standardizes domain names using a mapping dictionary
- Strips % from attendance and removes rows with values below 0 or above 100
- Converts word numbers (nine, two) to integers for score and study_hours
- Converts height to cm (handles both metres and cm formats), renames to height_cm
- Strips kg suffix from weight, renames to weight_kg
- Normalizes submitted values (Yes, Y, N) to yes/no
- Imputes remaining missing numeric values with column median

**validate_data.py** runs 9 checks on the cleaned dataframe and prints PASS/FAIL for each.

**main.py** orchestrates all steps and writes all output files.

## Cleaning Report
See `task_4/output/cleaning_report.md` for a full explanation of every decision made during cleaning.