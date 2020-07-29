import numpy as mypy
import threading
import time
import random
import socket as mysoc
import sys
import hmac

def serverConnect(port):
    print("\n" + "New Server Running")
    #Server listens for client connection
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', port)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a RSServer at", addr)
    print("\n")

    # send a intro  message to the client.
    msg = localhost_ip
    csockid.send(msg.encode('utf-8'))

    return csockid, ss

# get List of hostname only from List of full hostname, IP, Flag
def getHostName(list):
    hostNameList = []
    for x in range(len(list)):
        temp = list[x].split()
        hostNameOnly = temp[0]
        hostNameList.append(hostNameOnly)
    return hostNameList

#Open file and save to List
def openFile(fileName):
    try:
        listOfEntries = [line.strip() for line in open(fileName)]
        return listOfEntries

    except IOError:
        print("Error: Invalid file name!")
        exit()

def server():
    firstTime = 1
    csockid,ss = serverConnect(51008)

    # ******* UNUSURE HOW THEY WILL GRADE ********
    # Gets a list of keys
    inputComFile = 'PROJ3-KEY1.txt'
    # inputComFile = sys.argv[1]
    listOfKeys = openFile(inputComFile)

    # Open List of Hostname
    hostNameListFull = openFile('PROJ3-TLDS1.txt')
    hostNameOnlyList = getHostName(hostNameListFull)

    while True:
        waitForClientConnect = False
        hostnameReceived = csockid.recv(1024).decode('utf-8').strip()

        if (hostnameReceived == "EOF"):
            break
        print("Challenge String received from AS Server: ", hostnameReceived)


        # Traverse through list of key Values
        for y in range(len(listOfKeys)):

            # Convert hostname with all key values to digest value and Send response back to AS server

            digestValue = ""
            digestValue = hmac.new(listOfKeys[y].encode(), hostnameReceived.encode("utf-8"))
            csockid.send(digestValue.hexdigest().encode('utf-8'))
            time.sleep(.15)
        csockid.send("END".encode('utf-8'))

        matchResult = csockid.recv(1024).decode('utf-8').strip()
        print("Match Result: " + matchResult + "\n")
        if(matchResult == "Match"):
            waitForClientConnect = True

            if(firstTime == 1):
                csockid2, ss2 = serverConnect(52008)
            firstTime = firstTime + 1

        if(waitForClientConnect == True):
            hostnameClient = csockid2.recv(1024).decode('utf-8').strip()
            print("Hostname sent from client: ", hostnameClient)
            hostFound = False
            for x in range(len(hostNameOnlyList)):
                #print("Compare (C to L): " + hostnameClient + " : " + hostNameOnlyList[x])
                if (hostNameOnlyList[x] == hostnameClient):
                    hostFound = True
                    print("Match : Hostname Value sent to Client: " + hostNameListFull[x] + "\n")
                    csockid2.send(hostNameListFull[x].encode('utf-8'))
                    break
            if (hostFound == False):
                hostNotFound = hostnameClient + " ERROR - HOST NOT FOUND"
                print("No Match : Hostname Value sent to Client: " + hostNotFound + "\n")
                csockid2.send(hostNotFound.encode('utf-8'))




    print("Connection to RS Server Closed")
    csockid.close()
    ss.close()
    print("Connection to Client Closed")
    csockid2.close()
    ss2.close()
    exit()


t1 = threading.Thread(name='server', target=server)
t1.start()
time.sleep(random.random() * 5)