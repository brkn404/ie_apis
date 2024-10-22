from common import init_session, make_request
from datetime import datetime, timezone
import json

def format_timestamp(timestamp):
    """Convert Unix timestamp to human-readable UTC format."""
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def get_job_summary(job_id):
    """
    Retrieves the summary of a job using the job ID.
    """
    try:
        # Initialize session and get session_id and federation_id
        session_id, federation_id = init_session()

        print(f"\nRetrieving summary for Job ID: {job_id}...\n")

        # Build the endpoint with query parameters
        endpoint = f"/cybersense-api/v1/JobSummary?job_id={job_id}"
        response = make_request("GET", endpoint, session_id=session_id)

        if response.status_code == 200:
            job_summary = response.json()

            # Display Job Summary with correctly matched fields
            print(f"==== Job Summary for Job ID: {job_id} ====")
            print(f"Job Status: {job_summary.get('state')}")
            print(f"State Message: {job_summary.get('statemsg')}")
            print(f"Policy: {job_summary.get('policy')}")
            print(f"Total Bytes Indexed: {job_summary.get('total_bytes_indexed')}")
            print(f"Unsupported Bytes: {job_summary.get('unsupported_bytes')}")
            print(f"Missing Bytes: {job_summary.get('missing_bytes')}")
            print(f"Backup Sets: {job_summary.get('number_of_backup_sets')}")
            print(f"Backupset Groups: {job_summary.get('number_of_backupset_groups')}")
            print(f"Infections Found: {job_summary.get('number_of_infections_found')}")
            print(f"Unique Clients: {job_summary.get('number_of_unique_clients')}")
            print(f"Elapsed Time (seconds): {job_summary.get('elapsed_time')}")

            # Backup Time Window
            backup_window = job_summary.get('backup_time_window', {})
            print(f"Backup Start Time: {format_timestamp(backup_window.get('start'))}")
            print(f"Backup End Time: {format_timestamp(backup_window.get('end'))}\n")

            # Optional: Display full JSON response for reference
            print("Parsed JSON Response:\n", json.dumps(job_summary, indent=4))

        else:
            print(f"Failed to retrieve job summary: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        job_id = int(input("Enter Job ID (e.g., '127'): "))
        get_job_summary(job_id)
    except ValueError:
        print("Invalid Job ID. Please enter a valid integer.")
