from common import init_session, make_request
import json
from datetime import datetime, timezone

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a readable date format."""
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def format_alert(alert):
    """Formats and prints a single alert's details."""
    print("\n==== Alert Details ====\n")
    print(f"ID            : {alert.get('id', 'N/A')}")
    print(f"Service       : {alert.get('service', 'N/A')}")
    print(f"Severity      : {alert.get('severity', 'N/A')}")
    print(f"Status        : {alert.get('status', 'N/A')}")
    print(f"Type          : {alert.get('type', 'N/A')}")
    print(f"Start Time    : {format_unix_timestamp(alert.get('starttime'))}")
    print(f"End Time      : {format_unix_timestamp(alert.get('endtime'))}")
    print(f"MAC Address   : {alert.get('engine', 'N/A')}")
    print(f"Hidden        : {alert.get('hide', 'N/A')}")
    print(f"Alert Data    : {json.dumps(alert.get('alert_data', {}), indent=2)}")
    print(f"Update Seq.   : {alert.get('update_sequence', 'N/A')}\n")
    print("====================================\n")

def list_alert_ids():
    """Fetches and lists all available alert IDs."""
    session_id, _ = init_session()

    print("Retrieving available alerts...")
    response = make_request("GET", "/v1/alerts", session_id=session_id)

    if response.status_code == 200:
        alerts = response.json()
        if not alerts:
            print("No alerts found.")
            return None

        print("\n==== Available Alerts ====\n")
        for alert in alerts:
            print(f"ID: {alert.get('id', 'N/A')} | Service: {alert.get('service', 'N/A')} | Severity: {alert.get('severity', 'N/A')}")
        print("====================================\n")
        return alerts
    else:
        print(f"Failed to retrieve alerts: {response.status_code} - {response.text}")
        return None

def get_alert(alert_id):
    """Retrieves the details of a specific alert."""
    session_id, _ = init_session()

    print(f"Retrieving details for alert ID: {alert_id}...")
    endpoint = f"/v1/alerts/{alert_id}"
    response = make_request("GET", endpoint, session_id=session_id)

    if response.status_code == 200:
        alert = response.json()
        print("Successfully retrieved alert details.")
        format_alert(alert)
    else:
        print(f"Failed to retrieve alert: {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        alerts = list_alert_ids()
        if alerts:
            alert_id = input("Enter the Alert ID to view or update: ").strip()

            if alert_id.isdigit():
                get_alert(int(alert_id))
            else:
                print("Invalid Alert ID. Please enter a valid integer.")
        else:
            print("No alerts available. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")
