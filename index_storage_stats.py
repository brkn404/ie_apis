from common import init_session, make_request
from datetime import datetime

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a readable date format."""
    if not timestamp:
        return "N/A"
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_index_storage_stats(session_id, count=None, start_date=None, end_date=None):
    """Retrieve and display index storage statistics."""
    print("Retrieving index storage statistics...")

    # Prepare query parameters
    params = {
        "count": count,
        "start_date": start_date,
        "end_date": end_date,
    }

    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}

    response = make_request("GET", "/v1/indexstoragestats", session_id=session_id, params=params)

    try:
        print(f"Raw Response: {response.text}")

        stats = response.json()

        print("\n==== Index Storage Statistics ====\n")
        print(f"Available Storage (Bytes): {stats.get('available', 'N/A')}")
        print(f"Total Capacity (Bytes)  : {stats.get('capacity', 'N/A')}")
        print(f"Used Storage (Bytes)    : {stats.get('used', 'N/A')}\n")

        history = stats.get("history", [])
        if not history:
            print("No history data found.")
        else:
            print("==== Storage History ====\n")
            for entry in history:
                print(f"Date      : {format_unix_timestamp(entry.get('datetime'))}")
                print(f"Number    : {entry.get('number', 'N/A')} bytes")
                print(f"Used      : {entry.get('used', 'N/A')} bytes")
                print("------------------------------------")

    except ValueError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    session_id, _ = init_session()

    try:
        count = input("Enter the number of records to retrieve (optional): ")
        start_date = input("Enter start date (UNIX timestamp, optional): ")
        end_date = input("Enter end date (UNIX timestamp, optional): ")

        count = int(count) if count.isdigit() else None
        start_date = int(start_date) if start_date.isdigit() else None
        end_date = int(end_date) if end_date.isdigit() else None

        get_index_storage_stats(session_id, count, start_date, end_date)

    except Exception as e:
        print(f"An error occurred: {e}")
