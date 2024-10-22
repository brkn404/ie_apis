from common import init_session, make_request
import json

def format_cloud_configuration(cloud_data):
    """Formats and prints the cloud configuration in a readable way."""
    print("\n==== Cloud Configuration ====\n")
    print(f"Cloud Config Status : {cloud_data.get('cloud_config_status', 'N/A')}")
    print(f"Persistent Storage Limit : {cloud_data.get('persistent_storage_limit', 'N/A')}")
    print(f"Scratch Storage Limit : {cloud_data.get('scratch_storage_limit', 'N/A')}")
    print(f"Enforce Limits : {cloud_data.get('enforce_limits', 'N/A')}")
    print("====================================\n")

def get_cloud_configuration(session_id):
    """Fetches the cloud configuration."""
    print("Retrieving cloud configuration...")
    response = make_request("GET", "/v1/configurations/cloud", session_id=session_id)

    if response.status_code == 200:
        cloud_data = response.json()
        print("Successfully retrieved cloud configuration.")
        format_cloud_configuration(cloud_data)
    else:
        print(f"Failed to retrieve cloud configuration: {response.status_code} - {response.text}")

def update_cloud_configuration(session_id):
    """Updates the cloud configuration."""
    print("Updating cloud configuration...")
    persistent_storage = input("Enter Persistent Storage Limit (leave blank to skip): ")
    scratch_storage = input("Enter Scratch Storage Limit (leave blank to skip): ")
    enforce_limits = input("Enforce Limits? (true/false): ").lower() == "true"

    # Prepare the update payload
    data = {
        "persistent_storage_limit": int(persistent_storage) if persistent_storage else None,
        "scratch_storage_limit": int(scratch_storage) if scratch_storage else None,
        "enforce_limits": enforce_limits
    }

    # Remove keys with None values
    data = {k: v for k, v in data.items() if v is not None}

    response = make_request("PATCH", "/v1/configurations/cloud", session_id=session_id, data=data)

    if response.status_code == 200:
        print("Successfully updated cloud configuration.")
    else:
        print(f"Failed to update cloud configuration: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Initialize the session
    session_id, _ = init_session()

    # Select an action
    action = input("Select an option:\n1. View cloud configuration\n2. Update cloud configuration\nEnter 1 or 2: ")

    if action == "1":
        get_cloud_configuration(session_id)
    elif action == "2":
        update_cloud_configuration(session_id)
    else:
        print("Invalid option. Exiting.")
