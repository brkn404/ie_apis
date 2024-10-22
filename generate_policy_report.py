from common import init_session, make_request
import logging
import csv
import io

# Configure logging
logging.basicConfig(level=logging.INFO)

def list_policies(session_id):
    """List all policies and allow the user to select one."""
    logging.info("Fetching all policies...")
    response = make_request("GET", "cybersense-api/v1/policies", session_id)

    if response.status_code == 200:
        policies = response.json()
        logging.info("Fetched policies successfully.")
        for i, policy in enumerate(policies):
            print(f"{i + 1}. {policy.get('policy_name_encoded')}")
        return policies
    else:
        logging.error(f"Failed to fetch policies: {response.text}")
        raise Exception("Failed to retrieve policies")

def get_policy_jobs(session_id, policy_name):
    """Retrieve all jobs for the selected policy."""
    logging.info(f"Fetching jobs for policy: {policy_name}")
    response = make_request("GET", f"cybersense-api/v1/PolicyJobs?policy={policy_name}", session_id)

    if response.status_code == 200:
        jobs = response.json()
        if jobs:
            logging.info(f"Fetched {len(jobs)} jobs.")
        else:
            logging.warning("No jobs found.")
        return jobs
    else:
        logging.error(f"Failed to fetch jobs: {response.text}")
        raise Exception("Job retrieval failed")

def get_job_status(session_id, job_id):
    """Retrieve job status for the selected job."""
    logging.info(f"Fetching status for job ID: {job_id}")
    response = make_request("GET", f"cybersense-api/v1/JobStatus?job_id={job_id}", session_id)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch job status: {response.status_code} - {response.text}")
        raise Exception("Failed to fetch job status")

def get_job_statistics(session_id, job_id):
    """Retrieve job statistics as CSV for the selected job."""
    logging.info(f"Fetching statistics for job ID: {job_id}")
    response = make_request("GET", f"cybersense-api/v1/JobStatistics?job_id={job_id}", session_id)

    if response.status_code == 200:
        return response.text
    else:
        logging.error(f"Failed to fetch job statistics: {response.text}")
        raise Exception(response.text)

def parse_csv(csv_data):
    """Parse the CSV job statistics data."""
    try:
        reader = csv.reader(io.StringIO(csv_data))
        headers = next(reader)
        rows = [row for row in reader]

        logging.info("Job Statistics (CSV):")
        for header, row in zip(headers, rows[0]):
            logging.info(f"{header}: {row}")

        return headers, rows
    except Exception as e:
        logging.error(f"Failed to parse CSV data: {e}")
        return [], []

def generate_report(job_data, csv_headers, csv_rows):
    """Generate a detailed report based on job data and statistics."""
    report = f"""
    CyberSense Job Report
    ---------------------
    Job ID: {job_data.get('job_number', 'N/A')}
    Policy: {job_data.get('policy', 'N/A')}
    State: {job_data.get('state', 'N/A')}
    Start Time: {job_data.get('starttm', 'N/A')}
    End Time: {job_data.get('nowtm', 'N/A')}
    Total Bytes in Backup: {job_data.get('total_bytes_in_backups', 'N/A')}
    Unsupported Bytes: {job_data.get('total_unknown_unsupported_bytes', 'N/A')}
    Unsupported Percentage: {job_data.get('percentage_unknown_unsupported_bytes', 'N/A')}%

    Job Statistics:
    """
    for header, value in zip(csv_headers, csv_rows[0]):
        report += f"    {header}: {value}\n"

    return report

if __name__ == "__main__":
    try:
        # Step 1: Log in to CyberSense and get session ID
        session_id, _ = init_session()

        # Step 2: List policies and allow user selection
        policies = list_policies(session_id)
        if not policies:
            print("No policies found.")
            exit(1)

        policy_index = int(input("Enter the number of the policy to select: ")) - 1
        if policy_index < 0 or policy_index >= len(policies):
            raise ValueError("Invalid policy selection")

        selected_policy = policies[policy_index].get('policy_name_encoded')

        # Step 3: Fetch jobs for the selected policy and list them
        jobs = get_policy_jobs(session_id, selected_policy)
        if not jobs:
            print(f"No jobs found for policy '{selected_policy}'.")
            exit(1)

        print("\nAvailable Jobs:")
        for job in jobs:
            job_id = job.get('job_id')
            unknown_bytes = job.get('total_unknown_unsupported_bytes', 'N/A')
            print(f"Job ID: {job_id} - Unknown Bytes: {unknown_bytes}")

        # Step 4: Allow user to select a job to generate a report
        job_id = int(input("\nEnter the job ID to generate a report: "))

        # Step 5: Fetch job status and statistics
        job_data = get_job_status(session_id, job_id)
        csv_data = get_job_statistics(session_id, job_id)
        csv_headers, csv_rows = parse_csv(csv_data)

        # Step 6: Generate and display the report
        report = generate_report(job_data, csv_headers, csv_rows)
        print(report)

        # Save the report to a file
        with open(f"job_report_{job_id}.txt", "w") as file:
            file.write(report)

        logging.info(f"Report saved to job_report_{job_id}.txt")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
