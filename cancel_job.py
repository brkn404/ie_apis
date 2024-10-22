# cancel_job.py
from common import init_session, make_request

def cancel_job(session_id, job_id):
    """Cancels a job."""
    endpoint = f"/cybersense-api/v1/JobCancel"
    data = {"job_id": job_id}
    return make_request("POST", endpoint, session_id, data=data)

if __name__ == "__main__":
    session_id, _ = init_session()
    job_id = input("Enter Job ID to cancel: ")

    try:
        response = cancel_job(session_id, job_id)
        print(f"Job cancelled: {response}")
    except Exception as e:
        print(f"Failed to cancel job: {e}")
