"""
Failed Jobs Filter
Takes a list of job-log dicts, returns the job IDs where status is FAILED.
Practices: the FILTER PATTERN (loop + condition + collect), functions/return,
list comprehension.
"""

logs = [
    {"job_id": 101, "status": "SUCCESS", "timestamp": "2025-06-10T10:00:00"},
    {"job_id": 102, "status": "FAILED",  "timestamp": "2025-06-10T10:05:00"},
    {"job_id": 103, "status": "FAILED",  "timestamp": "2025-06-10T10:10:00"},
    {"job_id": 104, "status": "SUCCESS", "timestamp": "2025-06-10T10:15:00"},
]


# loop version
def get_failed_jobs(logs):
    failed_jobs = []
    for log in logs:
        if log["status"] == "FAILED":
            failed_jobs.append(log["job_id"])
    return failed_jobs


print(get_failed_jobs(logs))   # [102, 103]

# one-liner (list comprehension) — [COLLECT for ITEM in LIST if CONDITION]
failed = [log["job_id"] for log in logs if log["status"] == "FAILED"]
print(failed)                  # [102, 103]
