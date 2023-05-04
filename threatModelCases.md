An ACAP that runs the Docker Daemon, which is needed in order to run containers on a device. [https://github.com/AxisCommunications/docker-acap]
In the bellow picture you can see where the params get the config parameters from param.cgi (which is the api from VAPIX commands). The ACAP starts the docker-daemon after reading the config file. 
            --> Picture to be uploaded while moving this file to confluence.

Our mission to make the DockerACAP more secure and make use cases that run as potential loopholes for attacker to expose the application.

ACAP installation can be done by using pre-built docker-hub[https://hub.docker.com/r/axisecp/docker-acap] image or running axisecp/docker-acap image as mentioned in ReadMe file[https://github.com/AxisCommunications/docker-acap]. 

As a point of attacker view: Pulling an image from docker hub to build the Docker ACAP could contain potential threat, attacker can manipulate the docker run command with another image to be build. Thus, that would affect the installation with potential updated image.
            UC:1.0 Testing the image pulled from docker hub by assertion of the 
            image pulled or the real repository for the real image is secure, if that True, then the real image is pulled successfully.

The ACAP has been installed, and the DockerDaemon is starting with the corresponding parameters and variables.
Docker Daemon started with functions to retrieve parameter names and confirm that the SD card has been set up, TLS keys are available, and the IPC socket has been configured successfully.
To ensure the security of our Daemon, it is necessary to assume an attacker role, assert the functions used to run the Daemon, and inspect the variables that could be changed.

### In this part of the App code where parameter changes..
Any changes made to the SDCard parameter in the daemon require the Docker Daemon to be restarted, and this should be noted in the sys_logs of the application.
From an attacker's point of view, it is possible to send unknown parameters or injections that could affect the application by accessing or reading data that is not allowed.
Explanation as a code, can be found in the blocks bellow:

-There are 2 constant variables the (value and name) in the constructor.
-The code start iterates through an array of parameter names (ax_parameters) to check if a given parameter name (parname) matches any of the names in the array. 
-If a match is found, the value of that parameter is changed to a new value (value), and the flag restart_dockerd is set to true.

                            const gchar *parname = name += strlen("root.dockerdwrapper.");
                              bool unknown_parameter = true;
                              for (size_t i = 0; i < sizeof(ax_parameters) / sizeof(ax_parameters[0]);++i){
                                if (strcmp(parname, ax_parameters[i]) == 0) {
                                  syslog(LOG_INFO, "%s changed to: %s", ax_parameters[i], value);
                                  restart_dockerd = true;
                                  unknown_parameter = false;
                                }
                              }

-Where, at the top level, the (sizeof ax_parameters) get the number of elements and devided by the number of bytes in this case 
the elements are 3 (static const char* ax_parameters[]= {"IPCSocket", "SDCardSupport", "UseTLS"};Line 52), and the 
number of bytes is 8 for every element,
number of bytes overall array: (8 * 4 = 24) 
devide them to verify 3 elements are in the array 
-The characters are constant that connot the attacker change them to manipulate the elements in the array.


-The next step if the parameter is unknown parameter, then:
                            if (unknown_parameter) {
                                syslog(LOG_WARNING, "Parameter %s is not recognized", name);
                                restart_dockerd = false;

                                // No known parameter was changed, do not restart.
                                return;
                              }
-If the unknown_parameter flag is still true after the for loop completes, it means that the parameter name passed as an argument does not match any of the parameter names in the ax_parameters array. In this case, the function logs a warning message using the syslog function, indicating that the parameter is not recognized. The restart_dockerd flag is set to false, indicating that dockerd should not be restarted. Finally, the function returns, indicating that no known parameter was changed and dockerd does not need to be restarted.

          U:2.0 The name is already done and CANNOT be change, because the Loop iteration calculating the parameter depending on the name that provided in(ax_parameters array), So, to focus on the next parameter which is the Value:
                              Can the attacker change the value before it could be send to the call function and inject something other than the expected values?

          U:2.1 Test if the unkown parameter through the VAPIX command 
          ---------curl -s --anyauth -u username:password "http://device-IP/axis-cgi/param.cgi?action=stop&root.dockerdwrapper.UseTLS=yes"------
          if the attacker change the parameters, what will happen? regarding (restart and log message Warning, ) 

-Finally, if unknown_parameter is still true, the function stops the currently running dockerd process using the stop_dockerd function. 
If this fails, the function logs an error and sets exit_code to -1.
                          if (!stop_dockerd()) {
                              syslog(LOG_ERR,
                                    "Failed to stop dockerd process. Please restart the acap "
                                    "manually.");
                              exit_code = -1;
                            }

          U:1.2 If the Logs after the manual restart respond as "dockerd shutdown successfully" is True. 
                Get the output with VAPIX command:
                -----curl -s --anyauth -u username:"password" -k --header "Content-Type:application/json" http://device-IP/axis-cgi/admin/systemlog.cgi?------



### This code is for retrieving the value of an AXParameter struct based on a given parameter name. If an error occurs during initialization or parameter retrieval, the function logs an error message and returns NULL. If the parameter retrieval is successful, the function returns the retrieved parameter value.
Scenario: The attacker try to manupulate the Application that the (Attacker file contains the TLS files) rather than the dockerdwrapper

-This code take the name as parameter.
-The function creates a new AXParameter struct using the ax_parameter_new function, passing in the string "dockerdwrapper" and a pointer to the error struct. This function  call initializes the ax_parameter pointer to point to the newly created AXParameter struct.
-The function checks if ax_parameter is NULL. If it is, this means that an error occurred while creating the AXParameter struct. The function logs an error message using syslog and jumps to the end of the function using the goto statement to clean up any resources and return NULL.

-If ax_parameter was successfully created, the function continues to the next step.

                                  static char *
                                  get_parameter_value(const char *parameter_name)
                                  {
                                    GError *error = NULL;
                                    AXParameter *ax_parameter = ax_parameter_new("dockerdwrapper", &error);
                                    char *parameter_value = NULL;

                                    if (ax_parameter == NULL) {
                                      syslog(LOG_ERR, "Error when creating axparameter: %s", error->message);
                                      goto end;
                                    }

                  U:1.0 Test if the attacker can remove the "dockerdwrapper" and replace it with the same parameter name to manipulate the Application 
                          to trust attacker parameter_name(attacker--> dockerdwrapper).
                  U:1.1 Install docker-ACAP with out TLS and that mean it will run on port 2375, could the attacker get the files inside dockerdwrapper which are  
                          *conf *docker-init * docker proxy * dockerd etc.. then add *server-cert.pem *server-key.pem *ca.pem before upload the files agin to the camera, if the attacker can do this then will have own TLS.

                                  if (!ax_parameter_get(
                                          ax_parameter, parameter_name, &parameter_value, &error)) {
                                    syslog(LOG_ERR,
                                          "Failed to fetch parameter value of %s. Error: %s",
                                          parameter_name,
                                          error->message);

                                    free(parameter_value);
                                    parameter_value = NULL;
                                  }
                  U:2.0 The previous case should verify that the parameter_name is eligible to continue.
                        While this part could be dependable on previous or provided asserted name so no need to give more credits.

-The function jumps to the end of the function using the goto statement to clean up any resources and return parameter_value.
                                  end:
                                    if (ax_parameter != NULL) {
                                      ax_parameter_free(ax_parameter);
                                    }
                                    g_clear_error(&error);

                                    return parameter_value;
                                  }

-The function calls the ax_parameter_get function to retrieve the value of the parameter_name parameter. The function passes in the ax_parameter pointer, a pointer to the parameter_value variable, and a pointer to the error struct. If ax_parameter_get returns false, this means that an error occurred. The function logs an error message using syslog, frees the memory allocated for parameter_value, and sets it to NULL.
-If ax_parameter_get returns true, the function continues to the next step.
-The function checks if ax_parameter is not NULL. If it is not, the function frees the memory allocated for ax_parameter using ax_parameter_free.
-The function clears any errors stored in the error struct using the g_clear_error function.

                  U:3.0  Optional:  Get the sys_log output and investigate the process that intreprreted above and if the end step was reached,
                                    verify that from the logs to be more critical (apply VAPIX commands).




### Start a new dockerd process. True otherwise False. 

                                  static bool
                                  start_dockerd(void)
                                  {
                                    GError *error = NULL;

                                    bool return_value = false;
                                    bool result = false;

                                    gsize args_len = 1024;
                                    gsize msg_len = 128;
                                    gchar args[args_len];
                                    gchar msg[msg_len];
                                    guint args_offset = 0;
                                    gchar **args_split = NULL;

                                    // Read parameters
                                    char *use_sd_card_value = get_parameter_value("SDCardSupport");
                                    char *use_tls_value = get_parameter_value("UseTLS");
                                    char *use_ipc_socket_value = get_parameter_value("IPCSocket");
                                    if (use_sd_card_value == NULL || use_tls_value == NULL || use_ipc_socket_value == NULL) {
                                      goto end;
                                    }
                                    bool use_sdcard = strcmp(use_sd_card_value, "yes") == 0;
                                    bool use_tls = strcmp(use_tls_value, "yes") == 0;
                                    bool use_ipc_socket = strcmp(use_ipc_socket_value, "yes") == 0;

-The function starts by declaring and initializing several variables, including a GError pointer named error, two boolean variables named return_value and result, and several other variables related to command line arguments.

-The next block of code declares three char* variables named use_sd_card_value, use_tls_value, and use_ipc_socket_value, and initializes them with the values returned from calling the get_parameter_value function with the corresponding parameter names.

-If any of the three get_parameter_value function calls return a NULL value, the function jumps to the end label using the goto statement. This indicates that there was an error reading one or more of the required parameters.

-The next block of code compares the retrieved values for use_sd_card_value, use_tls_value, and use_ipc_socket_value to the string "yes" using the strcmp function. If the comparison returns 0, the corresponding boolean variables use_sdcard, use_tls, and use_ipc_socket are set to true; otherwise, they are set to false.

                              U:1.0 The Parameters Variables are const and should not be able to change, compared successfully and if something missing,
                                    then the end will be implemented. Nothing to be tested.



<!-- -If all of the required parameters were read successfully, the function proceeds with starting the Docker daemon process by constructing a command line argument string using the g_snprintf function and calling the g_shell_parse_argv function to split the argument string into an array of strings. It then calls the g_spawn_async function to launch the dockerd process with the specified arguments.

-If the g_spawn_async function returns a value greater than 0, indicating that the process was launched successfully, the function sets return_value to true and proceeds to the end label.

-If any errors occur during the function's execution, the function sets error to a non-NULL value and logs an error message using the g_error function. It then proceeds to the end label. -->

                                    if (use_sdcard) {
                                      // Confirm that the SD card is usable
                                      char *sd_file_system = get_sd_filesystem();
                                      if (sd_file_system == NULL) {
                                        syslog(LOG_ERR,
                                              "Couldn't identify the file system of the SD card at %s",
                                              sd_card_path);
                                        goto end;
                                      }

                                      if (strcmp(sd_file_system, "vfat") == 0 ||
                                          strcmp(sd_file_system, "exfat") == 0) {
                                        syslog(LOG_ERR,
                                              "The SD card at %s uses file system %s which does not support "
                                              "Unix file permissions. Please reformat to a file system that "
                                              "support Unix file permissions, such as ext4 or xfs.",
                                              sd_card_path,
                                              sd_file_system);
                                        goto end;
                                      }

                                      if (!setup_sdcard()) {
                                        syslog(LOG_ERR, "Failed to setup SD card.");
                                        goto end;
                                      }
                                    }
                                    args_offset += g_snprintf(args + args_offset, args_len - args_offset, "%s %s",
                                        "dockerd",
                                        "--config-file /usr/local/packages/dockerdwrapper/localdata/daemon.json");

                                    g_strlcpy(msg, "Starting dockerd", msg_len);

                                    if (use_tls) {
                                      const char *ca_path = "/usr/local/packages/dockerdwrapper/ca.pem";
                                      const char *cert_path =
                                          "/usr/local/packages/dockerdwrapper/server-cert.pem";
                                      const char *key_path = "/usr/local/packages/dockerdwrapper/server-key.pem";

                                      bool ca_exists = access(ca_path, F_OK) == 0;
                                      bool cert_exists = access(cert_path, F_OK) == 0;
                                      bool key_exists = access(key_path, F_OK) == 0;

                                      if (!ca_exists) {
                                        syslog(LOG_ERR,
                                              "Cannot start using TLS, no CA certificate found at %s",
                                              ca_path);
                                      }
                                      if (!cert_exists) {
                                        syslog(LOG_ERR,
                                              "Cannot start using TLS, no server certificate found at %s",
                                              cert_path);
                                      }
                                      if (!key_exists) {
                                        syslog(LOG_ERR,
                                              "Cannot start using TLS, no server key found at %s",
                                              key_path);
                                      }

                                      if (!ca_exists || !cert_exists || !key_exists) {
                                        goto end;
                                      }

                                      args_offset += g_snprintf(args + args_offset, args_len - args_offset, " %s %s %s %s %s %s %s %s",
                                          "-H tcp://0.0.0.0:2376",
                                          "--tlsverify",
                                          "--tlscacert", ca_path,
                                          "--tlscert", cert_path,
                                          "--tlskey", key_path);

                                      g_strlcat (msg, " in TLS mode", msg_len);
                                    } else {
                                      args_offset += g_snprintf(args + args_offset, args_len - args_offset, " %s %s",
                                          "-H tcp://0.0.0.0:2375",
                                          "--tls=false");

                                      g_strlcat (msg, " in unsecured mode", msg_len);
                                    }

                                    if (use_sdcard) {
                                    args_offset += g_snprintf(args + args_offset, args_len - args_offset, " %s",
                                        "--data-root /var/spool/storage/SD_DISK/dockerd/data");

                                    g_strlcat (msg, " using SD card as storage", msg_len);
                                  } else {
                                    g_strlcat (msg, " using internal storage", msg_len);
                                  }

                                  if (use_ipc_socket) {
                                    args_offset += g_snprintf(args + args_offset, args_len - args_offset, " %s",
                                        "-H unix:///var/run/docker.sock");

                                    g_strlcat (msg, " with IPC socket.", msg_len);
                                  } else {
                                    g_strlcat (msg, " without IPC socket.", msg_len);
                                  }

                                  // Log startup information to syslog.
                                  syslog(LOG_INFO, "%s", msg);

                                  args_split = g_strsplit(args, " ", 0);
                                  result = g_spawn_async(
                                      NULL,
                                      args_split,
                                      NULL,
                                      G_SPAWN_DO_NOT_REAP_CHILD | G_SPAWN_SEARCH_PATH,
                                      NULL,
                                      NULL,
                                      &dockerd_process_pid,
                                      &error);
                                  if (!result) {
                                    syslog(
                                        LOG_ERR,
                                        "Could not execv the dockerd process. Return value: %d, error: %s",
                                        result,
                                        error->message);
                                    goto end;
                                  }

                                  // Watch the child process.
                                  g_child_watch_add(dockerd_process_pid, dockerd_process_exited_callback, NULL);

                                  if (!is_process_alive(dockerd_process_pid)) {
                                    // The process died during adding of callback, tell loop to quit.
                                    exit_code = -1;
                                    g_main_loop_quit(loop);
                                    goto end;
                                  }

                                  return_value = true;

                                end:
                                  g_strfreev(args_split);
                                  free(use_sd_card_value);
                                  free(use_tls_value);
                                  free(use_ipc_socket_value);
                                  g_clear_error(&error);

                                  return return_value;
                                }