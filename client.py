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
import select
import errno
import sys
import json
import hashlib
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
"""
from Crypto.Cipher import AES
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
"""

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12345
client_secret = 5

# DH-SPEKE
pwd = 3
pwd_v2 = 34
#s = hashlib.sha256(psswd.encode()).hexdigest()

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket = socket.socket()
client_socket.connect((IP, PORT))

# Receiving DH variables
step1 = client_socket.recv(1024)

# Parsing DH variables
jsonData = json.loads(step1.decode())
jsonData = jsonData["dh-keyexchange"]
generator = int(jsonData["generator"])
prime = int(jsonData["prime"])
serverA = int(jsonData["serverA"])


print("Client secret: " + str(client_secret))
print("Prime: " + str(prime))
print("Generator: " + str(generator))
print("Server Public Key: " + str(serverA))
print("Password: " + str(pwd))

if (serverA < 2 or serverA > (prime-2)):
    print("Possible small subgroup confinement attack. Aborting on client side.")
    sys.exit(0)

# Calculating client shared secret
clientB = (pow(generator, client_secret)) % prime

# Sending back to server
step2 = "{"
step2 += "\"dh-keyexchange\":"
step2 += "{"
step2 += "\"step\": {},".format(2)
step2 += "\"clientB\": {}".format(clientB)
step2 += "}}"
client_socket.send(step2.encode())

# Calculating shared secret
sharedSecret = pow(serverA, client_secret) % prime
print("Shared secret: " + str(sharedSecret))

# Receive shouldn't block
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    # if not emtpy
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        
        # We can pass in the shared secret from the key exchange here to an
        # encryption algorithm like AES, but we're having issues using the 
        # Python AES library at the moment.
        """
        key = sharedSecret.to_bytes(2, 'little')
        pad(key, 16)
        cipher = AES.new(key, AES.MODE_ECB)
        message_e = cipher.encrypt(message)
        """
        
        # Send message
        client_socket.send(message_header + message)
    
    try:
        while True:
            # Receive stuff
            username_header = client_socket.recv(HEADER_LENGTH)
            # Didn't get any data
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()

            # Grabbing username
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            
            # Grabbing message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")
            
    except IOError as e:
        # Errors we might see depending on OS when there are no more messages to recieve
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue
            
    except Exception as e:
        print('Error', str(e))
        sys.exit()

client_socket.close()