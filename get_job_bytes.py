from common import init_session, make_request
import logging

# Configure logging to display output to the console
logging.basicConfig(level=logging.INFO)

def list_policies(session_id):
    """
    Retrieve and display all policies.
    """
    logging.info("Fetching all policies...")
    response = make_request("GET", "cybersense-api/v1/policies", session_id)

    if response.status_code == 200:
        policies = response.json()
        logging.info("Fetched policies successfully.")

        # Display the list of policies
        for i, policy in enumerate(policies):
            print(f"{i + 1}. {policy.get('policy_name_encoded')}")

        # Return the list of policies
        return policies
    else:
        logging.error(f"Failed to fetch policies: {response.status_code} - {response.text}")
        raise Exception("Policy retrieval failed")

def get_policy_jobs(session_id, policy_name):
    """
    Retrieve all jobs for the specified policy.
    """
    logging.info(f"Fetching jobs for policy: {policy_name}")
    response = make_request("GET", f"cybersense-api/v1/PolicyJobs?policy={policy_name}", session_id)

    if response.status_code == 200:
        jobs = response.json()
        logging.info(f"Fetched {len(jobs)} jobs.")
        return jobs
    else:
        logging.error(f"Failed to fetch jobs: {response.status_code} - {response.text}")
        raise Exception("Job retrieval failed")

def get_job_status(session_id, job_id):
    """
    Retrieve the status for a specific job by ID.
    """
    logging.info(f"Fetching status for job ID: {job_id}")
    response = make_request("GET", f"cybersense-api/v1/JobStatus?job_id={job_id}", session_id)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch job status: {response.status_code} - {response.text}")
        return None

def track_entropy(session_id, jobs):
    """
    Process jobs and log unknown bytes.
    """
    trends = []

    for job in jobs:
        job_id = job.get('job_id')
        if job_id:
            job_details = get_job_status(session_id, job_id)
            if job_details:
                trends.append({
                    'job_id': job_id,
                    'unknown_bytes': job_details['total_unknown_unsupported_bytes'],
                    'start_time': job_details['starttm']
                })
        else:
            logging.warning("Job ID not found in job data")

    # Display trends
    for trend in trends:
        logging.info(f"Job {trend['job_id']} - Unknown Bytes: {trend['unknown_bytes']}")

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: List all policies and allow the user to select one
        policies = list_policies(session_id)
        if not policies:
            print("No policies found.")
            exit(1)

        # User selects a policy from the list
        policy_index = int(input("Enter the number of the policy to select: ")) - 1
        if policy_index < 0 or policy_index >= len(policies):
            raise ValueError("Invalid policy selection")

        selected_policy = policies[policy_index].get('policy_name_encoded')

        # Step 3: Fetch and process jobs for the selected policy
        jobs = get_policy_jobs(session_id, selected_policy)
        if jobs:
            track_entropy(session_id, jobs)
        else:
            print(f"No jobs found for policy '{selected_policy}'.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
