from common import init_session, make_request
import json

def format_alerts(alerts):
    """Formats and prints alerts in a readable way."""
    if not alerts:
        print("No alerts found.")
        return

    print("\n==== Alerts ====\n")
    for alert in alerts:
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

def get_alerts(service=None, severity=None, status=None, hide=False):
    """Fetches alerts based on optional filters."""
    try:
        # Initialize session and get session ID and federation ID
        session_id, federation_id = init_session()

        print("Retrieving alerts...")
        params = {
            "service": service,
            "severity": severity,
            "status": status,
            "hide": hide,
        }

        # Filter out None values from params
        params = {k: v for k, v in params.items() if v is not None}

        response = make_request(
            "GET", "/v1/alerts", session_id=session_id, params=params
        )

        if response.status_code == 200:
            alerts = response.json()
            print("Successfully retrieved alerts.")
            format_alerts(alerts)
        else:
            print(f"Failed to retrieve alerts: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example inputs added to prompt the user
    service = input("Enter Service Code (optional, e.g., '18'): ")
    severity = input("Enter Severity Code (optional, e.g., '5'): ")
    status = input("Enter Status Code (optional, e.g., '2'): ")
    hide = input("Include Hidden Alerts? (true/false, default false): ").lower() == "true"

    # Handle optional integer inputs safely
    service = int(service) if service.isdigit() else None
    severity = int(severity) if severity.isdigit() else None
    status = int(status) if status.isdigit() else None

    get_alerts(service=service, severity=severity, status=status, hide=hide)
