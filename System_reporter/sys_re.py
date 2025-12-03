import psutil
import csv
from datetime import datetime
import os

# -----------------------
# CONFIG
# -----------------------
# Name of the CSV file where system data will be stored.
html_FILE = "daily_system_report.html"

# -----------------------
# FUNCTION: Collect Data
# -----------------------
def collect_system_data():
    # Get current date and time as a string.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get CPU usage percentage (waits 1 second to measure accurately).
    cpu_percent = psutil.cpu_percent(interval=1)

    # Get RAM (memory) usage info.
    ram = psutil.virtual_memory()
    ram_percent = ram.percent  # Extract % of RAM used.

    # Get disk usage for the main directory '/'.
    disk = psutil.disk_usage("/")
    disk_percent = disk.percent  # Extract % of disk used.

    # Get network upload/download bytes since boot.
    net = psutil.net_io_counters()
    upload = net.bytes_sent        # Total bytes uploaded.
    download = net.bytes_recv      # Total bytes downloaded.

    # Get battery percentage (if device has a battery).
    battery_info = psutil.sensors_battery()
    battery_percent = battery_info.percent if battery_info else "N/A"

    # Return all collected values as a list (one row of data).
    return [
        now,
        cpu_percent,
        ram_percent,
        disk_percent,
        upload,
        download,
        battery_percent,
    ]

# -----------------------
# FUNCTION: Create File Header
# -----------------------
def create_csv_if_missing():
    # If the CSV file does not exist, create it and add column headers.
    if not os.path.exists(html_FILE):
        with open(html_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write the header row (column names).
            writer.writerow([
                "timestamp",
                "cpu_percent",
                "ram_percent",
                "disk_percent",
                "network_upload_bytes",
                "network_download_bytes",
                "battery_percent",
            ])

# -----------------------
# MAIN
# -----------------------
def main():
    # Create CSV file with header if it doesn't exist.
    create_csv_if_missing()

    # Collect current system data.
    data = collect_system_data()

    # Append the collected data as a new row to the CSV file.
    with open(html_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

    # Print confirmation message.
    print("Daily system report saved to", html_FILE)


# Run the main function only if the script is executed directly.
if __name__ == "__main__":
    main()
