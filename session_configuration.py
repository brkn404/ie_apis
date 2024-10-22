from common import init_session, make_request
import json

def format_session_config(config):
    """Formats and prints session configuration information."""
    print("\n==== Session Configuration ====\n")
    print(f"IP Restricted Access   : {config.get('ip_restricted', 'N/A')}")
    print(f"Index ID Restricted    : {config.get('indexid_restricted', 'N/A')}")
    print(f"Max Idle Time (minutes): {config.get('max_idle_time', 'N/A')}")
    print("====================================\n")

def get_session_configuration():
    """Fetches the current session's configuration properties."""
    try:
        session_id, _ = init_session()
        print("Retrieving session configuration...")

        response = make_request("GET", "/v1/configuration/session", session_id=session_id)

        if response.status_code == 200:
            config = response.json()
            format_session_config(config)
        else:
            print(f"Failed to retrieve session configuration: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

def update_session_configuration(ip_restricted=None, indexid_restricted=None, max_idle_time=None):
    """Updates the session configuration properties."""
    try:
        session_id, _ = init_session()
        print("Updating session configuration...")

        payload = {
            "ip_restricted": ip_restricted,
            "indexid_restricted": indexid_restricted,
            "max_idle_time": max_idle_time,
        }

        # Remove None values to avoid sending unnecessary data
        payload = {k: v for k, v in payload.items() if v is not None}

        response = make_request("PATCH", "/v1/configuration/session", session_id=session_id, data=payload)

        if response.status_code == 200:
            print("Session configuration successfully updated.")
        else:
            print(f"Failed to update session configuration: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Select an option:")
    print("1. View current session configuration")
    print("2. Update session configuration")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        get_session_configuration()
    elif choice == "2":
        ip_restricted = input("Restrict to the same client IP? (true/false, default: None): ").lower()
        ip_restricted = ip_restricted == "true" if ip_restricted in ["true", "false"] else None

        indexid_restricted = input("Restrict access to the same index ID? (true/false, default: None): ").lower()
        indexid_restricted = indexid_restricted == "true" if indexid_restricted in ["true", "false"] else None

        max_idle_time = input("Enter max idle time in minutes (default: None): ")
        max_idle_time = int(max_idle_time) if max_idle_time.isdigit() else None

        update_session_configuration(ip_restricted, indexid_restricted, max_idle_time)
    else:
        print("Invalid option. Exiting...")
