import requests
from common import init_session

def download_results_file():
    """Downloads a results file from the CyberSense API."""
    try:
        session_id, _ = init_session()
        print("Enter the full path of the file to download (must start with /opt/ie/var/results/):")
        filename = input("> ")

        if not filename.startswith("/opt/ie/var/results/"):
            print("Invalid filename. It must start with /opt/ie/var/results/.")
            return

        print(f"Downloading {filename}...")

        url = f"https://192.168.72.48/ierest/v1/queries/results"
        headers = {"sessionid": session_id}
        params = {"filename": filename}

        # Ignore SSL verification
        response = requests.get(url, headers=headers, params=params, stream=True, verify=False)

        if response.status_code == 200:
            local_filename = filename.split("/")[-1]
            with open(local_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"File downloaded successfully and saved as {local_filename}.")
        elif response.status_code == 400:
            print("Bad request. Please check the filename.")
        elif response.status_code == 401:
            print("Authentication failed. Check session ID.")
        else:
            print(f"Failed to download file: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_results_file()
