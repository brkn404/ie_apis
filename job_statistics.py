from common import init_session, make_request

def get_job_statistics(session_id, job_id):
    """
    Retrieve job statistics from the CyberSense API.
    """
    endpoint = "cybersense-api/v1/JobStatistics"
    params = {"job_id": job_id}

    print(f"Retrieving statistics for Job ID: {job_id}...")
    response = make_request("GET", endpoint, session_id=session_id, params=params)

    if response.status_code == 200 and response.text.strip():
        try:
            data = response.json()
            print("Successfully retrieved job statistics:")
            print(data)
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response content: {response.text}")
    else:
        print(f"Failed to retrieve job statistics: {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        session_id, federation_id = init_session()
        job_id = input("Enter Job ID: ").strip()
        get_job_statistics(session_id, job_id)

    except Exception as e:
        print(f"An error occurred: {e}")
