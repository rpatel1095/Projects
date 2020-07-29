# Client Server Host Verification
This project was created to practice connecting a client socket to a server socket. The server socket then communicates with additional server sockets to verify if the hashed information from the client is valid or invalid.

Installation
* All files .txt files present must exist in the same directory as the four python files

Usage
* The user will run the three server files first in the following order: AS.py, TLDS1.py, TLDS2.py
* Then the user will run the client.py file and the communication between the server and client should began
* The files are written such that it will fetch the name of your local host machine as the hosting server.

Purpose:
* The client will iterate each line in the file “PROJ3-HNS.txt” which consist of a key, hostname pair
	o The key will be used to hash the hostname
* The hashed hostname will then be sent to the AS server to validate if the host name is valid.
* The AS server will then first try to connect to the TLDS1 server 
	o The TLDS1 server contains a list of host name in “PROJ3-TLDS1.txt”
	o The TLDS1 server will then fetch a key value stored in the “PROJ3-KEY1.txt” and hash all the host names from the previous step
	o It will then check if the hashed hostname from the AS server matches any values from it’s list of hashed servers
* If found: it will return to the AS server a match was found
* Else:  it will return to the AS server no match found
* Depending on the response from the TLDS1 Server:
	o If found: The AS server will respond back to the client that the host name is valid
	o If not found: the above steps are repeated to connect with TLDS2 Server
* The client will then write down the host name followed by “Error Host Not Found” or just the hostname in a “RESOLVED.txt” file to notify which servers are valid and which are not inside the servers







