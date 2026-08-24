"""
Log Analyzer
Reads a log file line by line, counts log levels, extracts and ranks ERROR
messages by frequency, and auto-identifies the top error.
Practices: line-by-line file reading, .split(), .strip(), slicing + join,
dict counting, max(key=...), empty-dict guard.
"""

counts = {}
error_count = {}

with open("app.log") as f:
    for line in f:
        parts = line.split()
        level = parts[2]

        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1

        if level == "ERROR":
            message = " ".join(parts[3:])
            if message in error_count:
                error_count[message] += 1
            else:
                error_count[message] = 1

# level counts
for level, count in counts.items():
    print(f"{level}: {count}")

# error messages ranked
print("\n--- Errors ---")
for msg, count in error_count.items():
    print(f"{count}x: {msg}")

# top error (guard against empty)
if error_count:
    top_error = max(error_count, key=error_count.get)
    top_count = error_count[top_error]
    print(f"\nTOP ERROR: {top_error} ({top_count} times)")
else:
    print("\nNo errors found!")
