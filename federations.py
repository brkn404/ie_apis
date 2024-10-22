from common import init_session, make_request
import json

def get_federations(session_id):
    """Retrieve and display federation information."""
    print("Retrieving federation information...")
    response = make_request("GET", "/v1/federations", session_id=session_id)

    if response.status_code == 200:
        federations = response.json()
        print("\n==== Federations ====\n")
        for federation in federations:
            print(f"Federation ID       : {federation.get('fed_id', 'N/A')}")
            print(f"Active Federation ID: {federation.get('active_fed_id', 'N/A')}")
            print(f"Local Federation ID : {federation.get('local_fed_id', 'N/A')}")
            print(f"Manager Hostname    : {federation.get('manager_engine_hostname', 'N/A')}")
            print("====================================\n")
    else:
        print(f"Failed to retrieve federations: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Initialize the session
    session_id, _ = init_session()

    try:
        get_federations(session_id)
    except Exception as e:
        print(f"An error occurred: {e}")
