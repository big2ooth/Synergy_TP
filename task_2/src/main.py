import sys
from analyzer import *

def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    submissions = read_submissions(input_path)
    submitted = get_submitted_students(submissions)
    missing = get_missing_submissions(submissions)
    avg = calculate_average_score(submissions)
    domain_avg = get_domain_wise_average(submissions)
    highest = max(submitted, key=lambda x: x['score'])
    lowest = min(submitted, key=lambda x: x['score'])
    below_5 = [s['name'] for s in submitted if s['score'] < 5]

    summary = {
        "total_students": len(submissions),
        "submitted_count": len(submitted),
        "missing_count": len(missing),
        "average_score": avg,
        "highest_scorer": {"name": highest['name'], "score": highest['score']},
        "lowest_scorer": {"name": lowest['name'], "score": lowest['score']},
        "domain_wise_average": domain_avg,
        "missing_submissions": missing,
        "students_below_5": below_5
    }

    print(f"Total students: {len(submissions)}")
    print(f"Submitted: {len(submitted)}")
    print(f"Missing: {len(missing)}")
    print(f"Average score: {avg}")
    print(f"Highest scorer: {highest['name']} ({highest['score']})")
    print(f"Missing submissions: {missing}")
    print(f"Summary written to {output_path}")

    write_summary(summary, output_path)

main()