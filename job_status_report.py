# job_status.py
from common import init_session, make_request

def get_job_status(session_id, job_id):
    """Retrieves the status of a job."""
    endpoint = f"/cybersense-api/v1/JobStatus"
    params = {"job_id": job_id}
    return make_request("GET", endpoint, session_id, params=params)

def format_job_status(status):
    """Formats job status for clean output."""
    print("\nJob Status Details")
    print("-" * 40)
    print(f"Job ID: {status.get('job_number')}")
    print(f"State: {status.get('state')}")
    print(f"Message: {status.get('statemsg')}")
    print(f"Start Time: {status.get('starttm')}")
    print(f"End Time: {status.get('endtm')}")
    print(f"Bytes Indexed: {status.get('total_bytes_indexed')}")
    print(f"Infections Found: {status.get('number_of_infections_found')}")
    print("-" * 40)

if __name__ == "__main__":
    session_id, _ = init_session()
    job_id = input("Enter Job ID: ")

    try:
        status = get_job_status(session_id, job_id)
        format_job_status(status)
    except Exception as e:
        print(f"Error: {e}")
