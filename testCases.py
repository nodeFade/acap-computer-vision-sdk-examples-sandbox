
#  Verify that a non-admin user cannot change the settings parameters
#  Add a function test that checks that a non-admin user cannot change the use-TLS parameter
import paramiko
import sys
import requests
password = sys.argv[1]
username = sys.argv[2]
url_base = sys.argv[3]

# Set up the SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the device
ssh_client.connect(hostname=url_base, username=username, password=password)

# Execute a command on the device
stdin, stdout, stderr = ssh_client.exec_command('ls /')

# Print the output of the command
print(stdout.read().decode())

# Close the SSH connection
ssh_client.close()


# print out the output for HTTP request
# curl -s --anyauth -u username:password "http://{url_base}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes"    # < HTTP/1.1 200 OK
# curl -s --anyauth -u username:password "http://{url_base}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes"    # < HTTP/1.1 401 Unauthorized


# from requests.auth import HTTPBasicAuth
# def test_tls_control():
#     # Login as the root user and get an auth token
#     auth_token = login(username, password)

#     # Set the headers with the auth token
#     headers = {"Authorization": f"Bearer {auth_token}"}

#     # Access the TLS settings and make a change
#     tls_config = {"key": "value"}
#     response = requests.post("https://{url_base}/tls/settings", headers=headers, json=tls_config)
#     assert response.status_code == 200

#     # Verify that the change was successful
#     response = requests.get("https://{url_base}/tls/settings", headers=headers)
#     assert response.status_code == 200
#     assert response.json() == tls_config





# Set up the necessary URLs and parameters for the API request
# base_url = url_base
# auth_token = password
# get_users_url = f"{base_url}/camera/index.html#/system/users"
# get_permissions_url = f"{base_url}/permissions"
# headers = {"Authorization": f"Bearer {auth_token}"}

# # Define a function to get the list of users from the API
# def get_users():
#     response = requests.get(get_users_url, headers=headers)
#     return response.json()

# # Define a function to get the list of permissions from the API
# def get_permissions():
#     response = requests.get(get_permissions_url, headers=headers)
#     return response.json()

# # Define a function to check if only the root user has control over the device
# def check_root_control():
#     users = get_users()
#     permissions = get_permissions()
#     root_users = [u for u in users if u["username"] == "root"]
#     if not root_users:
#         return False  # There is no root user
#     root_user_id = root_users[0]["id"]
#     root_user_permissions = [p for p in permissions if p["user_id"] == root_user_id]
#     non_root_permissions = [p for p in permissions if p["user_id"] != root_user_id]
#     if not root_user_permissions:
#         return False  # The root user has no permissions
#     if non_root_permissions:
#         return False  # There are non-root users with permissions
#     return True  # Only the root user has permissions

# Call the check_root_control function and print its return value
# check_root_control()



# def test_device_control():

#     # Set up the authentication token for the root user
#     auth_token = "your_auth_token_here"
#     headers = {"Authorization": f"Bearer {auth_token}"}

#     # Set up the device control endpoint URL
#     url = "https://your_device_control_endpoint_url_here"

#     # Attempt to control the device as the root user (should succeed)
#     response = requests.post(url, headers=headers)
#     assert response.status_code == 200, "Root user unable to control device"

#     # Attempt to control the device as a non-root user (should fail)
#     non_root_token = "your_non_root_auth_token_here"
#     non_root_headers = {"Authorization": f"Bearer {non_root_token}"}
#     non_root_response = requests.post(url, headers=non_root_headers)
#     assert non_root_response.status_code == 401, "Non-root user authorized to control device"

# def test_tls_control():
#     # Login as the root user and get an auth token
#     auth_token = Authentication.login(username, password)

#     # Set the headers with the auth token
#     headers = {"Authorization": f"Bearer {auth_token}"}

#     # Access the TLS settings and make a change
#     tls_config = {"key": "value"}
#     response = requests.post("https://{url_base}/tls/settings", headers=headers, json=tls_config)
#     assert response.status_code == 200

#     # Verify that the change was successful
#     response = requests.get("https://{url_base}/tls/settings", headers=headers)
#     assert response.status_code == 200
#     assert response.json() == tls_config

#     # Logout
#     Authentication.logout()

# # Attempt to access the TLS settings as the user or operator and make a change
# auth_token = Authentication.login("user", password)
# headers = {"Authorization": f"Bearer {auth_token}"}
# tls_config = {"key": "value"}
# response = requests.post("https://{url_base}/tls/settings", headers=headers, json=tls_config)
# assert response.status_code == 403
# assert "Unauthorized" in response.json()["message--not authorized"]