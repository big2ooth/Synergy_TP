import csv
import json
import os
from typing import List, Dict

def read_submissions(filepath: str) -> List[Dict]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, newline='') as f:
        data = list(csv.DictReader(f))
    
    if not data:
        raise ValueError("CSV is empty")
    
    for row in data:
        row['score'] = int(row['score'])
    
    return data

def get_submitted_students(submissions: List[Dict]) -> List[Dict]:
    return [s for s in submissions if s['submitted'] == 'yes']

def calculate_average_score(submissions: List[Dict]) -> float:
    submitted = get_submitted_students(submissions)
    total = sum(s['score'] for s in submitted)
    return round(total / len(submitted), 2)

def get_domain_wise_average(submissions: List[Dict]) -> Dict[str, float]:
    domains = {}
    for s in submissions:
        d = s['domain']
        if d not in domains:
            domains[d] = []
        domains[d].append(s['score'])
    return {d: round(sum(v)/len(v), 2) for d, v in domains.items()}

def get_missing_submissions(submissions: List[Dict]) -> List[str]:
    return [s['name'] for s in submissions if s['submitted'] == 'no']

def write_summary(summary: Dict, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(summary, f, indent=4)