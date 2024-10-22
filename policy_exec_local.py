from common import init_session, make_request

def execute_policy_local(policy_name, directory, storage_format):
    """
    Executes a local policy indexing job.
    """
    try:
        # Initialize session and get session_id and federation_id
        session_id, _ = init_session()

        # Prepare the request payload
        payload = {
            "policy": policy_name,
            "directory": directory,
            "storage_cont_fmt": storage_format
        }

        print(f"Executing local policy '{policy_name}' on directory '{directory}'...")

        # Make the POST request to execute the local policy
        response = make_request(
            method="POST",
            endpoint="/cybersense-api/v1/PolicyExecLocal",
            session_id=session_id,
            data=payload
        )

        if response.status_code == 200:
            job_id = response.json().get("jobid")
            print(f"Policy executed successfully. Job ID: {job_id}")
        else:
            print(f"Failed to execute local policy: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    policy_name = input("Enter Policy Name (e.g., 'local_policy'): ")
    directory = input("Enter Directory to Analyze (e.g., '/mnt/local'): ")
    storage_format = input("Enter Storage Format (e.g., 'FileSystem'): ")

    execute_policy_local(policy_name, directory, storage_format)
