from common import init_session, make_request

def send_job_statistics_email(job_id, email_addresses):
    """
    Sends an email about a job to the specified list of email addresses.
    """
    try:
        # Initialize session and get session ID and federation ID
        session_id, federation_id = init_session()

        # Prepare the request payload
        payload = {
            "job_id": job_id,
            "List_of_email_addresses": email_addresses
        }

        print(f"Sending email about Job ID '{job_id}' to {email_addresses}...")

        # Make the POST request to the JobStatisticsEmail endpoint
        response = make_request(
            "POST", "/cybersense-api/v1/JobStatisticsEmail", session_id=session_id, data=payload
        )

        if response.status_code == 200:
            print("Email sent successfully.")
        else:
            print(f"Failed to send email: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Collect inputs from the user
    try:
        job_id = int(input("Enter Job ID (e.g., '127'): "))
        email_list = input(
            "Enter Email Addresses (comma-separated, e.g., 'user1@example.com,user2@example.com'): "
        ).split(",")

        # Execute the function to send the job statistics email
        send_job_statistics_email(job_id, email_list)

    except ValueError:
        print("Invalid Job ID. Please enter a valid integer.")
