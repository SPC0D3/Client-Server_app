# Sohum Pete 210354790 
#

# Import socket module
import socket
import threading
import datetime

# Server Configuration
HOST = 'localhost'
PORT = 12345
MAX_CLIENTS = 3

# Cache to store client information (name, connection/disconnection times)
clients_cache = {}

# Repository of available files (for demonstration purposes)
file_repository = ['file1.txt', 'file2.txt', 'file3.txt']

def handle_client(client_socket, client_name):
    # Store connection time in cache
    clients_cache[client_name] = {
        'connected_at': datetime.datetime.now(),
        'disconnected_at': None
    }

    print(f"{client_name} connected.")

    while True:
        try:
            # Receive message from client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Handle different types of client requests
            if data == "status":
                # Send server cache details
                cache_info = "\n".join([f"{name}: connected at {details['connected_at']}, disconnected at {details['disconnected_at']}"
                                        for name, details in clients_cache.items()])
                client_socket.send(cache_info.encode())
            elif data == "list":
                # Send list of available files in repository
                file_list = "\n".join(file_repository)
                client_socket.send(file_list.encode())
            elif data.startswith("get "):
                # Handle file request
                requested_file = data.split(" ", 1)[1]
                if requested_file in file_repository:
                    client_socket.send(f"Sending contents of {requested_file}".encode())
                else:
                    client_socket.send("File not found".encode())
            elif data == "exit":
                # Handle client disconnection
                clients_cache[client_name]['disconnected_at'] = datetime.datetime.now()
                print(f"{client_name} disconnected.")
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

    client_count = 0

    while True:
        if client_count < MAX_CLIENTS:
            # Accept new client connection
            client_socket, addr = server_socket.accept()

            client_count += 1
            client_name = f"Client{client_count:02d}"  # Assign client a name like Client01, Client02, etc.

            # Send client name to the client
            client_socket.send(client_name.encode())

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
            client_thread.start()
        else:
            print("Max clients connected. No more clients can connect at this time.")

if __name__ == '__main__':
    start_server()
