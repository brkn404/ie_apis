import json
from common import init_session, make_request

def format_configurations(config_data):
    """Formats and prints the configurations in a readable way."""
    print("\n==== General Configurations ====\n")

    cloud_status = config_data.get('cloud', {}).get('cloud_config_status', 'N/A')
    print(f"Cloud Config Status   : {cloud_status}")

    vendor = config_data.get('customization', {}).get('vendor', 'N/A')
    print(f"Vendor                : {vendor}")

    index_maintenance = config_data.get('index_maintenance', {})
    print("\nIndex Maintenance:")
    print(f"  Reclaimation Day    : {index_maintenance.get('reclaimation_day', 'N/A')}")
    print(f"  Reclaimation Hour   : {index_maintenance.get('reclaimation_hour', 'N/A')}")
    print(f"  Schedule ID         : {index_maintenance.get('schedid', 'N/A')}")

    mfa = config_data.get('mfa', {})
    print("\nMFA Configuration:")
    print(f"  Federation ID       : {mfa.get('fedid', 'N/A')}")
    print(f"  OTP Setting         : {mfa.get('otp_setting', 'N/A')}")

    packages = config_data.get('packages', [])
    print("\nInstalled Packages:")
    for package_group in packages:
        if package_group:
            for package in package_group:
                print(f"  Name: {package['name']}")
                for version in package.get('versions', []):
                    print(f"    Version: {version['version']} (Release: {version['release']})")
                    print(f"    Installed by: {version['packager']}")
                    print(f"    Vendor: {version.get('vendor', 'N/A')}")
                    print(f"    Install Time: {version['install_time']}")
                    print()

    session = config_data.get('session', {})
    print("\nSession Configuration:")
    print(f"  Max Idle Minutes    : {session.get('max_idle_minutes', 'N/A')}")
    print(f"  Same Index Access   : {session.get('same_index_access', 'N/A')}")
    print(f"  Same IP Access      : {session.get('same_ip_access', 'N/A')}")

    stalehosts = config_data.get('stalehosts', {})
    print(f"\nStale Hosts Interval : {stalehosts.get('interval_seconds', 'N/A')} seconds")

def get_configurations():
    """Fetches general configurations."""
    try:
        session_id, _ = init_session()
        print("Retrieving general configurations...")
        response = make_request("GET", "/v1/configurations", session_id=session_id)

        if response.status_code == 200:
            config_data = response.json()
            print("Successfully retrieved configurations.")
            format_configurations(config_data)
        else:
            print(f"Failed to retrieve configurations: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_configurations()
