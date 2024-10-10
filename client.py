# Saad Rehan, 210723520
# Rajanbir Bhitewid, 210361510

# Import socket module
from socket import * 
import sys # In order to terminate the program
import struct
import time

# serverName = 'localhost'
serverName = '34.67.93.93'

# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)

print("CLIENT: ----------Start of Stage A----------")

data = b'Hello World!!!'
padding = (4 - (len(data) % 4)) % 4
data+=bytearray(padding)

data_length = len(data)

client_entity = 1
pcode = 0

# Now use the encoded bytes in struct.pack
packet = struct.pack("!IHH14sxx", data_length, pcode, client_entity, data)

clientSocket. sendto(packet, (serverName, serverPort))

serverPacket, serverAddress = clientSocket.recvfrom(2048)

#Receiving server side packet
data_length, pcode, entity, repeat, udp_port, server_len, codeA = struct.unpack("!IHHIIHH",serverPacket)
print('Receiving from server: data_length: {} pcode: {} entity: {} repeat: {} udp_port: {} server_len: {} codeA: {}'.format(data_length, pcode, entity, repeat, udp_port, server_len, codeA))

print("CLIENT: ----------End of Stage A----------")

print("\nCLIENT: ----------Start of Stage B----------")

pcode = codeA

data = 0
data = b'0'*server_len
padding = (4 - (len(data) % 4)) % 4
data += bytearray(padding)

header_length = len(data) + 4

for packet_id in range(repeat):
    
    #Packing Client Side Phase B packet
    format_str = "!IHHI{}s".format(header_length)
    newPacket = struct.pack(format_str, header_length, pcode,client_entity,packet_id, data)
    
    clientSocket. sendto(newPacket, (serverName, udp_port))

    #Receiving Server Side Phase B packet

    try:    
        serverPacket, serverAddress = clientSocket.recvfrom(2048)
    except TimeoutError:
        continue
    
    data_length, pcode, entity, acked_packet_id = struct.unpack("!IHHI", serverPacket)

    #Verfication suceeded, print contents
    print("From server--- data_length: {} pcode: {} entity: {} acked_packet_id: {}".format(data_length, pcode, entity, acked_packet_id))


tcp_packet, serverAddress = clientSocket.recvfrom(2048)
data_length, pcode, entity, tcp_port, codeB = struct.unpack("!IHHII", tcp_packet)

print("FROM UDP SERVER --- ")
print("data_length: {} pcode: {} entity: {} tcp_port: {} codeB: {}".format(data_length, pcode, entity, tcp_port, codeB))
print("\nCLIENT: ----------End of Stage B----------")
clientSocket.close()

print("\nCLIENT: ----------Start of Stage C----------")

print("Connecting to server at TCP port {}".format(tcp_port))
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, tcp_port))

time.sleep(2)

packetC, serverAddress = clientSocket.recvfrom(2048)
data_length, codeB, entity, repeat2, server_len2, codeC, server_char = struct.unpack("!IHHIIIc", packetC)
print("Received packet from server: data_length: {} codeB: {} entity: {} repeat2: {} len2: {} codeC: {} Char: {}".format(data_length, codeB, entity, repeat2, server_len2, codeC, server_char))
print("\nCLIENT: ----------End of Stage C----------")

print("\nCLIENT: ----------Start of Stage D----------")
pcode = codeC

if (server_len2)%4 != 0:
    len2_adjust = server_len2 + (4 - (server_len2%4))
else: len2_adjust = server_len2

data = server_char*len2_adjust
phased_data_length = len(data)
packetD = struct.pack("!IHH{}s".format(len(data)),len2_adjust, pcode, 1, data)
for _ in range(repeat2):
    clientSocket.sendto(packetD, (serverName, tcp_port))

final_packet, serverAddress = clientSocket.recvfrom(1048)
data_length, pcode, entity, codeD = struct.unpack("!IHHI", final_packet)

print("FROM TCP SERVER--- data_length: {} pcode: {} entity: {} codeD: {}".format(data_length, pcode, entity, codeD))
print("\nCLIENT: ----------End of Stage D----------")
clientSocket.close()
