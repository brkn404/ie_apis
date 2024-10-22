from common import init_session, make_request

def list_policies():
    """
    Lists all available policies and their current status.
    """
    try:
        # Initialize session and get session_id
        session_id, _ = init_session()

        print("Fetching policies...")
        # Make a GET request to retrieve all policies
        response = make_request(
            method="GET",
            endpoint="/cybersense-api/v1/policies",
            session_id=session_id
        )

        if response.status_code == 200:
            policies = response.json()
            print("Available Policies:\n")
            for i, policy in enumerate(policies):
                print(f"{i + 1}. Policy Name: {policy.get('policy_name_encoded')}")
                print(f"   State: {policy.get('policy_state')}")
                print(f"   Last Job Number: {policy.get('last_job_number')}")
                print(f"   Last Job State: {policy.get('last_job_state')}")
                print(f"   NFS Export: {policy.get('nfs_export')}")
                print(f"   ---")
            return policies
        else:
            print(f"Failed to retrieve policies: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"An error occurred while fetching policies: {e}")
        return []

def clear_infection(policy_name):
    """
    Clears the reported infection status for the specified policy.
    """
    try:
        session_id, _ = init_session()

        print(f"Clearing infection status for policy: '{policy_name}'...")

        response = make_request(
            method="POST",
            endpoint=f"/cybersense-api/v1/PolicyClearInfection?policy={policy_name}",
            session_id=session_id
        )

        if response.status_code == 200:
            print(f"Successfully cleared infection status for policy: '{policy_name}'.")
        else:
            print(f"Failed to clear infection: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # List policies and their statuses
    policies = list_policies()

    if not policies:
        print("No policies available. Exiting...")
        exit(1)

    # Prompt the user to select a policy by number
    try:
        choice = int(input("\nEnter the number of the policy to clear infection: ")) - 1
        if 0 <= choice < len(policies):
            selected_policy = policies[choice].get('policy_name_encoded')
            clear_infection(selected_policy)
        else:
            print("Invalid selection. Exiting...")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
