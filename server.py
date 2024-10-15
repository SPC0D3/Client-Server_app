# Sohum Pete 210354790 
#


#note: The 'list' and 'get' commands work only for the current working directory


# Import socket module
import socket
import threading
import datetime
import os

# Server Configuration
HOST = 'localhost'
PORT = 12345
MAX_CLIENTS = 3

# Cache to store client information (name, connection/disconnection times)
clients_cache = {}

client_count = 0  # Move client_count to the global scope
client_lock = threading.Lock()  # Created a threading lock to safely decrement client_count globally without causing a race condition

def handle_client(client_socket, client_name):
    # Store connection time in cache
    clients_cache[client_name] = {'connected_at': datetime.datetime.now(), 'disconnected_at': None}

    print(f"{client_name} connected.")

    while True:
        try:
            # Receive message from client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Handle different types of client requests
            if data == "status":
                
                # Send server cache details by appending them to a single string
                cache_info = ""

                for name, details in clients_cache.items():
                    cache_info += f"{name}: connected at {details['connected_at']}, disconnected at {details['disconnected_at']}\n"
                #print the string to the client  
                client_socket.send(cache_info.encode())                
                
            elif data == "list":

                file_list = "\n".join(os.listdir())  # Join the list of files into a single string
                client_socket.send(file_list.encode())  # Encode and send the file list

            elif data.startswith("get "):
                # Handle file request
                requested_file = data.split(" ", 1)[1]

                if os.path.exists(requested_file): #Check if the file exists in the current directory
                    with open(requested_file, 'r') as f: #Opens entered file in read mode and stores content in file_contents variable
                        file_contents = f.read()
                        client_socket.send(file_contents.encode())
                else:
                    client_socket.send("File not found".encode())

            elif data == "exit":
                # Handle client disconnection
                clients_cache[client_name]['disconnected_at'] = datetime.datetime.now()
                print(f"{client_name} disconnected.")

                with client_lock:
                    global client_count
                    client_count -= 1

                break

            else:
                # Echo message back with "ACK"
                response = f"{data} ACK"
                client_socket.send(response.encode())
        except:
            break

    # Close connection and free resources
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening...")

    max_clients_reached = False
    global client_count
    client_id_num = 0

    while True:
        with client_lock:
            if client_count < MAX_CLIENTS:
                # Accept new client connection
                client_socket, addr = server_socket.accept()

                # Reset the max client flag for the else statement so it prints the statement if its reached again
                max_clients_reached = False
                client_count += 1 # Tracks the number of active clients
                client_id_num += 1 # Separate variable to track client id number in cache and console 
                client_name = f"Client{client_id_num:02d}"  # Assign client a name like Client01, Client02, etc.

                # Send client name to the client
                client_socket.send(client_name.encode())

                # Start a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
                client_thread.start()
            else:
                # Prevents infinite printing of the statement with the max clients flag which is reset if the counter decrements
                if not max_clients_reached:
                    print("Max clients connected. No more clients can connect at this time.")
                    max_clients_reached = True  # Set the flag to avoid repeated messages

if __name__ == '__main__':
    start_server()
