from common import init_session, make_request

def list_scratch_storage_pools():
    """Retrieve information about existing scratch storage pools."""
    try:
        session_id, _ = init_session()
        endpoint = "/v1/scratchstoragepools"

        response = make_request("GET", endpoint, session_id=session_id)

        if response.status_code == 200:
            try:
                pools = response.json()
                print("\n==== Scratch Storage Pools ====")
                if isinstance(pools, list) and pools:
                    for pool in pools:
                        print(f"Path         : {pool.get('path', 'N/A')}")
                        print(f"Maximum Bytes: {pool.get('maximumBytes', 'N/A')}")
                        print(f"Minimum Bytes: {pool.get('minimumBytes', 'N/A')}\n")
                else:
                    print("No scratch storage pools found or unexpected data structure.")
            except ValueError as e:
                print(f"Failed to parse JSON response: {e}")
                print(f"Raw response: {response.text}")
        else:
            print(f"Failed to retrieve storage pools: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Select an option:")
    print("1. View Scratch Storage Pools")
    print("2. Create Scratch Storage Pool")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        list_scratch_storage_pools()
    elif choice == "2":
        print("This option is under development.")
    else:
        print("Invalid choice. Please enter 1 or 2.")
