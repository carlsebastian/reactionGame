#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys  #for exit
from random import randint

#Get ip address of interface wlp2s0
#import netifaces as ni
#ni.ifaddresses('wlp2s0')
#ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
#------------

#Establishes a UDP-socket
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
except socket.error, msg:
    print 'Misslyckades med att skapa socket. Felkod: ' + str(msg[0]) + ' , Felmeddelande : ' + msg[1]
    sys.exit();
host = socket.gethostname() #ip
port = 1234
udp_socket.bind((host, port))
message = []
address = []
#-----------------------------

#randomized coordinates for objects
def randomize_coordinates():
    obj = (randint(0, 10))
    x = (randint(100, 1000)) #random integer
    y = (randint(100, 1000))
    return str(obj)+','+str(x)+','+str(y)

#sends position to players from array address
def send_position_to_players(position, address):
    # Send postion to players
    j = 0
    while j<len(address):
        try:
            udp_socket.sendto(position,address[j])
        except socket.error, msg:
            print 'Misslyckades med sändning av position. Felkod: '+str(msg[0])+', Felmeddelande: '+msg[1]
            sys.exit();
        j = j+1
    return True

#awaits udp connections from clients and puts them into the global variable address
def await_connections():
    i = 0
    while i<2: # Wait for connection from players
        m, a = udp_socket.recvfrom(1024)
        address.append(a)
        print 'connection from', address[i]
        i = i+1
    return True

#Receive timestamp from clients and append to message array
def recieve_timestamp():
    i = 0
    while i<2: # Wait for connection from players
        m, a = udp_socket.recvfrom(1024)
        message.append(m)
        i = i+1
    return True


#Main routine, GameHandler
def main():
    #Some variables Needed
    global address # Address array from connected clients
    global message # Messages from connected clients, might be redundant.
    connection_limit = False
    sent_position = False
    got_timestamps = False

    print "listening on port, and address" , host, port
    while True:
        random_position_and_object = randomize_coordinates()
        if(not connection_limit):
            connection_limit = await_connections()
        if(not sent_position):
            sent_position = send_position_to_players(random_position_and_object, address)
            got_timestamps = False
        if(not got_timestamps):
            got_timestamps = recieve_timestamp()
            sent_position = False
    udp_socket.close()

if __name__ == "__main__":
    main()
