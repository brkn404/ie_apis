from common import init_session, make_request
from datetime import datetime

def list_scratch_storage_stats():
    """Retrieve scratch storage statistics."""
    try:
        session_id, _ = init_session()
        endpoint = "/v1/scratchstoragestats"

        # Get optional parameters for query
        count = input("Enter the number of results to retrieve (leave blank for all): ").strip() or None
        start_date = input("Enter the start date (YYYY-MM-DD, leave blank for none): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD, leave blank for none): ").strip()

        # Convert dates to Unix timestamp if provided
        params = {}
        if count:
            params['count'] = int(count)
        if start_date:
            params['start_date'] = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        if end_date:
            params['end_date'] = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

        response = make_request("GET", endpoint, session_id=session_id, params=params)

        if response.status_code == 200:
            try:
                stats = response.json()
                print("\n==== Scratch Storage Statistics ====")
                if isinstance(stats, list) and stats:
                    for stat in stats:
                        print(f"Timestamp: {datetime.fromtimestamp(stat.get('timestamp', 0))}")
                        print(f"Used Bytes: {stat.get('usedBytes', 'N/A')}")
                        print(f"Total Bytes: {stat.get('totalBytes', 'N/A')}\n")
                else:
                    print("No storage statistics found or unexpected data structure.")
            except ValueError as e:
                print(f"Failed to parse JSON response: {e}")
                print(f"Raw response: {response.text}")
        else:
            print(f"Failed to retrieve storage stats: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Fetching Scratch Storage Statistics...")
    list_scratch_storage_stats()
