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

# References
* [Chat application implementation]( https://codinginfinite.com/python-chat-application-tutorial-source-code/)
* [PAKE Wiki](http://cryptowiki.net/index.php?title=Password-authenticated_key_agreement)
