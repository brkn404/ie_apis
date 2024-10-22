from common import init_session, make_request
import json

def format_unix_timestamp(timestamp):
    """Converts a Unix timestamp to a readable date format."""
    from datetime import datetime, timezone
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def format_migration_jobs(jobs):
    """Formats and prints migration jobs information."""
    if not jobs:
        print("No migration jobs found.")
        return

    print("\n==== Migration Jobs ====\n")
    for job in jobs:
        print(f"Job ID        : {job.get('job_id', 'N/A')}")
        print(f"Status        : {job.get('status', 'N/A')}")
        print(f"Start Time    : {format_unix_timestamp(job.get('start_time'))}")
        print(f"End Time      : {format_unix_timestamp(job.get('end_time'))}")
        print(f"Segments      : {job.get('segments', [])}")
        print(f"Engine Target : {job.get('engine_target', 'N/A')}")
        print(f"Error Message : {job.get('error_message', 'N/A')}")
        print("====================================\n")

def get_migration_jobs():
    """Retrieves and displays migration jobs."""
    try:
        session_id, _ = init_session()
        print("Retrieving migration jobs...")

        response = make_request("GET", "/v1/migrationjobs", session_id=session_id)

        if response.status_code == 200:
            data = response.json()

            # Check if 'migration_jobs_status' exists and is a list
            jobs = data.get('migration_jobs_status', None)
            if jobs is not None:
                if isinstance(jobs, list) and jobs:
                    print("Successfully retrieved migration jobs.")
                    format_migration_jobs(jobs)
                else:
                    print("No migration jobs found.")
            else:
                print(f"Unexpected response format: {data}")
        else:
            print(f"Failed to retrieve migration jobs: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

def initiate_migration_job(data):
    """Initiates a new migration job."""
    try:
        session_id, _ = init_session()
        print("Initiating migration job...")

        response = make_request("POST", "/v1/migrationjobs", session_id=session_id, data=data)

        if response.status_code == 202:
            print("Migration job initiated successfully.")
        else:
            print(f"Failed to initiate migration job: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    option = input("Select an option:\n1. View Migration Jobs\n2. Initiate Migration Job\nEnter 1 or 2: ")

    if option == "1":
        get_migration_jobs()
    elif option == "2":
        engine_target = input("Enter target engine: ")
        segments = input("Enter segments to migrate (comma-separated): ").split(",")
        migration_data = {
            "engine_target": engine_target,
            "segments": segments
        }
        initiate_migration_job(data=migration_data)
    else:
        print("Invalid option selected.")
