from common import init_session, make_request

# Example Federation ID (replace as needed)
FED_ID = "3533654b-e66b-40f3-8b96-14e617e6940a"

def get_index_details(session_id, fed_id, index_id):
    """Fetch details of a specific index from CyberSense."""
    endpoint = f"v1/federations/{fed_id}/indexes/{index_id}"
    
    print(f"Fetching details for index ID: {index_id}")
    response = make_request("GET", endpoint, session_id)

    if response.status_code == 200:
        index_details = response.json()
        print(f"Index Details: {index_details}")
    else:
        print(f"Failed to fetch index details: {response.status_code} - {response.text}")

def main():
    try:
        # Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Get the index ID from user input
        index_id = input("Enter the index ID to retrieve: ")

        # Fetch and print index details
        get_index_details(session_id, FED_ID, index_id)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
