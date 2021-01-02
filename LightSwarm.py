'''
    LightSwarm Raspberry Pi Logger 
    SwitchDoc Labs 
    December 2020
'''
from __future__ import print_function
 
from builtins import chr
from builtins import str
from builtins import range
import sys  
import time 
import random

from netifaces import interfaces, ifaddresses, AF_INET

from socket import *

VERSIONNUMBER = 7
# packet type definitions
LIGHT_UPDATE_PACKET = 0
RESET_SWARM_PACKET = 1
CHANGE_TEST_PACKET = 2   # Not Implemented
RESET_ME_PACKET = 3
DEFINE_SERVER_LOGGER_PACKET = 4
LOG_TO_SERVER_PACKET = 5
MASTER_CHANGE_PACKET = 6
BLINK_BRIGHT_LED = 7

MYPORT = 2910

SWARMSIZE = 5


logString = ""
# command from command Code

def completeCommand():

        f = open("/home/pi/SDL_Pi_LightSwarm/state/LSCommand.txt", "w")
        f.write("DONE")
        f.close()

def completeCommandWithValue(value):

        f = open("/home/pi/SDL_Pi_LightSwarm/state/LSResponse.txt", "w")
        f.write(value)
        print("in completeCommandWithValue=", value)
        f.close()

        completeCommand()


def processCommand(s):
        f = open("//home/pi/SDL_Pi_LightSwarm/state/LSCommand.txt", "r")
        command = f.read()
        f.close()

        command = command.rstrip()        
        if (command == "") or (command == "DONE"):
            # Nothing to do
            return False

        # Check for our commands
        #pclogging.log(pclogging.INFO, __name__, "Command %s Recieved" % command)

        print("Processing Command: ", command)
        if (command == "STATUS"):

            completeCommandWithValue(logString)

            return True

        if (command == "RESETSWARM"):

            SendRESET_SWARM_PACKET(s)
		
            completeCommand()

            return True

        # check for , commands

        print("command=%s" % command)
        myCommandList = command.split(',')
        print("myCommandList=", myCommandList)

        if (len(myCommandList) > 1):   
            # we have a list command
		
            if (myCommandList[0]== "BLINKLIGHT"):
                SendBLINK_BRIGHT_LED(s, int(myCommandList[1]), 1)

            if (myCommandList[0]== "RESETSELECTED"):
                SendRESET_ME_PACKET(s, int(myCommandList[1]))

            if (myCommandList[0]== "SENDSERVER"):
                SendDEFINE_SERVER_LOGGER_PACKET(s)

            completeCommand()

            return True
		

			
        completeCommand()
			


        return False


# UDP Commands and packets

def SendDEFINE_SERVER_LOGGER_PACKET(s):
    print("DEFINE_SERVER_LOGGER_PACKET Sent") 
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# get IP address
    for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            print('%s: %s' % (ifaceName, ', '.join(addresses)))
  
    # last interface (wlan0) grabbed 
    print(addresses) 
    myIP = addresses[0].split('.')
    print(myIP) 
    data= ["" for i in range(14)]

    
    data[0] = int("F0", 16).to_bytes(1,'little') 
    data[1] = int(DEFINE_SERVER_LOGGER_PACKET).to_bytes(1,'little')
    data[2] = int("FF", 16).to_bytes(1,'little') # swarm id (FF means not part of swarm)
    data[3] = int(VERSIONNUMBER).to_bytes(1,'little')
    data[4] = int(myIP[0]).to_bytes(1,'little') # 1 octet of ip
    data[5] = int(myIP[1]).to_bytes(1,'little') # 2 octet of ip
    data[6] = int(myIP[2]).to_bytes(1,'little') # 3 octet of ip
    data[7] = int(myIP[3]).to_bytes(1,'little') # 4 octet of ip
    data[8] = int(0x00).to_bytes(1,'little')
    data[9] = int(0x00).to_bytes(1,'little')
    data[10] = int(0x00).to_bytes(1,'little')
    data[11] = int(0x00).to_bytes(1,'little')
    data[12] = int(0x00).to_bytes(1,'little')
    data[13] = int(0x0F).to_bytes(1,'little')
    mymessage = ''.encode()  	
    s.sendto(mymessage.join(data), ('<broadcast>'.encode(), MYPORT))
	
def SendRESET_SWARM_PACKET(s):
    print("RESET_SWARM_PACKET Sent") 
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    data= ["" for i in range(14)]

    data[0] = int("F0", 16).to_bytes(1,'little')
    
    data[1] = int(RESET_SWARM_PACKET).to_bytes(1,'little')
    data[2] = int("FF", 16).to_bytes(1,'little') # swarm id (FF means not part of swarm)
    data[3] = int(VERSIONNUMBER).to_bytes(1,'little')
    data[4] = int(0x00).to_bytes(1,'little')
    data[5] = int(0x00).to_bytes(1,'little')
    data[6] = int(0x00).to_bytes(1,'little')
    data[7] = int(0x00).to_bytes(1,'little')
    data[8] = int(0x00).to_bytes(1,'little')
    data[9] = int(0x00).to_bytes(1,'little')
    data[10] = int(0x00).to_bytes(1,'little')
    data[11] = int(0x00).to_bytes(1,'little')
    data[12] = int(0x00).to_bytes(1,'little')
    data[13] = int(0x0F).to_bytes(1,'little')
      	
    mymessage = ''.encode()  	
    s.sendto(mymessage.join(data), ('<broadcast>'.encode(), MYPORT))
	
def SendRESET_ME_PACKET(s, swarmID):
    print("RESET_ME_PACKET Sent") 
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    data= ["" for i in range(14)]

    data[0] = int("F0", 16).to_bytes(1,'little')
    
    data[1] = int(RESET_ME_PACKET).to_bytes(1,'little')
    data[2] = int(swarmStatus[swarmID][5]).to_bytes(1,'little')
    data[3] = int(VERSIONNUMBER).to_bytes(1,'little')
    data[4] = int(0x00).to_bytes(1,'little')
    data[5] = int(0x00).to_bytes(1,'little')
    data[6] = int(0x00).to_bytes(1,'little')
    data[7] = int(0x00).to_bytes(1,'little')
    data[8] = int(0x00).to_bytes(1,'little')
    data[9] = int(0x00).to_bytes(1,'little')
    data[10] = int(0x00).to_bytes(1,'little')
    data[11] = int(0x00).to_bytes(1,'little')
    data[12] = int(0x00).to_bytes(1,'little')
    data[13] = int(0x0F).to_bytes(1,'little')
      	
    mymessage = ''.encode()  	
    s.sendto(mymessage.join(data), ('<broadcast>'.encode(), MYPORT))


def SendCHANGE_TEST_PACKET(s, swarmID):
    print("RESET_ME_PACKET Sent") 
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    data= ["" for i in range(14)]

    data[0] = int("F0", 16).to_bytes(1,'little')
    
    data[1] = int(RESET_ME_PACKET).to_bytes(1,'little')
    data[2] = int(swarmStatus[swarmID][5]).to_bytes(1,'little')
    
    data[3] = int(VERSIONNUMBER).to_bytes(1,'little')
    data[4] = int(0x00).to_bytes(1,'little')
    data[5] = int(0x00).to_bytes(1,'little')
    data[6] = int(0x00).to_bytes(1,'little')
    data[7] = int(0x00).to_bytes(1,'little')
    data[8] = int(0x00).to_bytes(1,'little')
    data[9] = int(0x00).to_bytes(1,'little')
    data[10] = int(0x00).to_bytes(1,'little')
    data[11] = int(0x00).to_bytes(1,'little')
    data[12] = int(0x00).to_bytes(1,'little')
    data[13] = int(0x0F).to_bytes(1,'little')
      	
    mymessage = ''.encode()  	
    s.sendto(mymessage.join(data), ('<broadcast>'.encode(), MYPORT))
	

def SendBLINK_BRIGHT_LED(s, swarmID, seconds):
    print("BLINK_BRIGHT_LED Sent") 
    print("swarmStatus=", swarmStatus);
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    data= ["" for i in range(0,14)]

    data[0] = int("F0", 16).to_bytes(1,'little')
    
    data[1] = int(BLINK_BRIGHT_LED).to_bytes(1,'little')
    print("swarmStatus[swarmID][5]", swarmStatus[swarmID][5]) 
    
    data[2] = int(swarmStatus[swarmID][5]).to_bytes(1,'little')
    data[3] = int(VERSIONNUMBER).to_bytes(1,'little')
    if (seconds > 12.6):
        seconds = 12.6
    data[4] = int(seconds*10).to_bytes(1,'little')
    data[5] = int(0x00).to_bytes(1,'little')
    data[6] = int(0x00).to_bytes(1,'little')
    data[7] = int(0x00).to_bytes(1,'little')
    data[8] = int(0x00).to_bytes(1,'little')
    data[9] = int(0x00).to_bytes(1,'little')
    data[10] = int(0x00).to_bytes(1,'little')
    data[11] = int(0x00).to_bytes(1,'little')
    data[12] = int(0x00).to_bytes(1,'little')
    data[13] = int(0x0F).to_bytes(1,'little')
      	
    mymessage = ''.encode()  	
    s.sendto(mymessage.join(data), ('<broadcast>'.encode(), MYPORT))
    
	

def parseLogPacket(message):
       
	incomingSwarmID = setAndReturnSwarmID((message[2]))
	print("Log From SwarmID:",(message[2]))
	print("Swarm Software Version:", (message[4]))
	
	print("StringLength:",(message[3]))
	logString = ""
	for i in range(0,(message[3])):
		logString = logString + chr((message[i+5]))

	#print("logString:", logString)	
	return logString	



# build Webmap


def buildWebMapToFile(logString, swarmSize ):



    webresponse = ""

    swarmList = logString.split("|")
    for i in range(0,swarmSize):
        swarmElement = swarmList[i].split(",")	
        print("swarmElement=", swarmElement)
        webresponse += "<figure>"
        webresponse += "<figcaption"
        webresponse += " style='position: absolute; top: "
        webresponse +=  str(100-20)
        webresponse +=  "px; left: " +str(20+120*i)+  "px;'/>\n"
        if (int(swarmElement[5]) == 0):
            webresponse += "&nbsp;&nbsp;&nbsp&nbsp;&nbsp;---"
        else:
            webresponse += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s" % swarmElement[5]
				
        webresponse += "</figcaption>"
        #webresponse += "<img src='" + "http://192.168.1.40:9750"
        webresponse += "<img src='" 
			
			
        if (swarmElement[4] == "PR"):
            if (swarmElement[1] == "1"):
                webresponse += "On-Master.png' style='position: absolute; top: "
            else:
                webresponse += "On-Slave.png' style='position: absolute; top: "
        else:
            if (swarmElement[4] == "TO"):
                webresponse += "Off-TimeOut.png' style='position: absolute; top: "
            else:
                webresponse += "Off-NotPresent.png' style='position: absolute; top: "

        webresponse +=  str(100)
        webresponse +=  "px; left: " +str(20+120*i)+  "px;'/>\n"

        webresponse += "<figcaption"
        webresponse += " style='position: absolute; top: "
        webresponse +=  str(100+100)
        webresponse +=  "px; left: " +str(20+120*i)+  "px;'/>\n"
        if (swarmElement[4] == "PR"):
            if (swarmElement[1] == "1"):
                webresponse += "&nbsp;&nbsp;&nbsp;&nbsp;Master"
            else:
                webresponse += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Slave"
        else:
            if (swarmElement[4] == "TO"):
                webresponse += "TimeOut" 
            else:
                webresponse += "Not Present" 

				
        webresponse += "</figcaption>"
			
        webresponse += "</figure>"



    f = open("/home/pi/SDL_Pi_LightSwarm/state/figure.html", "w")

    f.write(webresponse)

    f.close()

    f = open("/home/pi/SDL_Pi_LightSwarm/state/swarm.html", "w")
    fh = open("/home/pi/SDL_Pi_LightSwarm/state/swarmheader.txt", "r")
    ff = open("/home/pi/SDL_Pi_LightSwarm/state/swarmfooter.txt", "r")

    webheader = fh.read()
    webfooter = ff.read()

    f.write(webheader)
    f.write(webresponse)
    f.write(webfooter)

    f.close
    fh.close
    ff.close


def setAndReturnSwarmID(incomingID):
 
  
    for i in range(0,SWARMSIZE):
        if (swarmStatus[i][5] == incomingID):
            return i
        else:
            if (swarmStatus[i][5] == 0):  # not in the system, so put it in
    
                swarmStatus[i][5] = incomingID;
                print("incomingID %d " % incomingID)
                print("assigned #%d" % i)
                return i
    
  
    # if we get here, then we have a new swarm member.   
    # Delete the oldest swarm member and add the new one in 
    # (this will probably be the one that dropped out)
  
    oldTime = time.time();
    oldSwarmID = 0
    for i in range(0,SWARMSIZE):
        if (oldTime > swarmStatus[i][1]):
            ldTime = swarmStatus[i][1]
            oldSwarmID = i
  		
 
 

    # remove the old one and put this one in....
    swarmStatus[oldSwarmID][5] = incomingID;
    # the rest will be filled in by Light Packet Receive
    print("oldSwarmID %i" % oldSwarmID)
 
    return oldSwarmID 
  

# set up sockets for UDP

s=socket(AF_INET, SOCK_DGRAM)
host = 'localhost';
s.bind(('',MYPORT))

print("--------------")
print("LightSwarm Logger")
print("Version ", VERSIONNUMBER)
print("--------------")

 
# first send out DEFINE_SERVER_LOGGER_PACKET to tell swarm where to send logging information 

SendDEFINE_SERVER_LOGGER_PACKET(s)
time.sleep(3)
SendDEFINE_SERVER_LOGGER_PACKET(s)



# swarmStatus
swarmStatus = [[0 for x  in range(6)] for x in range(SWARMSIZE)]

# 6 items per swarm item

# 0 - NP  Not present, P = present, TO = time out
# 1 - timestamp of last LIGHT_UPDATE_PACKET received
# 2 - Master or slave status   M S
# 3 - Current Test Item - 0 - CC 1 - Lux 2 - Red 3 - Green  4 - Blue
# 4 - Current Test Direction  0 >=   1 <=
# 5 - IP Address of Swarm


for i in range(0,SWARMSIZE):
	swarmStatus[i][0] = "NP"
	swarmStatus[i][5] = 0


#300 seconds round
seconds_300_round = time.time() + 300.0

#120 seconds round
seconds_120_round = time.time() + 120.0

completeCommand() 



while(1) :
     
         
    # receive datclient (data, addr)
    d = s.recvfrom(1024)

    message = d[0]
    addr = d[1]

    if (len(message) == 14):


        if (message[1] == LIGHT_UPDATE_PACKET):
            incomingSwarmID = setAndReturnSwarmID((message[2]))
            swarmStatus[incomingSwarmID][0] = "P"
            swarmStatus[incomingSwarmID][1] = time.time()  
            #print("in LIGHT_UPDATE_PACKET")
		         	
        if ((message[1]) == RESET_SWARM_PACKET):
            print("Swarm RESET_SWARM_PACKET Received")
            print("received from addr:",addr)	

        if ((message[1]) == CHANGE_TEST_PACKET):
            print("Swarm CHANGE_TEST_PACKET Received")
            print("received from addr:",addr)	

        if ((message[1]) == RESET_ME_PACKET):
            print("Swarm RESET_ME_PACKET Received")
            print("received from addr:",addr)	

        if ((message[1]) == DEFINE_SERVER_LOGGER_PACKET):
            print("Swarm DEFINE_SERVER_LOGGER_PACKET Received")
            print("received from addr:",addr)	
		
        if ((message[1]) == MASTER_CHANGE_PACKET):
            print("Swarm MASTER_CHANGE_PACKET Received")
            print("received from addr:",addr)	

        #for i in range(0,14):  
        #    print("ls["+str(i)+"]="+format((message[i]), "#04x"))

    else:
        if ((message[1]) == LOG_TO_SERVER_PACKET):
            print("Swarm LOG_TO_SERVER_PACKET Received")

            # process the Log Packet
            logString = parseLogPacket(message)
            buildWebMapToFile(logString, SWARMSIZE )

        else:
            print("error message length = ",len(message))
         
    if (time.time() >  seconds_120_round):
        # do our 2 minute round
        print(">>>>doing 120 second task")
        sendTo = random.randint(0,SWARMSIZE-1)
        SendBLINK_BRIGHT_LED(s, sendTo, 1)
        seconds_120_round = time.time() + 120.0	

    if (time.time() >  seconds_300_round):
        # do our 2 minute round
        print(">>>>doing 300 second task")
        SendDEFINE_SERVER_LOGGER_PACKET(s)
        seconds_300_round = time.time() + 300.0	

    processCommand(s)
   
    #print swarmStatus 
