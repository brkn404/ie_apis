from common import init_session, make_request
import json

# Configuration Settings
SEVERITY_TO_FETCH = 5  # Change this value to filter by severity level (1-5)
HIDE_ALERTS = False    # Set to True to hide resolved alerts

def fetch_alerts(session_id, severity, hide):
    """Fetch alerts from CyberSense based on severity and hide settings."""
    endpoint = "v1/alerts"
    params = {'severity': severity, 'hide': hide}
    
    print(f"Fetching alerts with params: {params}")
    response = make_request("GET", endpoint, session_id, params=params)
    
    if response.status_code == 200:
        print("Successfully retrieved alerts.")
        return response.json()
    else:
        raise Exception(f"Failed to fetch alerts: {response.status_code} - {response.text}")

def format_alert(alert):
    """Format the alert data for more readable output."""
    formatted_output = f"""
    ----------------------------------------
    Alert ID: {alert.get('id')}
    Severity: {alert.get('severity')} ({alert.get('severity_number')})
    Service: {alert.get('service')} (Service No: {alert.get('service_number')})
    Start Time: {alert.get('starttime')}
    Status: {alert.get('status')} (Status No: {alert.get('status_number')})
    Type: {alert.get('type')} (Type No: {alert.get('type_number')})
    Message: {alert.get('alert_data', {}).get('message')}
    
    Additional Info: {json.dumps(alert.get('alert_data'), indent=4)}
    ----------------------------------------
    """
    return formatted_output

def main():
    try:
        # Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Fetch alerts with specified severity
        alerts = fetch_alerts(session_id, SEVERITY_TO_FETCH, HIDE_ALERTS)
        
        # Process and print alerts
        for alert in alerts:
            formatted_alert = format_alert(alert)
            print(formatted_alert)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
