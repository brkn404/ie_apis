from common import init_session, make_request

def get_policy_status_local(policy_name):
    """
    Retrieves the status of a specified policy using the /PolicyStatusLocal endpoint.
    """
    try:
        # Initialize session and retrieve session ID
        session_id, federation_id = init_session()

        print(f"Retrieving status for policy '{policy_name}'...")

        # Make the GET request to retrieve the policy status
        endpoint = f"/cybersense-api/v1/PolicyStatusLocal?policy={policy_name}"
        response = make_request("GET", endpoint, session_id=session_id)

        if response.status_code == 200:
            policy_status = response.json()
            print("\n==== Policy Status ====")
            print(f"Policy Name: {policy_name}")
            print(f"Policy State: {policy_status.get('policy_state', 'N/A')}")
            print(f"Last Job Number: {policy_status.get('last_job_number', 'N/A')}")
            print(f"Last Job State: {policy_status.get('last_job_state', 'N/A')}")
            print(f"Queued Job: {policy_status.get('queued_job', 'N/A')}")
            print(f"NFS Export: {policy_status.get('nfs_export', 'N/A')}")
            print(f"Storage Format: {policy_status.get('storage_cont_fmt', 'N/A')}")
        else:
            print(f"Failed to retrieve policy status: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    policy_name = input("Enter Policy Name (e.g., 'daily_backup_policy'): ")
    get_policy_status_local(policy_name)
