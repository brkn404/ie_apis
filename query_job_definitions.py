import json
from common import init_session, make_request

def format_json_field(field):
    """Formats JSON fields for better readability."""
    if isinstance(field, str):
        try:
            # Attempt to parse and pretty print JSON strings
            parsed = json.loads(field)
            return json.dumps(parsed, indent=2)
        except (ValueError, TypeError):
            return field  # Return as-is if parsing fails
    elif isinstance(field, (dict, list)):
        return json.dumps(field, indent=2)  # Format if it's already a dict/list
    return str(field)

def view_query_job_definitions():
    """Retrieves and displays query job definitions with better formatting."""
    try:
        session_id, _ = init_session()
        print("Retrieving query job definitions...")
        response = make_request("GET", "/v1/queries/jobdefinitions", session_id=session_id)

        if response.status_code == 200:
            job_definitions = response.json()
            if job_definitions:
                print("\n==== Query Job Definitions ====\n")
                for job in job_definitions:
                    print(f"Job ID      : {job.get('qjobdefid')}")
                    print(f"Job Name    : {job['qjob'].get('qname', 'None')}")
                    print(f"Description : {job['qjob'].get('descript', 'None')}")
                    print(f"Email       : {job['qjob'].get('email', 'None')}")
                    print(f"Format      : {job['qjob'].get('format', 'None')}")
                    print(f"Format Str  :\n{format_json_field(job['qjob'].get('formatstr', 'None'))}")
                    print("====================================\n")
            else:
                print("No query job definitions found.")
        else:
            print(f"Failed to retrieve query job definitions: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """Main function to handle user input."""
    print("Select an option:")
    print("1. View Query Job Definitions")
    print("2. Create Query Job Definition")
    print("3. Update Query Job Definition")
    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        view_query_job_definitions()
    else:
        print("Other options not implemented.")

if __name__ == "__main__":
    main()
