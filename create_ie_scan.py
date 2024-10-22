# create_ie_scan.py
from common import init_session, make_request

def get_policy_details():
    """Prompt the user to enter policy details."""
    policy_name = input("Policy Name (e.g., dot_dat_policy): ")
    directory = input("Directory to scan (e.g., /run): ")

    include_files = input(
        "Enter files or directories to INCLUDE (comma-separated, or press Enter to skip): "
    ).split(',')
    exclude_files = input(
        "Enter files or directories to EXCLUDE (comma-separated, or press Enter to skip): "
    ).split(',')

    backup_type = input(
        "Select Backup Type (options: full, incremental, differential, archive, copy, transfer, daily, level1-level9): "
    )

    return policy_name, directory, include_files, exclude_files, backup_type

def create_policy_execution(session_id, policy_name, directory, include_files, exclude_files, backup_type):
    """Creates a new policy execution."""
    payload = {
        "policy": policy_name,
        "directory": directory,
        "include": [f.strip() for f in include_files if f.strip()],
        "exclude": [f.strip() for f in exclude_files if f.strip()],
        "backup_type": backup_type
    }

    print(f"Creating policy execution with payload: {payload}")
    response = make_request("POST", "cybersense-api/v1/PolicyExecLocal", session_id, data=payload)

    if response.status_code in [200, 202]:
        job_id = response.json().get("job_id")
        print(f"Policy execution created successfully. Job ID: {job_id}")
        return job_id
    else:
        raise Exception(f"Failed to create policy: {response.text}")

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: Get policy details from the user
        policy_name, directory, include_files, exclude_files, backup_type = get_policy_details()

        # Step 3: Create policy execution
        job_id = create_policy_execution(
            session_id, policy_name, directory, include_files, exclude_files, backup_type
        )

        print(f"Policy execution created successfully. Job ID: {job_id}")

    except Exception as e:
        print(f"An error occurred: {e}")
