# job_status.py
from common import init_session, make_request

def get_job_status(session_id, job_id):
    """Retrieves the status of a job."""
    endpoint = f"/cybersense-api/v1/JobStatus"
    params = {"job_id": job_id}
    return make_request("GET", endpoint, session_id, params=params)

if __name__ == "__main__":
    session_id, _ = init_session()
    job_id = input("Enter Job ID: ")

    try:
        status = get_job_status(session_id, job_id)
        print(f"Job Status: {status}")
    except Exception as e:
        print(f"Failed to retrieve job status: {e}")
