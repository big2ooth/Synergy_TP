import csv
import json
import os
from typing import List, Dict

def read_submissions(filepath: str) -> List[Dict]:
    if not os.path.exists(filepath): # checking if the input csv file exists
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, newline='') as f: # opening and reading the csv file 
        data = list(csv.DictReader(f))
    
    if not data: # checking if the csv is empty 
        raise ValueError("CSV is empty")
    
    for row in data: # converting string to int
        row['score'] = int(row['score'])
    
    return data

def get_submitted_students(submissions: List[Dict]) -> List[Dict]:
    return [s for s in submissions if s['submitted'] == 'yes'] # returning ONLY the students who submitted 

def calculate_average_score(submissions: List[Dict]) -> float:
    submitted = get_submitted_students(submissions) # assigning ONLY the submitted students
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
    return [s['name'] for s in submissions if s['submitted'] == 'no'] # fetching names of students who did not submit 

def write_summary(summary: Dict, filepath: str) -> None:
    #creates output folder if it doesnt exist (created empty folder locally using bash but git doesnt track empty folder when it clones, so code might crash)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  ##^^
    with open(filepath, 'w') as f: # writing summary in .json file
        json.dump(summary, f, indent=4)