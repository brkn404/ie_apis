from common import init_session, make_request
from datetime import datetime, timezone, timedelta

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a human-readable date format with UTC timezone."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def list_job_ids_from_policies(session_id):
    """Retrieve all job IDs from CyberSense policies."""
    print("Retrieving CyberSense policies to extract job IDs...")
    response = make_request("GET", "cybersense-api/v1/policies", session_id)

    if response.status_code == 200:
        policies = response.json()
        job_ids = []

        print("Retrieved policies and their job numbers:\n")
        for policy in policies:
            last_job_number = policy.get("last_job_number")
            if last_job_number:
                job_ids.append(last_job_number)
                print(f"Policy: {policy.get('policy_name_encoded')}, Job ID: {last_job_number}")

        print(f"\nTotal Jobs Found: {len(job_ids)}")
        return job_ids
    else:
        raise Exception(f"Failed to retrieve policies: {response.text}")

def fetch_job_details(session_id, job_id):
    """Fetch job details from the CyberSense API for a given job ID."""
    endpoint = f"cybersense-api/v1/JobStatus?job_id={job_id}"
    response = make_request(method="GET", endpoint=endpoint, session_id=session_id)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch job {job_id}: {response.status_code} - {response.text}")
        return None

def calculate_duration(start_unix, end_unix):
    """Calculate the duration between two Unix timestamps."""
    duration = end_unix - start_unix
    return str(timedelta(seconds=duration))

def analyze_jobs(session_id, job_ids):
    """Analyze the provided jobs and print a summary."""
    print(f"\n{'Job ID':<8} {'Total Bytes':<15} {'Duration':<15} {'Warnings'}")
    print("-" * 50)

    for job_id in job_ids:
        job_data = fetch_job_details(session_id, job_id)
        if job_data:
            total_bytes = job_data.get("total_bytes_in_backups", 0)
            start_time = job_data.get("starttm", 0)
            end_time = job_data.get("nowtm", 0)
            duration = calculate_duration(start_time, end_time)
            warnings_count = job_data.get("lan_backupset_counters", {}).get("nwarning", 0)

            print(f"{job_id:<8} {total_bytes:<15} {duration:<15} {warnings_count}")

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: List policies and extract job IDs
        job_ids = list_job_ids_from_policies(session_id)

        # Step 3: Analyze the extracted job IDs
        analyze_jobs(session_id, job_ids)

    except Exception as e:
        print(f"An error occurred during the process: {e}")
