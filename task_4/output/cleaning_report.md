# Cleaning Report — Task 4

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
