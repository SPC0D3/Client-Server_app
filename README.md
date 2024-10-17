# Client-Server_app by Sohum Pete and Dhanush Mohan-Kumar
To operate, follow the below steps.

1. Run the server.py file
2. Run the client.py file (in a separate terminal)
3. If you would like to open more than 1 client then open another new terminal and repeat step 2
4. You are now able to run commands on each of the clients that were able to connect to the server
5. If you would like to append 'ACK' to a string then enter any string and it will return the string + ACK at the end (note no command is needed as this is default functionality)
6. If you would like to know the status of all the clients that have connected now and in the past, type the command 'status' and you will see a list of clients with their connection and disconnection date and timestamp
7. If you would like to see the list of files in the current working directory, type 'list'
8. If you would like a specific file from the current working directory to have its content streamed to the terminal then type the name of the file (no extension name)   note: this function has only been tested with txt files thus far
9. If you are finished with the client then type 'exit' to disconnect the client from the server

Features to Add
1. Print a list of the commands for the client at the beginning of its session
2. Navigation between directories
3. Broader file type streaming capability beyond txt files
4. Error handling to disconnect a client if there is an attempt to open multiple clients from the same terminal without disconnecting the established client entity
