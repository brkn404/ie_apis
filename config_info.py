from common import init_session, make_request

def format_config_info(config_info):
    """Formats and prints the configuration information."""
    print("\n==== CyberSense Config Info ====\n")
    print(f"Engine ID       : {config_info.get('engineid', 'N/A')}")
    print(f"Federation ID   : {config_info.get('fedid', 'N/A')}")
    print(f"Index ID        : {config_info.get('indexid', 'N/A')}")
    print(f"TDB UUID        : {config_info.get('tdbuuid', 'N/A')}")
    print("\n================================\n")

def get_config_info():
    try:
        # Initialize session and get session ID and federation ID
        session_id, federation_id = init_session()

        print("Retrieving config information...")
        response = make_request(
            "GET", "/v1/configinfo", session_id=session_id
        )

        if response.status_code == 200:
            config_info = response.json()
            print("Successfully retrieved config info.")
            format_config_info(config_info)
        else:
            print(f"Failed to retrieve config info: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_config_info()
