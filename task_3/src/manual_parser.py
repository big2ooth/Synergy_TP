import json


def read_csv_manual(file_path: str) -> list[dict]:
    rows = [] 
    with open(file_path, "r") as f:
        lines = f.readlines()

    if not lines:
        return rows

    header = [col.strip() for col in lines[0].strip().split(",")]

    for line_num, line in enumerate(lines[1:], start=2):
        line = line.strip()
        if not line:
            continue  

        values = line.split(",")

        if len(values) != len(header):
            print(f"Warning: Skipping malformed row at line {line_num}: {line}")
            continue

        row = {header[i]: values[i].strip() for i in range(len(header))}
        rows.append(row)

    return rows


def convert_types(rows: list[dict]) -> list[dict]:
    converted = []
    for row in rows:
        try:
            row["score"] = int(row["score"])
        except (ValueError, KeyError):
            print(f"Warning: Could not convert score for row: {row}")
            row["score"] = 0

        submitted_raw = row.get("submitted", "").strip().lower()
        row["submitted"] = "yes" if submitted_raw == "yes" else "no"

        converted.append(row)
    return converted


def calculate_summary(rows: list[dict]) -> dict:
    total = len(rows)
    submitted_rows = [r for r in rows if r["submitted"] == "yes"]
    missing_rows = [r for r in rows if r["submitted"] == "no"]

    all_scores = [r["score"] for r in rows]
    avg_score = round(sum(all_scores) / total, 2) if total > 0 else 0

    highest = max(rows, key=lambda r: r["score"])
    submitted_only = [r for r in rows if r["submitted"] == "yes"]
    lowest_submitted = min(submitted_only, key=lambda r: r["score"]) if submitted_only else None

    
    domain_scores: dict[str, list] = {}
    for r in rows:
        domain = r["domain"]
        domain_scores.setdefault(domain, []).append(r["score"])
    domain_avg = {d: round(sum(s) / len(s), 2) for d, s in domain_scores.items()}

    below_5 = [r["name"] for r in rows if r["score"] < 5]

    return {
        "total_students": total,
        "submitted_count": len(submitted_rows),
        "missing_submissions": len(missing_rows),
        "average_score": avg_score,
        "highest_scorer": {"name": highest["name"], "score": highest["score"]},
        "lowest_scorer_among_submitted": (
            {"name": lowest_submitted["name"], "score": lowest_submitted["score"]}
            if lowest_submitted else None
        ),
        "domain_wise_average_score": domain_avg,
        "students_who_did_not_submit": [r["name"] for r in missing_rows],
        "students_scoring_below_5": below_5,
    }


def write_json(data: dict, output_path: str) -> None:
    """Write a dictionary to a JSON file."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Written: {output_path}")