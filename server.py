# Source: https://codinginfinite.com/python-chat-application-tutorial-source-code/
"""
Steps from Source:
1. Create socket
2. Communicate the socket address
3. Keep waiting for an incoming connection request/s
4. Connect to client
5. Receive the message
6. Decode the destination user and select the socket
7. Send a message to the intended client
8. Keep repeating step 5 & 6 as per users wish
9. Exit i.e. end the communication by terminating the connection
"""

import socket
import select
import json

# Setting up the server
IP = "127.0.0.1"
PORT = 12345
# Header holds the length of the message
HEADER_LENGTH = 10
# List of sockets (i.e. socket information for each client)
# List of connected users (Key: socket name, Value: user data)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP,PORT))
server_socket.listen()

socket_list = []
socket_list.append(server_socket)
users = {}

# DH variables
server_secret = 4
prime = 23
generator = 9
serverA = (pow(generator, server_secret)) % prime


print(f"Listening for connections on {IP}:{PORT}...")

# Handles receiving messages
def recv_msg(client_socket):
    try:
        # Grabbing message header
        message_header = client_socket.recv(HEADER_LENGTH)
        
        # If empty, exit
        if not (len(message_header)):
            return False
        
        # Grabbing message length as int
        message_length = int(message_header.decode("utf-8").strip())
        # Return dictionary containing message information
        return {"header": message_header, "data": client_socket.recv(message_length)}

    # Catching an error where clients message is not properly received
    except:
       return False

# Server actions
while True:
    # List of ready to read, ready to write, and exception sockets
    #ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[], socket_list)
    for sock in ready_to_read:
        # Someone just connected
        if sock == server_socket:
            # Bringing in the client connetion
            client_socket, client_address = server_socket.accept()

            step1 = "{"
            step1 += "\"dh-keyexchange\":"
            step1 += "{"
            step1 += "\"step\": {},".format(1)
            step1 += "\"generator\": {},".format(generator)
            step1 += "\"prime\": {},".format(prime)
            step1 += "\"serverA\": {}".format(serverA)
            step1 += "}}"
            client_socket.send(step1.encode())
            
            step2 = client_socket.recv(1024)
            
            jsonData = json.loads(step2.decode())
            jsonData = jsonData["dh-keyexchange"]
            
            clientB = int(jsonData["clientB"])
            
            sharedSecret = pow(clientB, server_secret) % prime
           
            #print("Server secret: " + str(sharedSecret))

            user = recv_msg(client_socket)
            # Someone disconnected
            if user is False:
                    continue

            #print("Sending prime to client")
            #client_socket.send((f"Prime {prime} and generator {generator} received from server: ".encode('utf-8')))

            socket_list.append(client_socket)
            
            # Adding user to users dictionary, with socket as key
            users[client_socket] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
            #client_socket.send(f"You are connected from: {client_address}")
        else:
            try:
                message = recv_msg(sock)
                #data = sock.recv(2048)
                if message is False:
                    print(f"Closed connection from {users[sock]['data'].decode('utf-8')}")
                    socket_list.remove(sock)
                    del users[sock]
                    continue
                
                user = users[sock]
                #username = user['data'].decode('utf-8')
                print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                
                # Share message with everybody
                for c_sock in users:
                    # Don't want to send message back to sender
                    if c_sock != sock:
                        print("DO YOU SEE ME?")
                        c_sock.send(user['header'] + user['data'] + message['header'] + message['data'])

            except Exception as e:
                print('Error', str(e))
                continue

    for sock in in_error:
       socket_list.remove(sock)
       del users[sock] 

server_socket.close()