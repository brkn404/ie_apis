import logging
from datetime import datetime, timezone
from common import init_session, make_request

# Set up logging to print info and errors directly to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_unix_timestamp(timestamp):
    """
    Converts a Unix timestamp to a human-readable date format with UTC timezone.
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def list_policies(session_id):
    """
    Retrieves and lists all policies from the CyberSense API.
    """
    logging.info("Fetching all policies...")
    response = make_request("GET", "cybersense-api/v1/policies", session_id)

    if response.status_code == 200:
        policies = response.json()
        logging.info("Fetched policies successfully.")

        for idx, policy in enumerate(policies, 1):
            print(f"{idx}. {policy.get('policy_name_encoded')}")
        return policies
    else:
        logging.error(f"Failed to retrieve policies: {response.status_code} - {response.text}")
        raise Exception("Failed to fetch policies")

def get_policy_details(session_id, policy):
    """
    Retrieves and returns detailed information for the selected policy.
    """
    logging.info(f"Retrieving details for policy: {policy.get('policy_name_encoded')}")
    
    formatted_details = f"""
    Policy Name: {policy.get('policy_name_encoded')}
    Hostname: {policy.get('hostname')}
    Policy State: {policy.get('policy_state')}
    Last Job Number: {policy.get('last_job_number')}
    Last Job State: {policy.get('last_job_state')}
    Last Job Start Time: {format_unix_timestamp(policy.get('last_job_start_time'))}
    Last Job End Time: {format_unix_timestamp(policy.get('last_job_end_time'))}
    NFS Export: {policy.get('nfs_export')}
    Storage Format: {policy.get('storage_cont_fmt')}
    Policy URL: {policy.get('policy_url')}
    """
    return formatted_details

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: List policies and allow the user to select one
        policies = list_policies(session_id)
        if not policies:
            print("No policies found.")
            exit(1)

        selected = int(input("Select a policy by number: ")) - 1
        if selected < 0 or selected >= len(policies):
            raise ValueError("Invalid selection.")

        # Step 3: Get and display details of the selected policy
        policy = policies[selected]
        details = get_policy_details(session_id, policy)

        # Step 4: Print the formatted policy details
        print(details)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
