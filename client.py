#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys  #for exit
from random import randint
import datetime
#Establishes a UDP-socket
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print 'Misslyckades med att skapa socket. Felkod: ' + str(msg[0]) + ' , Felmeddelande : ' + msg[1]
    sys.exit();
host = socket.gethostname() # IP of the server change if not localhost!!
port = 1234
#-----------------------------
#Global variables
recv_time = ()
post_time = ()

# Just a hacky way for the server to know who has connected
def tell_server_of_connection():
    udp_socket.sendto("unneccessary", (host,port))

# Recieve the random generated position from the server
def recieve_position_and_object_from_server():
    msg, addr = udp_socket.recvfrom(1024)
    data = msg.split(',')
    obj = data[0]
    coord = data[1],data[2]
    global recv_time
    recv_time = datetime.datetime.now()
    return obj, coord

def send_timestamp():
    global post_time
    global recv_time
    post_time = datetime.datetime.now()
    diff_time = post_time - recv_time
    udp_socket.sendto('[1,'+str(diff_time)+']', (host,port))


# def main():
#    tell_server_of_connection()
#    while True:
#        recieve_position_and_object_from_server()
#        send_timestamp()
#    s.close
# if __name__ == "__main__":
#    main()
