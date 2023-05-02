import requests
import sys
import subprocess
import paramiko
import time
# Github actions workflow variables
# device_ip = sys.argv[1]
# root_username = sys.argv[2]
# root_password = sys.argv[3]
# user_username = sys.argv[4]
# user_password = sys.argv[5]
# operator_username = sys.argv[6]
# operator_password =sys.argv[7]

device_ip = '172.25.65.98'  # Replace with the IP address of your device
root_username = 'root'  # Replace with your username
root_password = 'pass'  # Replace with your password
user_username = 'user'  # Replace with a non-admin username
user_password = 'pass'  # Replace with the non-admin password
operator_username = 'operator'
operator_password = 'pass'

# print("####################### Case 1 ######################")
# def verify_only_root_can_update_TLS():
#     # The Root should get inside the camera and change the TLS setup.
#     # The User should get inside the camera but not allowed to reach the TLS and the operator as well. 

#     url = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes'

#     # Test request with root credentials
#     root_response = requests.get(url, auth=(root_username, root_password))

#     if root_response.status_code == 200:
#         print('Root request succeeded')
#     else:
#         print(f'Root request failed with status code {root_response.status_code}')

#     # Test request with user credentials
#     user_response = requests.get(url, auth=(user_username, user_password))

#     if user_response.status_code == 401:
#         print('User request succeeded with "not allowed" response')
#     else:
#         print(f'User request failed with status code {user_response.status_code}')

#     # Test request with operator credentials
#     operator_response = requests.get(url, auth=(operator_username, operator_password))

#     if operator_response.status_code == 401:
#         print('Operator request succeeded with "not allowed" response')
#     else:
#         print(f'Operator request failed with status code {operator_response.status_code}')
# verify_only_root_can_update_TLS()

# print("####################### Case 2 ######################")
# # The daemon running on prot 2375 while not using the TLS else it's running on port 2376.
# def acap_without_tls_running_on_port_2375():
#     url_stop_daemon = f'http://{device_ip}/axis-cgi/applications/control.cgi?action=stop&package=dockerdwrapper'
#     root_response = requests.get(url_stop_daemon, auth=(root_username, root_password))
#     time.sleep(10)
#     if root_response.status_code == 200:
#         print('Daemon stopped')
#         url_turn_tls_off = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=no'
#         root_response = requests.get(url_turn_tls_off, auth=(root_username, root_password))
#         if root_response.status_code == 200:
#             print('TLS is off')
#             url_stop_daemon = f'http://{device_ip}/axis-cgi/applications/control.cgi?action=start&package=dockerdwrapper'
#             time.sleep(10)
#             root_response = requests.get(url_stop_daemon, auth=(root_username, root_password))
#             if root_response.status_code == 200:
#                 print('The daemon started even if the TLS is disabled and port changed to 2375')
#                 command = ['curl', '-s', '--anyauth', '-u', f'{root_username}:{root_password}', '-k', '--header', 'Content-Type:application/json', f'http://{device_ip}/axis-cgi/admin/systemlog.cgi?']
#                 process = subprocess.run(command, capture_output=True)
#                 logs = process.stdout.decode('utf-8')
#                 print(logs)
#     else:
#         print('The daemon started on port changed to 2376')
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Connect to the device
#     ssh_client.connect(hostname=device_ip, username=root_username, password=root_password)

#     # Execute a command on the device
#     stdin, stdout, stderr = ssh_client.exec_command('cat /usr/local/packages/dockerdwrapper/conf/dockerdwrapper.conf')

#     # Print the output of the command
#     print(stdout.read().decode())

#     # Close the SSH connection
#     ssh_client.close()
# acap_without_tls_running_on_port_2375()

# print("####################### Case 3 ######################")
# def try_to_enject_invalid_value_to_run_dockerd():
#     # When attacker get inside the camera, granted root credentials
#     # thus the root credentials used in this case.

#     url = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes'
#     root_response = requests.get(url , auth=(root_username, root_password))
#     if root_response.status_code == 200:
#         print("If the attacker change the value to no it will change as root permissions.")
#     else:
#         print("The attacker ned root permissions.")

#     url_change = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=delete'
#     root_response = requests.get(url_change , auth=(root_username, root_password))
#     if root_response.status_code == 200:
#         print("If the attacker change the value to 'delete/remove or inject a script' nothing will change and it will remain yes or no.")
#     else:
#         print("The attacker can update the command as wanted.")
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Connect to the device
#     ssh_client.connect(hostname=device_ip, username=root_username, password=root_password)

#     # Execute a command on the device
#     stdin, stdout, stderr = ssh_client.exec_command('cat /usr/local/packages/dockerdwrapper/conf/dockerdwrapper.conf')

#     # Print the output of the command
#     print(stdout.read().decode())

#     # Close the SSH connection
#     ssh_client.close()
# try_to_enject_invalid_value_to_run_dockerd()


# # Verify that the ACAP will not start if the parameter is deleted (or missing).
# # This case is not pretty clear and it needs some explanation.
# # Madelen mentioned the following:
# #################################
# # the way it should work is that before Docker ACAP is started the user will set the parameters.
# # Once the ACAP is started it should not care if the parameters are changed. 
# # But from an attacker point of view:
# # If  the attacker have internal access to the device you could stop the application,
# # change the parameter and then restart the application. 
# # Possibly it would work to just restart dockerd without the application noticing it.
# # So from outside - if TLS is disabled port 2376 will stop working but an attacker would be able to access on port 2375.
# # The certificates can remain on the camera - they will not be used if TLS is off.

# print("####################### Case 4 ######################")
# def attacker_have_internal_access_cannt_inject_parameters_or_update_paramfile():
#     # If you remove the value "no|No" from the (/usr/local/packages/dockerdwrapper/param.conf) file and add remove or delete
#     # that will no affect the docker-acap and it will continue as last value tested (UseTLS=yes|no).
#     # So, the file can edited but not executed 
#     url = f'http://{device_ip}/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=remove'
#     root_response = requests.get(url , auth=(root_username, root_password))
#     if root_response.status_code == 200:
#         print("TLS changed.")

#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Connect to the device
#     ssh_client.connect(hostname=device_ip, username=root_username, password=root_password)

#     # Execute a command on the device
#     stdin, stdout, stderr = ssh_client.exec_command('cat /usr/local/packages/dockerdwrapper/conf/dockerdwrapper.conf')

#     # Print the output of the command
#     print(stdout.read().decode())

#     # Close the SSH connection
#     ssh_client.close()
# attcker_have_internal_access_cannt_inject_parameters_or_update_paramfile()

# print("####################### Case 5 ######################")
# def daemonfile_edited_only_by_root():
#     # The daemon.json should have permission read and write while the other groups and users can only read the file.
#     # thus in the output (-rw-r--r--) is displayed and that mean the file can only readable and writable from the root.
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Connect to the device
#     ssh_client.connect(hostname=device_ip, username=root_username, password=root_password)

#     # Execute a command on the device
#     stdin, stdout, stderr = ssh_client.exec_command('ls -la /usr/local/packages/dockerdwrapper/localdata')
#     output = stdout.read().decode()
#     print(output)
#     lines = output.split('\n')
#     for line in lines:
#         if 'daemon.json' in line and '-rw-r--r--' not in line:
#             print("Daemon.json file not secure. Please fix the configuration.")
#             print(line)
#             return
       
#     print("Daemon have only root permissions.")
#     # Close the SSH connection
#     ssh_client.close()
# daemonfile_edited_only_by_root()


# print("####################### Case 6 ######################")
# def only_root_can_run_container(device_ip, username, password):
#      # SSH into the device
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         ssh.connect(device_ip, username=username, password=password)
#         print(f"Connected to {device_ip} via SSH")
#     except paramiko.AuthenticationException:
#         print("Authentication failed, please verify your credentials.")
#         return
#     except Exception as e:
#         print(f"Error: {e}")
#         return
#     stdin, stdout, stderr = ssh.exec_command('cat /etc/shadow')
#     stdin.write(password + '\n')
#     stdin.flush()
#     output = stdout.read().decode()
#     users = output.split('\n')
#     print("The users available now on the camera are: ")
#     for user in users:
#         if user.startswith('root:') or user.startswith('daemon:') or user.startswith('user') or user.startswith('operator'):
#             # print(user)
#             usersSplited = user.split(':')[0]
#             print(usersSplited)
#         # usernaming = user.split(':')[0]
#         # print(usernaming)

#     # Check if only root can run containers on the daemon
#     stdin, stdout, stderr = ssh.exec_command('ls -l /usr/local/packages/dockerdwrapper')
#     output = stdout.read().decode()
#     lines = output.split('\n')
#     print("Grab the line which contains dockerd and assert to have root permissions.")
#     for l in lines:
#         li=l.split(',')
#         print(li)
#     for line in lines:
#         if 'dockerd' in line and 'root' not in line: # if the root is removed then the case will be vise-versal which non-user can run docker daemon.
#             print("Containers can be run by non-root users. Please fix the configuration.")
#             return
    
#     print("Only root can run containers on the daemon.")
# only_root_can_run_container(device_ip, root_username, root_password)

# import docker
# print("################ Case 7 ###################")
# def test_local_user_access_to_dockerd():
#      # SSH into the device
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         ssh.connect(device_ip, username=root_username, password=root_password)
#         print(f"Connected to {device_ip} via SSH")
#     except paramiko.AuthenticationException:
#         print("Authentication failed, please verify your credentials.")
#         return
#     except Exception as e:
#         print(f"Error: {e}")
#         return
#     client = docker.from_env()

#     try:
#         # Try to run an arbitrary container with the current user
#         client.containers.run('alpine', 'echo hello world', remove=True)
#         # If the container runs successfully, the user has access to dockerd
#         print('Local user can run arbitrary containers via dockerd')
#     except docker.errors.APIError as e:
#         # If the container fails to run with an API error, the user does not have access to dockerd
#         if 'permission denied' in str(e).lower():
#             print('Local user does not have access to dockerd')
#         else:
#             print('Error:', str(e))
# test_local_user_access_to_dockerd()
