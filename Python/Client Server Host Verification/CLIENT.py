import threading
import time
import socket as mysoc
import hmac


def clientConnect(portNumber, hostname):
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    port = portNumber
    sa_sameas_myaddr = mysoc.gethostbyname(hostname)
    # connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port)
    cs.connect(server_binding)
    data_from_server = cs.recv(1024)

    # receive data from the server
    print("\n" + "[C]: Data received from server: ", data_from_server.decode('utf-8'))
    print("\n")

    return cs

# Opens hostnames file and stores value in hostname String
def openFile(fileNameToOpen):
    try:
        fileName = fileNameToOpen
        hostname = [line.rstrip('\n') for line in open(fileName)]
        return hostname

    except IOError:
        print("Error: Invalid file name!")
        cs.send('EOF'.encode('utf-8'))
        cs.close()
        outputFile.close()
        exit()

# Get just the key value from a single line
def getKeyValue(inputString):
    temp = inputString.split()
    keyValue = temp[0]
    return keyValue

# Get just the challenge value from a single line
def getChallengeString(inputString):
    temp = inputString.split()
    challengeString = temp[1]
    return challengeString

def getHostname(inputString):
    temp = inputString.split()
    hostName = temp[2]
    return hostName

def client():

    # For first time Connection to TLDS Servers
    firstConnectTLDS1 = 1
    firstConnectTLDS2 = 1

    #*** UNCOMMENT BASED ON HOW THEY USE IT ****
    # RSHostName = 'LAPTOP-HP3NK2NL'
    RSHostName = mysoc.gethostname()
    csRS = clientConnect(50007, RSHostName)
    #csRS = clientConnect(50007, mysoc.gethostname())

    # Create output file to save hostname, ip, flag
    outputFile = open("RESOLVED.txt", "w+")
    outputFile.close()

    # Value used to connect to TS Server only once
    firstTime = 1

    # List of hostname from Proji-HNS
    # *** UNCOMMENT BASED ON HOW THEY USE IT ****
    inputClientFile = 'PROJ3-HNS.txt'
    # inputClientFile = sys.argv[2]
    clientHostnameList = openFile(inputClientFile)

    # Send each hostname from client List to RS Server and TS Server
    for x in range(len(clientHostnameList)):
        hostnameToSendAS = clientHostnameList.pop()

        # Get Key Value, Challenege, and Hostname
        keyValue = getKeyValue(hostnameToSendAS)
        challengeString = getChallengeString(hostnameToSendAS)
        hostNameToSendTLDS = getHostname(hostnameToSendAS)

        # Make digest value using keyValue and Challenge String
        digestValue = hmac.new(keyValue.encode(), challengeString.encode("utf-8"))
        print("Key and Challenege: " + keyValue + ' ' + challengeString)

        # Combine challenge and digest to send to AS Server
        challengeAndDigest = challengeString + ' ' + digestValue.hexdigest()
        print("Value to Send to AS Server: " + challengeAndDigest + "\n")
        csRS.send(challengeAndDigest.encode('utf-8'))

        # Receive Results from AS Server about which TLDS Server Matches Key
        stringFromRSServer = csRS.recv(1024).decode('utf-8').strip()


        # Depending on which Server is matched will try to connect to that server
        if(stringFromRSServer == "Server 1 Match"):
            stringFromRSServer = csRS.recv(1024).decode('utf-8').strip()
            if(firstConnectTLDS1 == 1):
                print("\n" + "Establishing Connection to TLDS1 Server: " + stringFromRSServer)
                conTLDS1 = clientConnect(52008, stringFromRSServer)
            firstConnectTLDS1 = firstConnectTLDS1 + 1
            print("HostName Sent To TLDS1 Server: " + hostNameToSendTLDS)
            conTLDS1.send(hostNameToSendTLDS.encode('utf-8'))
            hostFullIP = conTLDS1.recv(1024).decode('utf-8').strip()
            print("HOST IP FLAG From TLDS1 Server: ", hostFullIP)
            outputFile = open("RESOLVED.txt", "a")
            outputFile.write(hostFullIP + "\n")
            outputFile.close()


        elif(stringFromRSServer == "Server 2 Match"):
                stringFromRSServer = csRS.recv(1024).decode('utf-8').strip()
                if(firstConnectTLDS2 == 1):
                    print("\n" + "Establishing Connection to TLDS2 Server: " + stringFromRSServer)
                    conTLDS2 = clientConnect(52050, stringFromRSServer)
                firstConnectTLDS2 = firstConnectTLDS2 + 1
                print("HostName Sent To TLDS2 Server: " + hostNameToSendTLDS)
                conTLDS2.send(hostNameToSendTLDS.encode('utf-8'))
                hostFullIP2 = conTLDS2.recv(1024).decode('utf-8').strip()
                print("HOST IP FLAG From TLDS2 Server: ", hostFullIP2)
                outputFile = open("RESOLVED.txt", "a")
                outputFile.write(hostFullIP2 + "\n")
                outputFile.close()


        elif(stringFromRSServer == "Server No Match"):

            stringFromRSServer = csRS.recv(1024).decode('utf-8').strip()
            time.sleep(.50)
            if (firstConnectTLDS1 == 1):
                print("Hostname Server 1: ", stringFromRSServer)
                clientConnect(52008, stringFromRSServer)
            firstConnectTLDS1 = firstConnectTLDS1 + 1

            stringFromRSServer = csRS.recv(1024).decode('utf-8').strip()

            if (firstConnectTLDS2 == 1):
                print("Hostname Server 2: ", stringFromRSServer)
                clientConnect(52050, stringFromRSServer)
            firstConnectTLDS2 = firstConnectTLDS2 + 1

        print("\n")

    lines = []
    with open('RESOLVED.txt') as f:
        lines = f.readlines()

    with open('RESOLVED.txt', 'w') as f:
        for line in reversed(lines):
            f.write(line)
    # Reached end of file, no more hostnames to send > Close all connections
    csRS.send("EOF".encode('utf-8'))
    print("Connection to RS Server Closed")
    csRS.close()
    print("Connection to TLDS1 Server Closed")
    conTLDS1.close()
    print("Connection to TLDS2 Server Closed")
    conTLDS2.close()

t2 = threading.Thread(name='client', target=client)
t2.start()