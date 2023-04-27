import requests
import paramiko
import sys
# Github actions workflow variables
device_ip = sys.argv[1]
root_username = sys.argv[2]
root_password = sys.argv[3]
user_username = sys.argv[4]
user_password = sys.argv[5]
operator_username = sys.argv[6]
operator_password =sys.argv[7]



# The Root should get inside the camera and change the TLS setup.
# The User should get inside the camera but not allowed to reach the TLS and the operator as well. 
def verify_only_root_can_update_TLS():
    url = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes'

    # Test request with root credentials
    root_response = requests.get(url, auth=(root_username, root_password))

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


import subprocess
import paramiko
# The daemon running on prot 2375 while not using the TLS else it's running on port 2376.
def acap_without_tls_running_on_port_2375():
    url_stop_daemon = f'http://{device_ip}/axis-cgi/applications/control.cgi?action=stop&package=dockerdwrapper'
    root_response = requests.get(url_stop_daemon, auth=(root_username, root_password))

    if root_response.status_code == 200:
        print('Daemon is stopped')
        url_turn_tls_off = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=no'
        root_response = requests.get(url_turn_tls_off, auth=(root_username, root_password))
        if root_response.status_code == 200:
            print('TLS is off')
            url_stop_daemon = f'http://{device_ip}/axis-cgi/applications/control.cgi?action=start&package=dockerdwrapper'
            root_response = requests.get(url_stop_daemon, auth=(root_username, root_password))
            if root_response.status_code == 200:
                print('The daemon started even if the TLS is disabled and port changed to 2375')
                command = ['curl', '-s', '--anyauth', '-u', f'{root_username}:{root_password}', '-k', '--header', 'Content-Type:application/json', f'http://{device_ip}/axis-cgi/admin/systemlog.cgi?']
                process = subprocess.run(command, capture_output=True)
                logs = process.stdout.decode('utf-8')
                print(logs)
    else:
        print('The daemon started on port changed to 2376')
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the device
    ssh_client.connect(hostname=device_ip, username=root_username, password=root_password)

    # Execute a command on the device
    stdin, stdout, stderr = ssh_client.exec_command('cat /usr/local/packages/dockerdwrapper/conf/dockerdwrapper.conf')

    # Print the output of the command
    print(stdout.read().decode())

    # Close the SSH connection
    ssh_client.close()
acap_without_tls_running_on_port_2375()

