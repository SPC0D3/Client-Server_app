# Sohum Pete            210354790
# Dhanush Mohan-Kumar   210348040

# Import socket module
import socket
HOST = 'localhost'
PORT = 12345

def start_client():
    #Create a new TCP socket and connect to the host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  

    # The server will assign a name like Client01, Client02, etc.
    client_name = client_socket.recv(1024).decode()
   
    if client_name == "Failed to Connect":
            print("Failed to Connect")
            client_socket.close()
            return
   
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
