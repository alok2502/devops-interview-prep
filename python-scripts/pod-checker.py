"""
Pod Health Checker
Reads pod data from a JSON file, evaluates each pod against health signals
(status, restarts, CPU), reports problems, and prints a summary.
Practices: file reading, JSON, functions/return, if/elif/else, dict counting.
"""
import json


def check_pod(pod):
    if pod["status"] != "Running":
        return f"PROBLEM: {pod['name']} is {pod['status']}"
    elif pod["restarts"] > 5:
        return f"WARNING: {pod['name']} has high restarts ({pod['restarts']})"
    elif pod["cpu"] > 80:
        return f"WARNING: {pod['name']} has high CPU ({pod['cpu']}%)"
    else:
        return f"OK: {pod['name']} is healthy"


with open("pods.json") as f:
    pods = json.load(f)

healthy = 0
problems = 0
warnings = 0

for pod in pods:
    result = check_pod(pod)
    print(result)
    if result.startswith("OK"):
        healthy += 1
    elif result.startswith("PROBLEM"):
        problems += 1
    else:
        warnings += 1

print(f"\nSummary: {healthy} healthy, {problems} problems, {warnings} warnings")
