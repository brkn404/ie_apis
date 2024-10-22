from common import init_session, make_request

def get_indexes(session_id, fed_id):
    """
    Fetch indexes for a given federation ID and print their details.
    """
    endpoint = f"v1/federations/{fed_id}/indexes"
    response = make_request("GET", endpoint, session_id)

    if response.status_code == 200:
        indexes = response.json()
        print(f"Indexes found: {len(indexes)}")

        for index in indexes:
            print(f"Index ID: {index['indexid']}, Name: {index['name']}, "
                  f"State: {index['istate']}, Capacity: {index['capacity']}")

        return indexes
    else:
        print(f"Failed to fetch indexes: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, federation_id = init_session()

        # Step 2: Retrieve and print indexes for the federation
        indexes = get_indexes(session_id, federation_id)

        if not indexes:
            print("No indexes found or failed to retrieve.")
    except Exception as e:
        print(f"An error occurred: {e}")
