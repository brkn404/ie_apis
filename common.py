import requests
import urllib3
from datetime import datetime, timezone

# Suppress InsecureRequestWarnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Environment-specific variables
API_URL = "https://192.168.72.48/ierest"
USERNAME = "admin"
PASSWORD = "IE!ATSP@ssw0rd?"

def init_session():
    """
    Logs into the CyberSense API and retrieves the session ID and Federation ID.
    """
    print("Logging into CyberSense API...")
    login_payload = {"user_name": USERNAME, "password": PASSWORD}

    response = requests.post(f"{API_URL}/v1/sessions", json=login_payload, verify=False)

    if response.status_code == 200:
        session_id = response.json().get("sessionid")
        print(f"Logged in successfully. Session ID: {session_id}")

        federation_id = get_federation_id(session_id)
        return session_id, federation_id
    else:
        print(f"Failed to log in: {response.text}")
        raise Exception("Login failed")

def get_federation_id(session_id):
    """
    Retrieves the Federation ID using the session ID.
    """
    headers = {"sessionid": session_id}
    response = requests.get(f"{API_URL}/v1/federations", headers=headers, verify=False)

    if response.status_code == 200:
        federation_id = response.json()[0].get("fed_id")
        print(f"Federation ID: {federation_id}")
        return federation_id
    else:
        print(f"Failed to retrieve federation ID: {response.text}")
        raise Exception("Federation retrieval failed")

def make_request(method, endpoint, session_id=None, data=None, params=None):
    """
    Makes a request to the specified API endpoint using the session ID.
    Supports JSON body and query parameters.
    """
    url = f"{API_URL}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}

    if session_id:
        headers["sessionid"] = session_id

    response = requests.request(
        method, url, headers=headers, json=data, params=params, verify=False
    )

    if response.status_code >= 400:
        print(f"Request failed: {response.status_code} - {response.text}")
    return response

def format_unix_timestamp(timestamp):
    """
    Converts a Unix timestamp to a readable date format.
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
