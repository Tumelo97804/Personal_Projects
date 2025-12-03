import re
import csv
from pathlib import Path
from datetime import datetime

# Optional Windows imports
try:
    import win32evtlog  # Windows Event Log API
    import win32con     # Windows constants
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

def get_Error_Logs(server="localhost", log_types=None, test_mode=False):
    """
    Reads Windows Event Logs (if available) or simulated logs in test_mode.
    Returns a list of error events as dictionaries.
    """
    error_logs = []

    if log_types is None:
        log_types = ['System', 'Application', 'Security', 'Setup', 'Forwarded Events']

    if test_mode or not WINDOWS_AVAILABLE:
        # --- Test mode / Linux-friendly version ---
        import glob
        print("--- Running in test mode: reading simulated logs ---")
        for log_file in glob.glob("sample_logs/*.log"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if "ERROR" in line.upper():
                        error_logs.append({
                            "LogType": "TestLog",
                            "EventID": 0,
                            "Source": "TestScript",
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Message": line.strip()
                        })
        return error_logs

    # --- Original Windows Event Log functionality ---
    for log_type in log_types:
        print(f"--- Searching for errors in '{log_type}' log ---")
        try:
            hand = win32evtlog.OpenEventLog(Application, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

            events_read = 1
            while events_read > 0:
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                if not events:
                    break
                events_read = len(events)
                for event in events:
                    if event.EventType == win32con.EVENTLOG_ERROR_TYPE:
                        error_logs.append({
                            "LogType": log_type,
                            "EventID": event.EventID,
                            "Source": event.SourceName,
                            "Time": event.TimeGenerated.Format(),
                            "Message": " ".join(event.StringInserts) if event.StringInserts else ""
                        })

        except Exception as e:
            print(f"Could not read '{log_type}' log. Error: {e}")
        finally:
            if 'hand' in locals():
                win32evtlog.CloseEventLog(hand)

    return error_logs


def generate_report(error_logs, report_file="output/error_file.csv"):
    """
    Writes the error logs into a CSV report.
    """
    Path("output").mkdir(parents=True, exist_ok=True)  # Ensure output folder exists

    if not error_logs:
        print("No errors found in the Event Logs.")
        return

    try:
        with open(report_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["LogType", "EventID", "Source", "Time", "Message"])
            writer.writeheader()
            writer.writerows(error_logs)

        print(f"CSV report generated: {Path(report_file).resolve()}")

    except Exception as e:
        print(f"Failed to generate report: {e}")


if __name__ == "__main__":
    # --- Change test_mode=True to run on GitHub Actions / Linux ---
    logs = get_Error_Logs(test_mode=True)
    generate_report(logs, report_file="output/error_file.csv")
