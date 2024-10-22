from common import init_session, make_request
from datetime import datetime, timezone

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a readable date format."""
    try:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "Invalid Timestamp"

def list_policy_jobs(policy_name, limit):
    """
    Retrieves the list of jobs for a specific policy in reverse chronological order.
    """
    try:
        # Initialize session and get session_id
        session_id, _ = init_session()

        # Prepare query parameters
        params = {"policy": policy_name, "limit": limit}

        print(f"\nRetrieving jobs for policy '{policy_name}' (limit: {limit})...\n")

        # Make the GET request to retrieve policy jobs
        response = make_request(
            method="GET",
            endpoint="/cybersense-api/v1/PolicyJobs",
            session_id=session_id,
            params=params
        )

        if response.status_code == 200:
            jobs = response.json()
            print(f"Successfully retrieved {len(jobs)} job(s).\n")

            # Loop through jobs and print their details
            for job in jobs:
                print("\n==== Job Details ====")
                print(f"Job ID: {job.get('job_id', 'N/A')}")
                print(f"Job State: {job.get('job_state', 'N/A')}")
                print(f"Policy Name: {job.get('policy', 'N/A')}")
                print(f"Job Type: {job.get('mtype', 'N/A')}")
                print(f"Start Time: {format_unix_timestamp(job.get('start_time_unix'))}")
                print(f"End Time: N/A")  # Assuming no end time field in response
                print(f"Total Bytes Processed: N/A")  # Adjust based on API response

                # Optional: Debugging raw job data
                print(f"\nRaw Job Data: {job}")

        else:
            print(f"Failed to retrieve policy jobs: {response.status_code} - {response.text}")

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    policy_name = input("Enter Policy Name (e.g., 'daily_backup_policy'): ")
    limit_input = input("Enter the number of jobs to retrieve (0 for all, default 10): ") or "10"

    try:
        # Ensure limit is a valid integer
        limit = int(limit_input)
    except ValueError:
        print("Please enter a valid number for the job limit.")
        exit(1)

    list_policy_jobs(policy_name, limit)
