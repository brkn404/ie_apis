from common import init_session, make_request

def regenerate_job_statistics(job_id, email_send=True, email_list=None):
    """
    Requests the regeneration of statistics for the specified job ID.
    """
    try:
        # Initialize session and get session_id and federation_id
        session_id, federation_id = init_session()

        # Prepare the request payload
        payload = {
            "job_id": job_id,
            "email_send": email_send,
        }

        if email_list:
            payload["List_of_email_addresses"] = email_list

        print(f"Requesting statistics regeneration for Job ID: {job_id}...")

        # Make the POST request to initiate statistics regeneration
        response = make_request(
            "POST", "/cybersense-api/v1/JobStatisticsRegen", session_id=session_id, data=payload
        )

        if response.status_code == 200:
            print(f"Successfully started regeneration for Job ID: {job_id}.")
        else:
            print(f"Failed to start regeneration: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        job_id = int(input("Enter Job ID (e.g., '127'): "))
        email_send = input("Send email? (true/false): ").lower() == 'true'
        email_list = input(
            "Enter additional email addresses (comma-separated, optional): "
        ).split(",") if email_send else None

        # Call the function to regenerate job statistics
        regenerate_job_statistics(job_id, email_send, email_list)

    except ValueError:
        print("Invalid Job ID. Please enter a valid integer.")
