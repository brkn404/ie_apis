from common import init_session, make_request

def list_active_policies():
    """
    List active policies with jobs running or queued.
    """
    try:
        # Initialize session and get session_id and federation_id
        session_id, federation_id = init_session()

        print("Retrieving active policies...")

        # Make GET request to /PolicyJobs to list active policies
        response = make_request(
            method="GET",
            endpoint="/cybersense-api/v1/PolicyJobs",
            session_id=session_id
        )

        if response.status_code == 200:
            policies = response.json()
            if not policies:
                print("No active policies found.")
                return []

            print("\n==== Active Policies ====")
            for policy in policies:
                print(f"Policy Name: {policy.get('policy')}")
                print(f"Job State: {policy.get('state')}")
                print(f"Last Job Number: {policy.get('last_job_number')}\n")

            return [p.get("policy") for p in policies]
        else:
            print(f"Failed to retrieve policies: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"An error occurred while listing policies: {e}")
        return []

def cancel_policy(policy_name):
    """
    Cancels the rerun flag for the specified policy with an active job.
    """
    try:
        # Initialize session and get session_id and federation_id
        session_id, federation_id = init_session()

        # Prepare the request payload
        payload = {"policy": policy_name}

        print(f"Cancelling rerun flag for policy: '{policy_name}'...")

        # Make the POST request to cancel the policy
        response = make_request(
            method="POST",
            endpoint="/cybersense-api/v1/PolicyCancel",
            session_id=session_id,
            data=payload
        )

        if response.status_code == 200:
            print(f"Policy '{policy_name}' rerun flag successfully cancelled.")
        else:
            print(f"Failed to cancel policy: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Step 1: List active policies
    active_policies = list_active_policies()

    if active_policies:
        # Step 2: Prompt the user to enter a policy name to cancel
        policy_name = input("Enter Policy Name to Cancel: ").strip()

        if policy_name in active_policies:
            cancel_policy(policy_name)
        else:
            print(f"Invalid policy name: {policy_name}. Please try again.")
