# cancel_policy.py

from common import init_session, make_request

def cancel_policy(session_id, policy_name):
    """
    Attempts to cancel the specified policy execution in CyberSense.
    """
    print(f"Attempting to cancel policy: {policy_name}")

    # Prepare the request payload and headers
    cancel_payload = {"policy": policy_name}

    # Make the request to cancel the policy
    response = make_request(
        method="POST",
        endpoint="cybersense-api/v1/PolicyCancel",
        session_id=session_id,
        data=cancel_payload
    )

    # Handle the response and output messages
    if response.status_code == 200:
        print(f"Policy '{policy_name}' canceled successfully.")
    elif response.status_code == 405:
        print(f"Method not allowed: {response.text}")
    elif response.status_code == 404:
        print(f"Policy not found: {response.text}")
    else:
        print(f"Error: Failed to cancel policy: {response.text}")
        raise Exception("Policy cancellation failed")

if __name__ == "__main__":
    try:
        # Step 1: Initialize session and retrieve session ID
        session_id, _ = init_session()

        # Step 2: Cancel the specified policy
        policy_name = input("Enter the name of the policy to cancel: ")
        cancel_policy(session_id, policy_name)

    except Exception as e:
        print(f"An error occurred: {e}")
