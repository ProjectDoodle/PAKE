# Introduction
This repo contains our final project code for NMTs CSE541 Cryptograpy class.

# PAKE
Our final project covers PAKE implementation through a chat app, and subsequent PAKE cryptanalysis.

# Usage
*Current as of 11/6/21*

Our chat application consists of a `server.py` and `client.py` script.
Steps for running the sample Chat application:
1. Open a terminal and Run the server-chat.py
2. Open a new terminal and run client-chat.py
	a) Enter the username with a ‘#’ prefix. Example: #alice
	b) Now, send the message to a user by following the format @username:message. Example: @bob:Hello, Bob! This is alice
3. Repeat step 2 for other users. (Maximum 5 users is allowed with server configuration i.e. server_socket.listen(5)

# To-Do
1. Finish chat app implementation
2. Apply DH-EKE to messages
3. Apply "some" cryptanalysis on messages

# Questions:
1. Is DH used to generate a key between each client and the server? Or is it just used for key generation between clients?
2. Why is the server not broadcasting the message a client sends? But also, does it matter? If DH is used between the client and
   server, then we can just work with that.

Make sure to view messages at each stage. We can demo what is viewable at from non-encrypted chat app -> DH -> DH-EKE.

# References
* [Chat application implementation]( https://codinginfinite.com/python-chat-application-tutorial-source-code/)
* [PAKE Wiki](http://cryptowiki.net/index.php?title=Password-authenticated_key_agreement)
