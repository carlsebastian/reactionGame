#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
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
udp_socket = ''
host = '' #ip
port = 1234
user = []
round_result = []
message = []
address = []
userid_winner = ''
score_game = [] #only the scores througout a game
user_score = '' #Score and the corresponding user throughout a game
#logging variables
addressip = []
old_players_ip = []
old_scores = []
#-----------------------------

#Establishes a UDP-socket
def establish_socket():
    global udp_socket
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        udp_socket.bind((host, port))
    except socket.error as msg:
        print ('Misslyckades med att skapa socket. Felkod: ' + str(msg[0]) + ' , Felmeddelande : ' + msg[1])
        sys.exit();

#randomized coordinates for objects
def randomize_coordinates():
    obj = (randint(0, 2))
    x = (randint(100, 500)) #random integer
    y = (randint(100, 500))
    w = (randint(1, 5))
    time  = datetime.datetime.now() + datetime.timedelta(0,w)
    return str(obj)+','+str(x)+','+str(y) + ',' + str(time)

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
def await_connections(load):
    global score_game, addressip
    i = 0
    while i<2: # Wait for connection from players
        m, a = udp_socket.recvfrom(1024)
        address.append(a)
        addressip.append(a[0])
        user.append(m)
        score_game.append(0)
        print("connection from "+str(address[i])+",  Player Name: " +user[i])
        i = i+1
    #Log loading crosschecking with connected IP's
    if(load):
        i = 0
        try:
            temp = ''
            for i in range(len(old_players_ip)):
                addr_i = addressip.index(old_players_ip[i])
                #Endast buggfix för localhostspel och om man är max 2 spelare och slump vem som får score

                if addr_i == temp:
                    addr_i = addr_i+1
                #----------------
                score_game[addr_i] = int(old_scores[addr_i])
                # fortsättnig
                temp = addr_i
                #----------------
                i = i+1
        except ValueError:
            pass
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
    global user_score
    user_score = ''
    if userid_winner != '':
        winner_i = user.index(userid_winner)
        score_game[winner_i] = score_game[winner_i]+1
    i = 0
    for i in range(len(score_game)):
        user_score = user_score+user[i]+','+str(score_game[i])+';'
        i = i+1
    for addr in address:
        udp_socket.sendto(user_score,addr)

#logging
def log_round():
    log_result = '' # Logga variables som håller round-info
    i = 0
    addrip = []
    for addr in address:
        addrip.append(addr[0])
    for i in range(len(score_game)):
        log_result = log_result+str(addrip[i])+','+str(score_game[i])+';'
        i = i+1
    pickle.dump(log_result, open( "log.p", "wb" ) )

#Erase log.p
def log_erase():
    empty = '' # Tömmer filen, vill vi göra efter varje avslutat spel, samt kanske i början
    pickle.dump( empty, open( "log.p", "wb" ) )

def log_load_values(log):
    global old_scores, old_players_ip
    data = log.split(';')
    for i in range(len(data)-1):
        p = data[i].split(',')
        old_players_ip.append(p[0])
        old_scores.append(p[1])

def log_check():
    global user_score
    log = ''
    try:
        log = pickle.load(open("log.p", "rb"))
    except IOError:
        log_erase()
        return False
    if log != '':
        print(log)
        print('förra spelet avslutades ej! Laddar in...')
        log_load_values(log)
        print('Done!')
        return True

def take_arg_ip():
    global host
    if len(sys.argv)>1:
        host = str(sys.argv[1])
    else:
        host = socket.gethostname()
        print('!!To provide your IP instead of default "gethostname", give ip as an argument "python server <ip>"!!')
#Main routine, GameHandler
def main():
    take_arg_ip()
    establish_socket()
    #Some variables Needed
    global address # Address array from connected clients
    global message # Messages from connected clients, might be redundant.
    connection_limit = False
    sent_position = False
    got_timestamps = False
    old_bool = log_check()
    print ("listening on port, and address" , host, port)
    i= 0 # test
    while i<5:
        random_position_and_object = randomize_coordinates()
        if(not connection_limit):
            connection_limit = await_connections(old_bool)
        score_send_clients()
        log_round()
        if(not sent_position):
            sent_position = send_position_to_players(random_position_and_object, address)
            got_timestamps = False
        if(not got_timestamps):
            got_timestamps = recieve_timestamp()
            sent_position = False
        score_present_server()
        i= i+1
    log_erase()
    udp_socket.close()

if __name__ == "__main__":
    main()
