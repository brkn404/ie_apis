import requests
import logging
import time
from common import init_session, make_request

# Enable logging
logging.basicConfig(level=logging.INFO)

poll_interval = 10  # Polling interval in seconds

def list_jobs(session_id):
    """Fetch and list all available jobs from policies."""
    logging.info("Fetching all policies to retrieve jobs...")
    response = make_request("GET", "cybersense-api/v1/policies", session_id)

    if response.status_code == 200:
        policies = response.json()
        logging.info("Fetched policies successfully.")

        jobs = []
        for policy in policies:
            policy_name = policy.get("policy_name_encoded")
            job_number = policy.get("last_job_number")
            if job_number:
                logging.info(f"Policy: {policy_name} - Last Job ID: {job_number}")
                jobs.append({"policy": policy_name, "job_id": job_number})

        return jobs
    else:
        logging.error(f"Failed to fetch policies: {response.status_code} - {response.text}")
        raise Exception("Job retrieval failed")

def get_job_status(session_id, job_id):
    """Fetch the status of a specific job."""
    logging.info(f"Fetching status for job ID: {job_id}")
    response = make_request("GET", f"cybersense-api/v1/JobStatus?job_id={job_id}", session_id)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch job status: {response.status_code} - {response.text}")
        return None

def print_job_summary(job_details):
    """Print a detailed summary of the job."""
    summary = f"""
    Job ID: {job_details.get('job_number')}
    Policy: {job_details.get('policy')}
    State: {job_details.get('state')}
    Message: {job_details.get('statemsg', 'N/A')}
    Start Time: {job_details.get('starttm')}
    End Time: {job_details.get('nowtm')}
    Total Bytes in Backup: {job_details.get('total_bytes_in_backups', 'N/A')} bytes
    Unsupported Bytes: {job_details.get('total_unknown_unsupported_bytes', 'N/A')} bytes
    Unsupported Percentage: {job_details.get('percentage_unknown_unsupported_bytes', 'N/A')}%
    New Files Indexed: {job_details.get('nnew', 'N/A')}
    New Groups: {job_details.get('nnew_groups', 'N/A')}
    Infected Files: {job_details.get('nnew_infected', 'N/A')}
    Indexing Mode: {job_details.get('indexing_mode', 'N/A')}
    Warnings: {job_details.get('lan_backupset_counters', {}).get('nwarning', 'N/A')}
    Errors: {job_details.get('job_exception_counters', {}).get('ninternalerr', 'N/A')}
    """
    logging.info(summary)

def monitor_job(session_id, job_id):
    """Monitor the status of a selected job in real-time."""
    while True:
        job_status = get_job_status(session_id, job_id)
        if job_status and job_status.get('ie_idx_job_state') == 'Done':
            logging.info(f"Job {job_id} completed.")
            print_job_summary(job_status)
            break
        elif job_status:
            state = job_status.get('ie_idx_job_state', 'Unknown')
            message = job_status.get('statemsg', 'No message')
            logging.info(f"Current State: {state} - {message}")
        time.sleep(poll_interval)

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: List jobs and allow the user to select one
        jobs = list_jobs(session_id)
        if not jobs:
            print("No jobs found.")
            exit(1)

        print("\nAvailable Jobs:")
        for idx, job in enumerate(jobs, 1):
            print(f"{idx}. Policy: {job['policy']} - Job ID: {job['job_id']}")

        selected = int(input("\nSelect a job by number: ")) - 1
        selected_job = jobs[selected]['job_id']

        # Step 3: Monitor the selected job in real-time
        monitor_job(session_id, selected_job)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
