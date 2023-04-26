import requests
import sys
# Github actions workflow variables
device_ip = sys.argv[1]
root_username = sys.argv[2]
root_password = sys.argv[3]
user_username = sys.argv[4]
user_password = sys.argv[5]
operator_username = sys.argv[6]
operator_password =sys.argv[7]

# device_ip = '172.25.65.98'  # Replace with the IP address of your device
# username = 'root'  # Replace with your username
# password = 'pass'  # Replace with your password
# user_username = 'user'  # Replace with a non-admin username
# user_password = 'pass'  # Replace with the non-admin password
# operator_username = 'operator'
# operator_password = 'pass'

def verify_only_root_can_update_TLS():
    url = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes'

    # Test request with root credentials
    root_response = requests.get(url, auth=(username, password))

    if root_response.status_code == 200:
        print('Root request succeeded')
    else:
        print(f'Root request failed with status code {root_response.status_code}')

    # Test request with user credentials
    user_response = requests.get(url, auth=(user_username, user_password))

    if user_response.status_code == 401:
        print('User request succeeded with "not allowed" response')
    else:
        print(f'User request failed with status code {user_response.status_code}')

    # Test request with operator credentials
    operator_response = requests.get(url, auth=(operator_username, operator_password))

    if operator_response.status_code == 401:
        print('Operator request succeeded with "not allowed" response')
    else:
        print(f'Operator request failed with status code {operator_response.status_code}')
verify_only_root_can_update_TLS()