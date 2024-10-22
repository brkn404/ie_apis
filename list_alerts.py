from common_save import init_session, make_request

def list_alerts(session_id):
    """Lists all alerts."""
    endpoint = "/v1/alerts"
    response = make_request("GET", endpoint, session_id)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            return response.json()  # Parse the JSON data
        except ValueError:
            print("Failed to parse JSON response.")
            return []
    else:
        print(f"Request failed: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    session_id, _ = init_session()

    try:
        alerts = list_alerts(session_id)

        if alerts:
            print(f"Retrieved {len(alerts)} alert(s):")
            for alert in alerts:
                print(f"- ID: {alert.get('id')}, Severity: {alert.get('severity')}, Status: {alert.get('status')}, Type: {alert.get('type')}")
        else:
            print("No alerts found.")
    except Exception as e:
        print(f"Failed to retrieve alerts: {e}")
