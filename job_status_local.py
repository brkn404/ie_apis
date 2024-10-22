from common import init_session, make_request
from datetime import datetime, timezone
import json

def format_timestamp(timestamp):
    """Convert Unix timestamp to human-readable UTC format."""
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def get_local_job_status(job_id):
    """
    Retrieves the status of a local job using the job ID.
    """
    try:
        session_id, federation_id = init_session()

        print(f"\nRetrieving status for Job ID: {job_id}...\n")

        endpoint = f"/cybersense-api/v1/JobStatusLocal?job_id={job_id}"
        response = make_request("GET", endpoint, session_id=session_id)

        if response.status_code == 200:
            job_status = response.json()

            # Print Job ID as Header
            print(f"==== Job ID: {job_id} ====")
            
            # Print the parsed response details
            print(f"Job State: {job_status.get('state')}")
            print(f"Associated Policy: {job_status.get('policy')}")
            print(f"Job Start Time: {format_timestamp(job_status.get('starttm'))}")
            print(f"Job End Time: {format_timestamp(job_status.get('nowtm'))}")
            print(f"Message: {job_status.get('statemsg')}")
            print(f"Hostname: {job_status.get('hostname')}")
            print(f"Storage Format: {job_status.get('storage_cont_fmt')}\n")

            # Optional: Show entire JSON for debugging
            print("Parsed JSON Response:\n", json.dumps(job_status, indent=4))

        else:
            print(f"Failed to retrieve job status: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        job_id = int(input("Enter Job ID (e.g., '127'): "))
        get_local_job_status(job_id)
    except ValueError:
        print("Invalid Job ID. Please enter a valid integer.")
