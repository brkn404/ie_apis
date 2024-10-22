from common import init_session, make_request
import json

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a readable date format."""
    from datetime import datetime, timezone
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def format_license_info(license_info):
    """Formats detailed license information."""
    return json.dumps(license_info, indent=2)

def format_licenses(licenses_data):
    """Formats and prints license information."""
    print("\n==== System License Information ====\n")
    if "license_system" in licenses_data:
        print(format_license_info(licenses_data["license_system"]))
    print("====================================\n")

    print("\n==== Individual Licenses ====\n")
    for license_entry in licenses_data.get("license_list", []):
        print(f"License ID     : {license_entry.get('license_id')}")
        print(f"Components     : {', '.join(license_entry.get('license_components', []))}")
        print(f"Inherited      : {license_entry.get('inherited', False)}")
        print(f"Install Time   : {format_unix_timestamp(license_entry.get('license_install_time'))}")
        print(f"Expiry Time    : {format_unix_timestamp(license_entry.get('license_expire_time'))}")
        print(f"Serial         : {license_entry.get('license_serial')}")
        print(f"Software Ver   : {license_entry.get('license_sversion', 'N/A')}")
        print(f"Details:\n{format_license_info(license_entry.get('license_info', {}))}")
        print("====================================\n")

def get_licenses():
    """Retrieves and displays license information."""
    try:
        session_id, _ = init_session()
        print("Retrieving license information...")

        response = make_request("GET", "/v1/licenses", session_id=session_id)

        if response.status_code == 200:
            licenses_data = response.json()
            print("Successfully retrieved licenses.")
            format_licenses(licenses_data)
        else:
            print(f"Failed to retrieve licenses: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_licenses()
