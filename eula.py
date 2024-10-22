from common import init_session, make_request
import json

def view_eula(session_id):
    """Retrieve and display the EULA text and acceptance status."""
    print("Retrieving EULA...")
    response = make_request("GET", "/v1/eula", session_id=session_id)

    if response.status_code == 200:
        eula_data = response.json()
        print("\n==== EULA ====\n")
        print(f"EULA Text: {eula_data.get('eula_text', 'N/A')}\n")
        print(f"Accepted : {eula_data.get('accepted', 'N/A')}")
        print("====================================\n")
    else:
        print(f"Failed to retrieve EULA: {response.status_code} - {response.text}")

def update_eula(session_id):
    """Update the EULA acceptance status."""
    accept = input("Do you accept the EULA? (yes/no): ").lower() == "yes"

    data = {"accepted": accept}
    print("Updating EULA acceptance status...")
    response = make_request("PATCH", "/v1/eula", session_id=session_id, data=data)

    if response.status_code == 200:
        print("Successfully updated EULA acceptance status.")
    else:
        print(f"Failed to update EULA: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Initialize the session
    session_id, _ = init_session()

    # Select action
    action = input("Select an option:\n1. View EULA\n2. Update EULA\nEnter 1 or 2: ")

    if action == "1":
        view_eula(session_id)
    elif action == "2":
        update_eula(session_id)
    else:
        print("Invalid option. Exiting.")
