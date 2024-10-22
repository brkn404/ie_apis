# list_ie_jobs.py
from common import init_session, make_request
from datetime import datetime, timezone

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a human-readable date format with UTC timezone."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def list_policies(session_id):
    """List CyberSense policies and print them in a readable format."""
    print("Retrieving CyberSense policies...")
    response = make_request("GET", "cybersense-api/v1/policies", session_id)

    if response.status_code == 200:
        policies = response.json()
        print("Retrieved policies:\n")

        # Loop through policies and print them in a readable format
        for policy in policies:
            print(f"Policy Name: {policy.get('policy_name_encoded')}")
            print(f"Hostname: {policy.get('hostname')}")
            print(f"Last Job Number: {policy.get('last_job_number')}")
            print(f"Last Job State: {policy.get('last_job_state')}")
            print(f"Last Job Start Time: {format_unix_timestamp(policy.get('last_job_start_time'))}")
            print(f"Last Job End Time: {format_unix_timestamp(policy.get('last_job_end_time'))}")
            print(f"NFS Export: {policy.get('nfs_export')}")
            print(f"Policy State: {policy.get('policy_state')}")
            print(f"Queued Job: {policy.get('queued_job')}")
            print(f"Policy URL: {policy.get('policy_url')}")
            print(f"Storage Format: {policy.get('storage_cont_fmt')}\n")

    else:
        raise Exception(f"Failed to retrieve policies: {response.text}")

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: List policies via API
        list_policies(session_id)

    except Exception as e:
        print(f"An error occurred during the process: {e}")
