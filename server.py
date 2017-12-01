#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import socket
import sys  #for exit
from random import randint
import datetime
#Get ip address of interface wlp2s0
#import netifaces as ni
#ni.ifaddresses('wlp2s0')
#ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
#------------

#Establishes a UDP-socket
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
except socket.error as msg:
    print ('Misslyckades med att skapa socket. Felkod: ' + str(msg[0]) + ' , Felmeddelande : ' + msg[1])
    sys.exit();
host = socket.gethostname() #ip
port = 1234
udp_socket.bind((host, port))
user = []
round_result = []
message = []
address = []
userid_winner = ''
score_game = []
#-----------------------------

#randomized coordinates for objects
def randomize_coordinates():
    obj = (randint(1, 1))
    x = (randint(100, 500)) #random integer
    y = (randint(100, 500))
    return str(obj)+','+str(x)+','+str(y)

#sends position to players from array address
def send_position_to_players(position, address):
    # Send postion to players
    j = 0
    while j<len(address):
        try:
            udp_socket.sendto(position,address[j])
        except socket.error as msg:
            print ('Misslyckades med sändning av position. Felkod: '+str(msg[0])+', Felmeddelande: '+msg[1])
            sys.exit();
        j = j+1
    return True

#awaits udp connections from clients and puts them into the global variable address
def await_connections():
    i = 0
    while i<2: # Wait for connection from players
        m, a = udp_socket.recvfrom(1024)
        address.append(a)
        user.append(m)
        score_game.append(0)
        print("connection from "+str(address[i])+",  Player Name: " +user[i])
        i = i+1
    return True

#Receive timestamp from clients and append to message array
def recieve_timestamp():
    i = 0
    while i<2: # Wait for connection from players
        m, a = udp_socket.recvfrom(1024)
        ui = address.index(a)
        userid = user[ui]
        round_result.append([userid,m])
        i = i+1
    return True

#present the winner
def score_present_server():
    global round_result, userid_winner
    oldmax = round_result[0]
    for potnewmax in round_result:
        if potnewmax[1] <= oldmax[1]:
            oldmax = potnewmax
    print(oldmax[0], 'Is the winner')
    userid_winner = oldmax[0]
    round_result = []

#send winner to clients
def score_send_clients():
    print userid_winner
    if userid_winner != '':
        winner_i = user.index(userid_winner)
        score_game[winner_i] = score_game[winner_i]+1
    user_score = ''
    i = 0
    for i in range(len(score_game)):
        user_score = user_score+user[i]+','+str(score_game[i])+';'
        i = i+1
    for addr in address:
        udp_socket.sendto(user_score,addr)

#logging
def log_round():
    log_result = {} # Logga variables som håller round-info
    pickle.dump(log_result, open( "log.p", "ab" ) )

#Erase log.p
def log_erase():
    empty = {} # Tömmer filen, vill vi göra efter varje avslutat spel, samt kanske i början
    pickle.dump( empty, open( "log.p", "wb" ) )

#Main routine, GameHandler
def main():
    #Some variables Needed
    global address # Address array from connected clients
    global message # Messages from connected clients, might be redundant.
    connection_limit = False
    sent_position = False
    got_timestamps = False

    print ("listening on port, and address" , host, port)
    i= 0 # test
    while i<5:
        random_position_and_object = randomize_coordinates()
        if(not connection_limit):
            connection_limit = await_connections()
        score_send_clients()
        if(not sent_position):
            sent_position = send_position_to_players(random_position_and_object, address)
            got_timestamps = False
        if(not got_timestamps):
            got_timestamps = recieve_timestamp()
            sent_position = False
        score_present_server()
        i= i+1
    udp_socket.close()

if __name__ == "__main__":
    main()
