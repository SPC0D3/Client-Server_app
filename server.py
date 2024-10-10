# Saad Rehan, 210723520
# Rajanbir Bhitewid, 210361510

# Import socket module
from socket import * 
import sys # In order to terminate the program
import struct

# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))


print("SERVER: ----------Start of Stage A----------")
#Receiving client-side packet
packet, clientAddress = serverSocket.recvfrom(1024)

data_length, pcode, entity, data = struct.unpack("!IHH14sxx", (packet))

padding = (4 - (len(data) % 4)) % 4
data+=bytearray(padding)

packet_length = len(packet)
print("Receiving from client: data: {} data_length: {} pcode: {} entity: {}".format(data, data_length,pcode, entity))


if packet_length %4 !=0:
    print("ERROR: The packet length is not divisible by four, exiting.")
    serverSocket.close
    exit()
    
elif pcode !=0:
    print("ERROR: Unexpected value for pcode, exiting.")
    serverSocket.close
    exit() 

elif data_length != len(data):
    print("ERROR: Length of data does not match, exiting.")
    serverSocket.close
    exit()

#Creating server side packet
repeat = 6
udp_port = 25000
server_len = 12
codeA = 237
server_entity = 2
serverPacket = struct.pack("!IHHIIHH",data_length, pcode, server_entity, repeat, udp_port, server_len, codeA)
serverSocket.sendto(serverPacket, clientAddress)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", udp_port))
print("NEW SERVER: udp_port ready to receive: {}".format(udp_port))

print("\nSERVER: ----------End of Stage A----------")
print("\nSERVER: ----------Start of Stage B----------")

for acked_id in range(repeat):
    #Receiving client side Phase B packet
    newPacket, clientAddress = serverSocket.recvfrom(1024)
    # data, clientAddress = serverSocket.recvfrom(1024)
    # packet_length = len(newPacket)
    data_length, pcode, entity, packet_id = struct.unpack('!IHHI',newPacket[:12])
    data = struct.unpack("!{}s".format(data_length), newPacket[12:])
    print("FROM UDP CLIENT--- pcode: {} entity: {} packet_id: {} data_length: {} data: {}".format(pcode, entity,packet_id, data_length, data))

    #Verifying Client side packet
    if data_length % 4 != 0:
        print("ERROR: Data is not divisible by 4, exiting.")
        serverSocket.close()
        exit()
    elif pcode != codeA:
        print("ERROR: Unexpected pcode, exiting.")
        serverSocket.close()
        exit()
    elif data_length != len(data[0]):
        print("ERROR: Data length does not match, exiting.")
        serverSocket.close()
        exit()

    #Sending acknowledgement packet 
    serverPacket = struct.pack('!IHHI', data_length, pcode, server_entity, acked_id)
    serverSocket.sendto(serverPacket, clientAddress)

#Creating and sending TCP server address
tcp_port = 29450
codeB = 367

tcp_packet = struct.pack("!IHHII", data_length, pcode, entity, tcp_port, codeB)
serverSocket.sendto(tcp_packet, clientAddress)
print("\nSERVER: ----------End of Stage B----------")
print("\nSERVER: ----------Start of Stage C----------")

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", tcp_port))

serverSocket.listen(5)

connectionSocket, addr = serverSocket.accept()
print('The server is ready to receive on tcp port: {}'.format(tcp_port))

repeat2 = 8
server_len2 = 70
codeC = 380
server_char = b"S"
data_length = 13 

packet = struct.pack("!IHHIIIc", data_length, codeB, 2, repeat2, server_len2, codeC, server_char)
connectionSocket.send(packet)
print("\nSERVER: ----------End of Stage C----------")
print("\nSERVER: ----------Start of Stage D----------")

for i in range (repeat2):
    packetD = connectionSocket.recv(1048)
    #data = connectionSocket.recv(1024)
    data_length, pcode, entity = struct.unpack("!IHH", packetD[:8])
    data = struct.unpack("!{}s".format(data_length), packetD[8:])
    print("FROM TCP CLIENT--- pcode: {} entity: {} data_length: {} data: {}".format(pcode, entity, data_length, data))

codeD = 234

final_packet = struct.pack("!IHHI", data_length, codeC, 2, codeD)
connectionSocket.send(final_packet)
print("\nSERVER: ----------End of Stage D----------")

serverSocket.close()  
sys.exit()#Terminate the program after sending the corresponding data