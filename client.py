# Source: https://codinginfinite.com/python-chat-application-tutorial-source-code/
"""
Steps from Source:
1. Create a unique client socket per instance/user
2. Connect to the server with given socket address (IP and port)
3. Send and receive messages
4. Repeat step 3 as per configuration
5. Close the connection
"""

import socket

client_socket = socket.socket()
port = 12345
client_socket.connect(('127.0.0.1',port))

#recieve connection message from server
recv_msg = client_socket.recv(1024)
print(recv_msg)

#send user details to server
send_msg = input("Enter your user name(prefix with #):")
client_socket.send(send_msg)


#receive and send message from/to different user/s

while True:
    recv_msg = client_socket.recv(1024)
    print(recv_msg)
    send_msg = input("Send your message in format [@user:message] ")
    if send_msg == 'exit':
        break;
    else:
        client_socket.send(send_msg)

client_socket.close()