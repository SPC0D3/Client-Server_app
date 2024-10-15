# Sohum Pete 210354790
# 
# Note: Please open each client in a separate terminal as the confusion of executing this file more than once in the same 
#       terminal causes the previous instances of the client in said terminal to remain open if it was not exited beforehand
#       (We do not yet know how to return to the previous instances of the client to close the instance if it can be done)

# Import socket module

import socket
HOST = 'localhost'
PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # Connect to the server

    # The server will assign a name like Client01, Client02, etc.
    client_name = client_socket.recv(1024).decode()
    print(f"Connected to server as {client_name}")

    while True:
        # User input to send message
        message = input(f"{client_name}> ")

        if message == "exit":
            client_socket.send(message.encode())  # Send 'exit' command to disconnect
            print("Disconnecting from server...")
            break
        elif message == "status":
            client_socket.send(message.encode())  # Request server cache
        elif message == "list":
            client_socket.send(message.encode())  # Request list of files from server
        elif message.startswith("get "):
            client_socket.send(message.encode())  # Request a file from server
        else:
            client_socket.send(message.encode())  # Send a regular message to the server

        # Receive response from the server
        server_response = client_socket.recv(1024).decode()
        print(f"Server> {server_response}")

    # Close the socket when done
    client_socket.close()

if __name__ == '__main__':
    start_client()
