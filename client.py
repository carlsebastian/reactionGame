#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys  #for exit
from random import randint
#Establishes a UDP-socket
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
    print 'Misslyckades med att skapa socket. Felkod: ' + str(msg[0]) + ' , Felmeddelande : ' + msg[1]
    sys.exit();
host = socket.gethostname() # IP of the server change if not localhost!!
port = 1234
#-----------------------------

# Just a hacky way for the server to know who has connected
def tell_server_of_connection():
    udp_socket.sendto("unneccessary", (host,port))

# Recieve the random generated position from the server
def recieve_position_and_object_from_server():
    msg, addr = udp_socket.recvfrom(1024)
    data = msg.split(',')
    obj = data[0]
    coord = data[1],data[2]
    return obj, coord

def send_timestamp():
    udp_socket.sendto("[1,timestamp]", (host,port))


#def main():
#    tell_server_of_connection()
#    while True:
#        recieve_position_and_object_from_server()
#        send_timestamp()
#    s.close
#if __name__ == "__main__":
#    main()
