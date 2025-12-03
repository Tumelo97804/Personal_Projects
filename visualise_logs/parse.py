import csv

LOG_FILE = "error_file.csv"  # your CSV log file

def parse_logs():
    summary = {
        "error_count": 0,
        "warning_count": 0,
        "info_count": 0,
        "recent_errors": [],
        "recent_warnings": [],
        "recent_info": []
    }

    with open(LOG_FILE, newline="", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message = row["Message"]
            log_type = row["LogType"].upper()  # e.g., SYSTEM, APPLICATION

            # Decide type based on log_type or keywords in message
            if "ERROR" in message.upper() or row["EventID"].startswith("2"):  # Example: EventID 20+ = error
                summary["error_count"] += 1
                summary["recent_errors"].append(row)
            elif "WARN" in message.upper() or "WARNING" in message.upper():
                summary["warning_count"] += 1
                summary["recent_warnings"].append(row)
            else:
                summary["info_count"] += 1
                summary["recent_info"].append(row)

    # Keep only last 10 entries
    summary["recent_errors"] = summary["recent_errors"][-10:]
    summary["recent_warnings"] = summary["recent_warnings"][-10:]
    summary["recent_info"] = summary["recent_info"][-10:]

    return summary

# Example usage
if __name__ == "__main__":
    summary = parse_logs()
    print("Error count:", summary["error_count"])
    print("Warning count:", summary["warning_count"])
    print("Info count:", summary["info_count"])
    print("Recent errors:", summary["recent_errors"])
